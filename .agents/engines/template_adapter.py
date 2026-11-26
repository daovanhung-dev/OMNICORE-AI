"""Chọn template tường minh; không chỉnh sửa tài nguyên nguyên bản."""
import json,re,shutil
from pathlib import Path
from context import digest
ORIG={'api':'create_dd_api/docs/dd/DD_API_Template_MD','screen':'create_dd_screen/01-TEMPLATES/SCREEN_ID','module':'create-dd-mobile/template'}
PLACEHOLDER=re.compile(r'\{\{[^{}\n]+\}\}|`?<\s*[A-ZÀ-Ỹ_][A-ZÀ-Ỹ_0-9 /.-]*>|\b(?:TBD|NOT_YET_REVIEWED|__ID__|__SLUG__)\b',re.U)
# Template gốc có phụ lục đối chiếu Excel chứa placeholder, không phải phần authoring.
def body(t):return t.split('## Phụ lục đối chiếu nguồn Excel',1)[0]
def files(a,kind,mode):
    if kind not in ORIG:raise ValueError('Loại DD không hợp lệ')
    if mode=='original':
        base=a/'skills-original'/ORIG[kind]
        mapping={p.relative_to(base).as_posix():p for p in base.rglob('*.md')}
        if kind=='module':mapping['history/CHANGELOG.md']=mapping.pop('history/README.md')
    elif mode=='adapted':
        s=json.loads((a/'workflows/registry.json').read_text())['templates'][kind];base=a/s['dir'];mapping={p:base/p for p in s['files']}
    else:raise ValueError('Chỉ hỗ trợ original hoặc adapted; template ngoài cần review riêng')
    return mapping

def create_dd(a,kind,mode,dest):
    mapping=files(a,kind,mode)
    if dest.exists():raise FileExistsError('Không ghi đè DD')
    dest.mkdir(parents=True)
    for rel,src in mapping.items():
        p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,p)
    # Metadata nằm ở đầu ra, không thay đổi template.
    (dest/'template-origin.json').write_text(json.dumps({'kind':kind,'mode':mode,'files':{p:digest(s) for p,s in mapping.items()}},ensure_ascii=False,indent=2)+'\n')
    return dest

def has_table_rows(t):
    lines=t.splitlines()
    for i,line in enumerate(lines[:-2]):
        if line.startswith('|') and re.fullmatch(r'[| :\-]+',lines[i+1]) and lines[i+2].startswith('|'):
            cells=[x.strip() for x in lines[i+2].strip('|').split('|')]
            if any(x and x not in {'-', '—', 'N/A'} for x in cells):return True
    return False

def headings(t):
    return re.findall(r'^#{1,6} .+$',re.sub(r'```.*?```','',t,flags=re.S),re.M)

def verify_dd(a,kind,dest,mode):
    mapping=files(a,kind,mode);issues=[]
    for rel,src in mapping.items():
        p=dest/rel
        if not p.is_file() or p.is_symlink():issues.append('Thiếu '+rel);continue
        t=body(p.read_text(encoding='utf8')); baseline=body(src.read_text(encoding='utf8'))
        if not t.strip() or digest(p)==digest(src):issues.append('Chưa điền '+rel)
        if PLACEHOLDER.search(t):issues.append('Placeholder '+rel)
        # Kiểm tra nội dung và heading tĩnh của tài liệu chính; không ép README hướng dẫn của template vào dự án.
        if not headings(t):issues.append('Thiếu heading '+rel)
        core=Path(rel).name not in {'README.md','CHANGELOG.md'}
        if core:
            actual=set(headings(t))
            for h in headings(baseline):
                if h.startswith('# '):continue
                if not PLACEHOLDER.search(h) and '[' not in h and h not in actual:issues.append('Thiếu heading '+rel+': '+h)
            if has_table_rows(baseline) and not has_table_rows(t):issues.append('Thiếu bảng dữ liệu '+rel)
            if len(re.sub(r'[\s#|`_\-]','',t))<40:issues.append('Nội dung quá ngắn '+rel)
        for content in re.findall(r'```json\s*\n(.*?)```',t,re.S):
            try:json.loads(content)
            except ValueError:issues.append('JSON sai '+rel)
    if kind=='api':
        # Ma trận phải có nội dung thật, không chỉ tiêu đề, trường nguồn được đối chiếu tại review.
        for name in ['request-usage','query','mutation','response-source']:
            p=dest/'matrices'/f'{name}.md'
            if not p.is_file() or len([x for x in p.read_text().splitlines() if x.startswith('|')])<3 or PLACEHOLDER.search(p.read_text()):issues.append('Thiếu ma trận hoặc chưa điền: '+name)
    if kind=='module':
        docs={n:(dest/n).read_text(encoding='utf8') if (dest/n).is_file() else '' for n in ['Overall.md','List_Features.md','Function_List.md','Views.md','Import_File.md']}
        for label,pattern,owner,refs in [('feature',r'\b(?:[A-Z0-9]+-)?F-?\d{2,3}\b','List_Features.md',['Overall.md','Function_List.md']),('function',r'\b(?:[A-Z0-9]+-)?FN-?\d{2,3}\b','Function_List.md',['List_Features.md','Views.md','Import_File.md']),('view',r'\b(?:[A-Z0-9]+-)?V-?\d{2,3}\b','Views.md',['List_Features.md'])]:
            ids=set(re.findall(pattern,docs[owner]))
            if not ids:issues.append('Thiếu ID '+label+' trong '+owner)
            for ref in refs:
                if not ids.intersection(re.findall(pattern,docs[ref])):issues.append('Thiếu truy vết '+label+' giữa '+owner+' và '+ref)
    if kind=='screen':
        for name in ['screen-clean.png','screen-numbered.png']:
            p=dest/'images'/name
            if not p.is_file() or p.read_bytes()[:8]!=b'\x89PNG\r\n\x1a\n':issues.append('Thiếu ảnh PNG hợp lệ '+name)
    return {'kind':kind,'mode':mode,'required_files':len(mapping),'issues':issues,'semantic_review':'HUMAN_REQUIRED'}
