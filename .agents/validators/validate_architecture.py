"""Kiểm định tĩnh hồ sơ FastAPI và TypeScript; không chạy mã nguồn được kiểm."""
import argparse, ast, json, re, sys, importlib.util
from pathlib import Path
A=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('inventory',A/'codebase/inventory.py');inv=importlib.util.module_from_spec(spec);spec.loader.exec_module(inv)
SQL=re.compile(r'^\s*(SELECT\s|INSERT\s|UPDATE\s|DELETE\s|WITH\s|CREATE\s+TABLE|DROP\s+TABLE|ALTER\s+TABLE)',re.I)

def validate(backend: Path, frontend: Path):
    issues=[]
    def err(rule,p,line,msg):issues.append({'rule':rule,'path':str(p),'line':line,'message':msg})
    modules=backend/'app/modules'; app=frontend/'src/app'; features=app/'features'
    if not modules.is_dir():err('BE-001',modules,0,'Thiếu gốc module')
    if not features.is_dir():err('FE-001',features,0,'Thiếu gốc màn hình')
    apis=[p for p in modules.glob('*/*') if p.is_dir() and not p.name.startswith(('.', '__'))]
    screens=[p for p in features.glob('*/*') if p.is_dir() and not p.name.startswith(('.', '__'))]
    if not apis:err('BE-001',modules,0,'Không có API để xác minh')
    if not screens:err('FE-001',features,0,'Không có màn hình để xác minh')
    for p in apis:
        for n in ['models.py','query.py','validate.py','view.py']:
            if not (p/n).is_file():err('BE-001',p,0,'Thiếu '+n)
        extra={f.name for f in p.glob('*.py')}-{'models.py','query.py','validate.py','view.py','__init__.py'}
        if extra:err('BE-001',p,0,'Tệp trách nhiệm ngoài quy chuẩn: '+str(sorted(extra)))
    graph={}
    modules_by_name={'.'.join(p.relative_to(backend).with_suffix('').parts):p for p in backend.glob('app/**/*.py')}
    for p in backend.glob('app/**/*.py'):
        if p.is_symlink():continue
        try:t=ast.parse(p.read_text())
        except (SyntaxError,UnicodeError) as e:err('PARSE',p,0,str(e));continue
        rel=p.relative_to(backend).parts;in_api='modules' in rel;core='core' in rel
        module='.'.join(p.relative_to(backend).with_suffix('').parts);graph[module]=set()
        capabilities=set(); aliases={}
        for node in ast.walk(t):
            if isinstance(node,ast.ImportFrom):
                base=node.module or ''
                if node.level:
                    parent=module.split('.')[:-node.level];base='.'.join(parent+([base] if base else []))
                for a0 in node.names:
                    target=base+'.'+a0.name
                    aliases[a0.asname or a0.name]=target
                    if target in modules_by_name:graph[module].add(target)
                    elif base in modules_by_name:graph[module].add(base)
                    if any(k in target.split('.') for k in ('database','repository','repositories','sqlalchemy','psycopg','sqlite3','requests','httpx','redis','subprocess')):capabilities.add(a0.asname or a0.name)
            elif isinstance(node,ast.Import):
                for a0 in node.names:
                    aliases[a0.asname or a0.name]=a0.name
                    if a0.name in modules_by_name:graph[module].add(a0.name)
                    if a0.name.split('.')[0] in {'sqlite3','sqlalchemy','psycopg','requests','httpx','redis','subprocess'}:capabilities.add(a0.asname or a0.name)
        # Lan truyền alias đơn giản, ví dụ repo = db hoặc run = session.query.
        for node in ast.walk(t):
            if isinstance(node,(ast.Assign,ast.AnnAssign)) and node.value is not None:
                names=node.targets if isinstance(node,ast.Assign) else [node.target]
                val=ast.unparse(node.value)
                if val.split('.')[0] in capabilities or val.split('.')[-1] in {'query','execute','commit','rollback','get_db','get_session'}:
                    capabilities.update(x.id for x in names if isinstance(x,ast.Name))
        for n in ast.walk(t):
            if isinstance(n,(ast.Import,ast.ImportFrom)):
                names=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module or '']
                if core and any('modules' in x.split('.') for x in names):err('BE-010',p,n.lineno,'Core phụ thuộc module')
                if in_api and p.name!='view.py' and any(x.split('.')[-1] in {'view'} for x in names):err('BE-010',p,n.lineno,'Phụ thuộc ngược vào view')
            if in_api and p.name!='query.py' and isinstance(n,ast.Constant) and isinstance(n.value,str) and SQL.match(n.value):err('BE-007',p,n.lineno,'SQL đặt ngoài query')
            if in_api and p.name in {'models.py','validate.py','query.py'} and isinstance(n,ast.Call):
                name=ast.unparse(n.func)
                if name.split('.')[0] in capabilities or name in {'open','print','get_db','get_session'} or name.split('.')[-1] in {'execute','executemany','commit','rollback','connect','fetchone','fetchall','query','scalar','scalars','flush','add','delete','refresh','bulk_save_objects','get_connection','cursor'}:err('BE-003',p,n.lineno,'Thao tác I/O hoặc giao dịch sai lớp')
            if in_api and p.name=='view.py' and isinstance(n,ast.ClassDef):err('BE-002',p,n.lineno,'Khai báo lớp riêng trong view')
        if in_api and p.name=='query.py':
            for n in t.body:
                if not ((isinstance(n,(ast.Assign,ast.AnnAssign)) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str)) or (isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str))):
                    err('BE-005',p,n.lineno,'Query chỉ được khai báo truy vấn trong hồ sơ SQL này')
    visited=set();active=set()
    def walk(node):
        if node in active:err('BE-010',modules_by_name[node],0,'Phụ thuộc vòng tròn');return
        if node in visited:return
        active.add(node)
        for dep in graph.get(node,[]):walk(dep)
        active.remove(node);visited.add(node)
    for node in graph:walk(node)
    expected={'data-access','models','pages','ui'}
    for p in screens:
        found={x.name for x in p.iterdir() if x.is_dir() and not x.name.startswith('.')}
        if found!=expected:err('FE-001',p,0,'Thư mục màn hình sai: '+str(sorted(found)))
    for group in features.iterdir() if features.is_dir() else []:
        if group.is_dir() and not group.name.startswith('.'):
            if not (group/(group.name+'.route.ts')).is_file():err('FE-008',group,0,'Thiếu tuyến nhóm')
            if not (app/'layouts'/group.name).is_dir():err('FE-008',group,0,'Thiếu khung nhóm')
    inputs=[{'path':str(p),'text':p.read_text()} for p in app.rglob('*') if p.suffix in {'.ts','.tsx','.js','.jsx'} and p.is_file() and not p.is_symlink()]
    if not inputs:err('FE-001',app,0,'Không có mã nguồn FE để xác minh')
    for info in inv.ts_batch(inputs):
        p=Path(info['path']);parts=p.relative_to(app).parts;layer=parts[3] if len(parts)>4 and parts[0]=='features' else ''
        if info['status']!='STATIC_AST':err('PARSE',p,0,'Không phân tích được TypeScript: '+info['status']);continue
        for dep in info['imports']:
            raw=dep['path'];dest=(p.parent/raw).resolve() if raw.startswith('.') else None
            dest_parts=dest.relative_to(app.resolve()).parts if dest and dest.is_relative_to(app.resolve()) else ()
            if parts[0] in {'core','shared','layouts'} and ('features' in dest_parts or '/features/' in raw):err('FE-010',p,dep['line'],'Phụ thuộc ngược vào features')
            if layer in {'models','ui'} and (any(x in dest_parts for x in ['data-access','pages','http']) or 'HttpClient' in raw or raw in {'@angular/common/http','axios'}):err('FE-006',p,dep['line'],'Phụ thuộc truy cập dữ liệu sai lớp')
            if layer=='ui' and (dest_parts[:1]==('core',) or raw=='@angular/router' or any(x.endswith('.route.ts') or x.endswith('.route.js') for x in dest_parts)):err('FE-010',p,dep['line'],'UI phụ thuộc core/router')
            if layer and len(dest_parts)>=4 and dest_parts[0]=='features' and tuple(parts[1:3])!=tuple(dest_parts[1:3]):err('FE-010',p,dep['line'],'Screen nhập implementation screen khác')
        for call in info['calls']:
            name=call['name'];last=name.split('.')[-1]
            if layer in {'ui','models','pages'} and (last=='fetch' or last=='XMLHttpRequest' or name.startswith(('axios.','this.http.','http.'))):err('FE-006',p,call['line'],'Gọi HTTP trực tiếp ngoài data-access/core')
            if layer=='models' and name.startswith(('document.','localStorage.','sessionStorage.')):err('FE-005',p,call['line'],'Tác động phụ trong mô hình')
    return issues

def main():
    p=argparse.ArgumentParser(description='Kiểm định tĩnh kiến trúc');p.add_argument('--backend',required=True,type=Path);p.add_argument('--frontend',required=True,type=Path);args=p.parse_args()
    issues=validate(args.backend.resolve(),args.frontend.resolve());print(json.dumps({'status':'FAIL' if issues else 'PASS_STATIC','issues':issues},ensure_ascii=False,indent=2));return bool(issues)
if __name__=='__main__':sys.exit(main())
