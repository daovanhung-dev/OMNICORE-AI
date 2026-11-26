#!/usr/bin/env python3
"""Maintain a source-faithful, project-agnostic .agents/project/tree living mirror.

- Standard library only. Read-only source scan; writes exclusively to .agents/project.
- One README.md for every observed source directory, one Markdown document for
  each observed file, without copying source bodies or secret values.
- Generated sections are delimited, so user notes outside them survive --refresh.
- No framework assumptions, Git remote/network calls or writes to source files.
"""
from __future__ import annotations
import argparse
import ast
from collections import defaultdict
import datetime as dt
import hashlib
import json
import os
import shutil
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import re
import subprocess
import sys
import importlib.util
_spec=importlib.util.spec_from_file_location("inventory",Path(__file__).resolve().parents[2]/"codebase"/"inventory.py")
_inventory=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_inventory)

SKIP_DIRS={'.agents','.git','.hg','.svn','node_modules','.next','.nuxt','.angular','.venv','venv','__pycache__','dist','build','.dart_tool','.gradle','coverage','.idea','.vs','.tox','target','.turbo','Pods','vendor','.cache','.pytest_cache'}
SKIP_NAMES={'.DS_Store','Thumbs.db'}
SENSITIVE_NAMES={'.env','id_rsa','id_ed25519','.npmrc','.pypirc','credentials.json','service-account.json'}
SENSITIVE_EXTS={'.pem','.key','.p12','.pfx','.jks','.keystore'}
TEXT_EXTS={'.py','.pyi','.js','.jsx','.ts','.tsx','.mjs','.cjs','.vue','.svelte','.dart','.go','.rs','.java','.kt','.swift','.rb','.php','.cs','.cpp','.c','.h','.hpp','.sql','.html','.css','.scss','.sass','.json','.yaml','.yml','.toml','.ini','.sh','.bash','.ps1','.gradle','.graphql','.proto','.prisma','.xml','.md','.txt','.rst','.adoc','.conf','.tf','.tfvars','.vue','.svelte'}
SENTINEL_START='<!-- AUTO_CONTEXT_START -->'
SENTINEL_END='<!-- AUTO_CONTEXT_END -->'
SAFE_PATH=re.compile(r'^[^\x00-\x1f]+$')
MAX_DISPLAY=30


def run_git(repo:Path, *args:str) -> bytes | None:
    try:
        p=subprocess.run(['git',*args],cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=35)
        return p.stdout if p.returncode==0 else None
    except (OSError,subprocess.TimeoutExpired):
        return None


def select_source_paths(repo:Path):
    """Return normal regular files. Honors ignored files; handles non-Git projects."""
    manifest=run_git(repo,'ls-files','--cached','--others','--exclude-standard','-z')
    files=[]
    if manifest is not None:
        names=[os.fsdecode(x) for x in manifest.split(b'\0') if x]
        for s in sorted(set(names)):
            p=PurePosixPath(s)
            if s.startswith('/') or '..' in p.parts or any(part in SKIP_DIRS for part in p.parts) or p.name in SKIP_NAMES:
                continue
            f=repo.joinpath(*p.parts)
            if f.is_symlink() or not f.is_file():
                continue
            try:
                if not f.resolve().is_relative_to(repo.resolve()):continue
            except OSError:continue
            files.append(p.as_posix())
        mode='git-tracked-and-untracked-not-ignored'
    else:
        mode='filesystem-no-git'
        for base,dirs,names in os.walk(repo,followlinks=False):
            dirs[:]=sorted(d for d in dirs if d not in SKIP_DIRS and not (Path(base)/d).is_symlink())
            for name in sorted(names):
                if name in SKIP_NAMES:continue
                f=Path(base)/name
                if f.is_symlink() or not f.is_file():continue
                files.append(f.relative_to(repo).as_posix())
    return sorted(set(files)),mode



def select_source_dirs(repo:Path, mode:str)->list[str]:
    """Discover physical directories (including empty) except excluded/ignored/symlinks."""
    candidates=[]
    for root, dirs, _ in os.walk(repo,followlinks=False):
        base=Path(root)
        dirs[:]=sorted(d for d in dirs if d not in SKIP_DIRS and not (base/d).is_symlink())
        for directory in dirs:
            rel=(base/directory).relative_to(repo).as_posix()
            if rel and not any(part in SKIP_DIRS for part in PurePosixPath(rel).parts):
                candidates.append(rel)
    if mode.startswith('git-') and candidates:
        try:
            p=subprocess.run(['git','check-ignore','--stdin','-z'],cwd=repo,
                             input='\0'.join(candidates).encode('utf8')+b'\0',
                             capture_output=True,timeout=35)
            # Git check-ignore exit 1 means no ignored folders.
            if p.returncode in (0,1):
                ignored={os.fsdecode(x) for x in p.stdout.split(b'\0') if x}
                candidates=[d for d in candidates if d not in ignored]
        except (OSError,subprocess.TimeoutExpired):
            pass
    return sorted(set(candidates))


def is_sensitive(rel:str)->bool:
    p=PurePosixPath(rel);n=p.name
    return n in SENSITIVE_NAMES or (n.startswith('.env') and n not in {'.env.example','.env.sample','.env.template'}) or p.suffix.lower() in SENSITIVE_EXTS

def text_summary(rel:str, data:bytes, max_bytes:int):
    path=PurePosixPath(rel)
    name=path.name
    if is_sensitive(rel):
        return {'status':'PATH_ONLY_SENSITIVE','purpose':'Tệp cấu hình/khóa có khả năng chứa bí mật; không đọc hoặc xuất nội dung.','symbols':[],'imports':[],'notes':['Không sao chép secret, giá trị cấu hình, token hoặc credential vào context.']}
    if len(data)>max_bytes or b'\0' in data[:8192]:
        return {'status':'PATH_ONLY','purpose':'Tệp lớn/nhị phân; mô tả dựa trên đường dẫn, không khẳng định runtime.','symbols':[],'imports':[],'notes':[]}
    if path.suffix.lower() not in TEXT_EXTS and name not in {'Dockerfile','Makefile','Jenkinsfile','Procfile','Gemfile','Justfile','Caddyfile'}:
        return {'status':'PATH_ONLY','purpose':'Tài nguyên hoặc tệp chưa nhận diện; cần kiểm tra khi task liên quan.','symbols':[],'imports':[],'notes':[]}
    try: content=data.decode('utf-8')
    except UnicodeDecodeError:
        return {'status':'PATH_ONLY','purpose':'Tệp không phải UTF-8; không phân tích nội dung.','symbols':[],'imports':[],'notes':[]}
    purpose=classify_path(rel)
    symbols=[];imports=[];notes=[]
    ext=path.suffix.lower()
    if ext in {'.py','.pyi'}:
        try:
            tree=ast.parse(content)
            symbols=[f"{x['kind']} {x['name']}" for x in _inventory.py_symbols(content)]
            imports=[('.'*n.level+(n.module or '')) if isinstance(n,ast.ImportFrom) else ', '.join(x.name for x in n.names) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
            notes=['Python AST được phân tích tĩnh; import không chứng minh đường chạy runtime.']
        except SyntaxError:
            notes=['Không phân tích được AST; cần kiểm tra lại source.']
    elif ext in {'.js','.jsx','.ts','.tsx','.mjs','.cjs'}:
        parsed=_inventory.ts_batch([{'path':rel,'text':content}])[0]
        symbols=[f"{x['kind']} {x['name']}" for x in parsed['symbols']]
        imports=[x['path'] for x in parsed['imports']]
        notes=['Trạng thái bộ phân tích: '+parsed['status']+'; không chứng minh hành vi runtime.']
    elif ext in {'.dart','.go','.rs','.java','.kt','.cs','.rb','.php','.vue','.svelte'}:
        notes=['Chưa có bộ phân tích cú pháp được xác minh; không suy đoán khai báo.']
    elif ext=='.sql':
        symbols=[f'table {x}' for x in re.findall(r'(?im)\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?["`]?([\w.]+)',content)]
        notes=['Tồn tại DDL trong source không xác nhận schema database đã deploy.']
    elif ext=='.html':
        symbols=[f'element {x}' for x in re.findall(r'(?i)<(form|table|button|input|router-outlet|main|header|nav)\b',content)[:MAX_DISPLAY]]
    elif ext=='.json' and name=='package.json':
        try:
            o=json.loads(content)
            symbols=['script '+k for k in o.get('scripts',{}).keys()]
            imports=['dependency '+k for k in list(o.get('dependencies',{}).keys())[:MAX_DISPLAY]]
            notes=['Chỉ xuất tên dependency/script; không sao chép giá trị cấu hình.']
        except (ValueError,TypeError,AttributeError):pass
    elif ext in {'.yaml','.yml','.toml','.json'}:
        notes=['Cấu hình tham khảo; dependency/service thực tế cần xác minh bằng call-chain.']
    elif name in {'.env.example','.env.sample','.env.template'}:
        symbols=['variable '+v for v in re.findall(r'(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=',content)]
        notes=['Chỉ ghi tên biến; không sao chép giá trị.']
    return {'status':'SOURCE_INSPECTED_STATIC','purpose':purpose,'symbols':list(dict.fromkeys(symbols)),'imports':list(dict.fromkeys(str(x) for x in imports if x))[:MAX_DISPLAY],'notes':notes}


def classify_path(rel:str)->str:
    p=PurePosixPath(rel); name=p.name.lower(); parts={x.lower() for x in p.parts}
    if re.search(r'(^test_|_test\.|\.test\.|\.spec\.)',name) or {'tests','test','__tests__'} & parts:
        return 'Test/fixture; kiểm chứng hành vi trong phạm vi tương ứng.'
    if name in {'package.json','pyproject.toml','pubspec.yaml','go.mod','cargo.toml','pom.xml','build.gradle','requirements.txt'}:
        return 'Manifest khai báo project/dependency/build tooling.'
    if name.endswith(('.lock','.lockb')) or name in {'package-lock.json','yarn.lock'}:
        return 'Dependency lockfile, đảm bảo tính tái lập của môi trường.'
    if p.suffix.lower() in {'.sql','.prisma'} or 'migrations' in parts:
        return 'Schema/migration/query liên quan tầng dữ liệu; xem quyền truy cập và transaction.'
    if name in {'main.py','main.ts','main.tsx','main.dart','index.js','server.js','app.py'}:
        return 'Ứng viên entrypoint; cần kiểm chứng qua script/bootstrap thực tế.'
    if name.startswith(('view.','views.')):
        return 'Ứng viên view/handler orchestration; xác minh router, service và side effects.'
    if name.startswith(('models.','model.')):
        return 'Ứng viên định nghĩa DTO/schema/domain model.'
    if name.startswith('query.'):
        return 'Ứng viên truy vấn dữ liệu/repository query.'
    if name.startswith(('validate.','validator.')):
        return 'Ứng viên chuẩn hóa/kiểm tra dữ liệu đầu vào và nghiệp vụ.'
    if any(x in parts for x in {'core','shared','common'}):
        return 'Thành phần dùng chung/hạ tầng; xác minh phạm vi tái sử dụng.'
    if any(x in parts for x in {'pages','screens','views','components','ui'}):
        return 'Ứng viên UI/presentation; kiểm tra route, state và action.'
    if 'modules' in parts or 'features' in parts:
        return 'Thành phần trong feature/module; xác minh ownership và contract.'
    if any(x in parts for x in {'docs','documentation'}):
        return 'Tài liệu yêu cầu/thiết kế/tham khảo; không tự chứng minh trạng thái code.'
    if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.svg','.ico','.gif','.mp4','.pdf'}:
        return 'Tài nguyên tĩnh/visual; không kết luận chức năng qua asset.'
    if p.suffix.lower() in {'.html','.css','.scss','.sass'}:
        return 'Giao diện/tạo kiểu; cần đối chiếu component sở hữu.'
    if p.suffix.lower() in {'.py','.ts','.tsx','.js','.jsx','.go','.rs','.java','.kt','.dart','.cs','.rb','.php'}:
        return 'Ứng viên code thực thi; xác minh imports/callers và wiring.'
    return 'Chưa xác định từ tên; phải mở source/metadata khi task liên quan.'


def folder_purpose(rel:str)->str:
    if not rel:return 'Repository root; phạm vi triển khai và các manifest cấu hình.'
    part=PurePosixPath(rel).name.lower()
    mapping={'core':'Hạ tầng/lõi dùng chung theo codebase thực tế','modules':'Nhóm module; mỗi module phải có owner/contract rõ ràng','features':'Nhóm tính năng theo nhu cầu nghiệp vụ','utils':'Hàm tiện ích; tránh đưa business logic sai layer','services':'Dịch vụ tích hợp/use cases (xác nhận theo source)','service':'Dịch vụ tích hợp/use cases (xác nhận theo source)','api':'API/router/transport boundary','routes':'Định tuyến ứng dụng hoặc API','pages':'Trang/screen entry UI','ui':'Thành phần giao diện','components':'Component UI có thể dùng lại','models':'Type/DTO/domain model','data-access':'Gateway/HTTP/repository','repositories':'Repository/data persistence layer','tests':'Kiểm thử và fixture','test':'Kiểm thử và fixture','docs':'Tài liệu và đặc tả','contracts':'Hợp đồng giao tiếp/versioned schemas','migrations':'Lịch sử thay đổi schema dữ liệu','infra':'Hạ tầng vận hành','scripts':'Script tự động hóa','assets':'Tài nguyên phục vụ UI'}
    return mapping.get(part, 'Thư mục do source thực tế khai báo; đọc các file bên dưới để xác định owner.')


def doc_name_for(rel:str):
    n=PurePosixPath(rel).name
    if n.lower()=='readme.md':return 'README.source.md'
    if n.lower()=='readme':return 'README.file.md'
    if n.endswith('.md'):return n[:-3]+'.source.md'
    if n.endswith(('.py','.pyi')):
        candidate=n.rsplit('.',1)[0]+'.md'
        return n+'.md' if candidate=='README.md' else candidate
    return n+'.md'


def map_docs(files:list[str]):
    grouped=defaultdict(list)
    for rel in files:
        path=PurePosixPath(rel)
        doc=doc_name_for(rel)
        grouped[(str(path.parent),doc)].append(rel)
    mappings={}
    for (_,candidate),source_files in grouped.items():
        if len(source_files)==1:
            mappings[source_files[0]]=candidate
        else:
            for source in source_files:
                mappings[source]=PurePosixPath(source).name+'.md'
    docs={}
    for rel in files:
        p=PurePosixPath(rel); out=PurePosixPath('tree')/p.parent/mappings[rel]
        if out in docs:raise ValueError(f'Markdown mapping collision: {out}: {docs[out]}, {rel}')
        docs[out]=rel
    return {v:k.as_posix() for k,v in docs.items()}


def rendered_file_doc(rel:str,info:dict,size:int,sha256:str,has_source:bool):
    def limited(items):
        return ['- `'+str(x).replace('`','')+'`' for x in items] if items else ['- Không phát hiện bằng phân tích tĩnh; cần đọc source khi thực thi.']
    lines=[f'# `{PurePosixPath(rel).name}` — source context','',SENTINEL_START,
           f'**Source:** `{rel}`',f'**Evidence:** `{info["status"]}`; **Size:** {size} bytes; **SHA-256:** `{sha256}`','',
           '## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)','',info['purpose'],'',
           '## Symbol / khai báo phát hiện','',*limited(info['symbols']),'',
           '## Import / phụ thuộc được phát hiện','',*limited(info['imports']),'',
           '## Quan hệ cần xác nhận','',
           '- Caller và route registration: **CHƯA XÁC MINH** (mở router/entrypoint và test liên quan).',
           '- Contract/DB/provider, authz, side effects: **CHƯA XÁC MINH** nếu chưa có bằng chứng runtime.',
           '- Test liên quan: tìm file test, đối chiếu assertions, không coi file tồn tại là test PASS.','',
           '## Ghi chú kiểm tra','',*(('- '+n for n in info['notes']) if info['notes'] else ['- Tránh suy luận nghiệp vụ hoặc chức năng chỉ từ tên file.']),
           SENTINEL_END,'',
           '## Ghi chú bổ sung có xác minh (do agent/người dùng điền)','',
           '- [ ] Đường gọi vào / điều kiện kích hoạt:',
           '- [ ] Luồng xử lý, trạng thái lỗi, auth/permission:',
           '- [ ] DB / API / message contract và test evidence:',
           '']
    return '\n'.join(lines)


def render_folder_doc(rel:str,subdirs:list[str],children:list[tuple[str,str]]):
    lines=[f'# Folder: `{rel or "."}/`','',SENTINEL_START,
           '**Trách nhiệm dự kiến:** '+folder_purpose(rel),'',
           '## Folder con hiện có','']
    if subdirs:lines += ['- [`'+s+'/`]('+quote(s)+'/README.md) — '+folder_purpose((rel+'/' if rel else '')+s) for s in subdirs]
    else:lines+=['- Không có thư mục con trong danh mục source.']
    lines+=['','## File thực tế','']
    if children:lines+=['- [`'+source.replace('`','')+'`]('+quote(doc)+') — '+classify_path((rel+'/' if rel else '')+source) for source,doc in children]
    else:lines+=['- Không có file được chọn.']
    lines += ['', '**Giới hạn:** cây này phản ánh file quan sát được; không suy ra runtime wiring, permission, deployment hay business rule.',SENTINEL_END,'',
              '## Ghi chú owner / dependency có bằng chứng','',
              '- [ ] Owner/feature/module:',
              '- [ ] Entry/caller và quan hệ liên module:',
              '- [ ] DD/contract/test tương ứng:','']
    return '\n'.join(lines)


def merge_generated(old:str,new:str):
    if SENTINEL_START in old and SENTINEL_END in old:
        start=old.index(SENTINEL_START)
        end=old.index(SENTINEL_END,start)+len(SENTINEL_END)
        st=new.index(SENTINEL_START);en=new.index(SENTINEL_END,st)+len(SENTINEL_END)
        # Keep previous header and human annotations outside generated section.
        return old[:start]+new[st:en]+old[end:]
    raise ValueError('Existing document is not kit-managed; refusing overwrite')


def detect_projects(repo:Path,paths:list[str]):
    bybase=defaultdict(set)
    for p in paths:
        q=PurePosixPath(p);bybase[str(q.parent)].add(q.name)
    result=[]
    for folder,names in sorted(bybase.items()):
        markers=sorted(names & {'package.json','pyproject.toml','requirements.txt','pubspec.yaml','Cargo.toml','go.mod','pom.xml','build.gradle','build.gradle.kts','Gemfile','composer.json','.csproj','Dockerfile'})
        if not markers:continue
        tech=[]
        pkg=repo/folder/'package.json'
        if 'package.json' in markers:
            try:
                data=json.loads(pkg.read_text(encoding='utf-8'))
                deps={**data.get('dependencies',{}),**data.get('devDependencies',{})}
                for key,label in [('@angular/core','Angular'),('react','React'),('vue','Vue'),('next','Next.js'),('express','Express'),('fastify','Fastify'),('nestjs','NestJS')]:
                    if key in deps or (label=='NestJS' and '@nestjs/core' in deps):tech.append(label+' (dependency declared)')
            except (ValueError,OSError):pass
        if 'pubspec.yaml' in markers:tech.append('Dart/Flutter candidate')
        if 'go.mod' in markers:tech.append('Go module')
        if 'Cargo.toml' in markers:tech.append('Rust/Cargo module')
        if 'pom.xml' in markers:tech.append('JVM/Maven module')
        if 'pyproject.toml' in markers or 'requirements.txt' in markers:tech.append('Python application/package')
        result.append({'path':folder if folder!='.' else '.', 'manifests':markers, 'signals':tech})
    return result


def file_tree_summary(paths:list[str], max_depth=3):
    dirs=set()
    for p in paths:
        components=PurePosixPath(p).parts[:-1]
        for i in range(1,min(len(components),max_depth)+1):dirs.add('/'.join(components[:i]))
    # show folders, not all thousands of leaf files
    return ['- `'+(p+'/')+'`' for p in sorted(dirs)] or ['- Chưa tìm thấy source.']


def cmd_run(args):
    repo=Path(args.repo).expanduser().resolve()
    if not repo.is_dir():raise ValueError('Repository directory missing: '+str(repo))
    kit=Path(__file__).resolve().parents[2]
    root=kit.parent.resolve()
    if repo!=root and not args.allow_external_repo:
        raise ValueError('Refusing to generate a mirror of a different repository (pass --allow-external-repo only for isolated test/explicit use)')
    out=kit/'project'
    if (out/'SOURCE_MAP.json').exists() and not (args.refresh or args.dry_run or args.check):
        raise ValueError('Source mirror already exists; use --refresh to preserve human notes while updating generated sections')
    paths,mode=select_source_paths(repo)
    physical_dirs=select_source_dirs(repo,mode)
    if not paths:raise ValueError('No source files detected (check Git status/ignore rules)')
    if len(paths)>args.max_files:raise ValueError('Source file count exceeds --max-files budget; choose a scoped repo or raise budget intentionally')
    mapping=map_docs(paths)
    # Determine directory list exactly from observed files; no imposed framework tree.
    directories={''}; dirs_to_files=defaultdict(list);dirs_to_subdirs=defaultdict(set)
    for p in paths:
        pp=PurePosixPath(p);parent='' if str(pp.parent)=='.' else str(pp.parent)
        dirs_to_files[parent].append((pp.name,PurePosixPath(mapping[p]).name))
        parts=pp.parts[:-1]
        for i in range(1,len(parts)+1):
            d='/'.join(parts[:i]);directories.add(d)
            previous='/'.join(parts[:i-1]);dirs_to_subdirs[previous].add(parts[i-1])
    # Include source folders which exist physically even if they have no files.
    for physical in physical_dirs:
        parts=PurePosixPath(physical).parts
        for i in range(1,len(parts)+1):
            d='/'.join(parts[:i]);directories.add(d)
            previous='/'.join(parts[:i-1]);dirs_to_subdirs[previous].add(parts[i-1])
    plan={};items=[]
    for p in paths:
        source=repo/p
        stat=source.stat()
        size=stat.st_size
        if is_sensitive(p):
            info=text_summary(p,b'',args.max_read_bytes)
            digest='REDACTED_SENSITIVE'
        elif size>args.max_read_bytes:
            info={'status':'PATH_ONLY_LARGE','purpose':classify_path(p)+' (file quá lớn để đọc theo budget)','symbols':[],'imports':[],'notes':[]}
            digest='NOT_COMPUTED_LARGE'
        else:
            data=source.read_bytes()
            info=text_summary(p,data,args.max_read_bytes)
            digest=hashlib.sha256(data).hexdigest()
        dest=out/mapping[p]
        plan[dest]=rendered_file_doc(p,info,size,digest,True)
        items.append({'source':p,'document':mapping[p],'status':info['status'],'sha256':digest,'size':size,'mtimeNs':stat.st_mtime_ns})
    for folder in sorted(directories):
        md=out/'tree'/folder/'README.md'
        plan[md]=render_folder_doc(folder,sorted(dirs_to_subdirs[folder]),sorted(dirs_to_files[folder]))
    revision=(run_git(repo,'rev-parse','HEAD') or b'').decode('ascii',errors='replace').strip() or 'NO_GIT_COMMIT'
    projects=detect_projects(repo,paths)
    map_file=out/'SOURCE_MAP.json'
    prev_data=json.loads(map_file.read_text(encoding='utf-8')) if map_file.is_file() else {}
    prev_items={x['source']:x for x in prev_data.get('files',[])}
    new_items={x['source']:x for x in items}
    previous_dirs=set(prev_data.get('folders',[]))
    current_dirs=set(directories)
    added_folders=sorted(current_dirs-previous_dirs)
    removed_folders=sorted(previous_dirs-current_dirs)
    added=sorted(set(new_items)-set(prev_items))
    removed=sorted(set(prev_items)-set(new_items))
    def source_changed(new,old):
        stable=(new['sha256'],new['size'],new['document']) != (old['sha256'],old['size'],old['document'])
        if stable:return True
        if new['sha256'] in {'REDACTED_SENSITIVE','NOT_COMPUTED_LARGE'}:
            return new.get('mtimeNs') != old.get('mtimeNs')
        return False
    changed=sorted(p for p in new_items.keys() & prev_items.keys()
                   if source_changed(new_items[p],prev_items[p]))
    now=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    branch=(run_git(repo,'branch','--show-current') or b'').decode('utf8',errors='replace').strip() or 'NO_BRANCH'
    status_raw=run_git(repo,'status','--porcelain','--untracked-files=normal')
    git_dirty_lines=[x for x in (status_raw or b'').decode('utf8',errors='replace').splitlines()
                     if x.strip() and not x[3:].startswith('.agents/')] 
    delta={'added':len(added),'modified':len(changed),'removed':len(removed)}
    map_data={'schemaVersion':'1.1.0','method':mode,'gitCommit':revision,'gitBranch':branch,
              'lastSyncUTC':now,'sourceFileCount':len(paths),'sourceFolderCount':len(directories),
              'dirtyFileCount':len(git_dirty_lines),'projectSignals':projects,'delta':delta,'folders':sorted(directories),'files':items}
    if args.check:
        if not prev_data:
            print('STALE: project/ has not been initialized; run build-context.py',file=sys.stderr)
            return 1
        if added or removed or changed or added_folders or removed_folders or prev_data.get('gitCommit')!=revision:
            print(f'STALE: project context differs from source: +{len(added)}, ~{len(changed)}, -{len(removed)}, '+
                  f'folders +{len(added_folders)}/-{len(removed_folders)}, HEAD={revision}; run build-context.py --refresh')
            for p in (added+changed+removed)[:args.preview]:
                print(' -',p)
            return 1
        print(f'CURRENT: project context matches selected source ({len(paths)} files, HEAD {revision}). '+
              'Runtime/behavior not verified by this check.')
        return 0
    if args.dry_run:
        print(f'DRY-RUN: {len(paths)} file docs, {len(directories)} folder docs, {len(projects)} package candidates; '+
              f'delta=+{len(added)}/~{len(changed)}/-{len(removed)}, folders +{len(added_folders)}/-{len(removed_folders)}; source={mode}; no writes')
        for x in items[:args.preview]: print(f'  {x["source"]} -> {x["document"]} [{x["status"]}]')
        return 0
    summary=['# Project structure — generated from this repository','',
             f'- Source files: **{len(paths)}**; source directories: **{len(directories)}**',
             f'- Scan: `{mode}`; git HEAD: `{revision}`',
             '- Độ tin cậy: **PATH_VERIFIED** cho file tồn tại; **SOURCE_INSPECTED_STATIC** khi phân tích tĩnh; không khẳng định wiring/runtime.',
             '- File-level docs trong [`tree/`](tree/README.md); ánh xạ đường dẫn trong [`SOURCE_MAP.json`](SOURCE_MAP.json).','',
             '## Cấu trúc thư mục cấp cao (tối đa 3 tầng)','',*file_tree_summary(paths,3),'',
             '## Ứng viên deployable/package từ manifest','']
    if projects:
        for project in projects:
            summary.append(f'- `{project["path"]}`: `{", ".join(project["manifests"])}`; tín hiệu: {", ".join(project["signals"]) or "chưa nhận diện"}')
    else:summary.append('- Không có manifest chuẩn được phát hiện; khảo sát thủ công.')
    summary += ['', '## Cần agent xác minh trước coding','',
                '- [ ] Entry/bootstrap và router registration','- [ ] Boundary client/server/worker/module','- [ ] DB/schema/API/event contracts thực tế',
                '- [ ] Quy tắc bảo mật và quyền dữ liệu','- [ ] Lệnh test/build thực sự được chạy','']
    summary_txt='\n'.join(summary)
    project_txt='\n'.join(['# Project profile — generated candidate','',
             f'- Status: `GENERATED_NEEDS_REVIEW`',f'- Git commit: `{revision}`',f'- Scan mode: `{mode}`',
             f'- Files/folders: {len(paths)}/{len(directories)}',
             '- Stack / deployables: candidates only, see [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md).',
             '- Requirement/BD/DD authority: inspect actual repository documents; not assumed.',
             '- Routes/entrypoints, persistence, authz, integration, CI: `NOT_VERIFIED` until traced.',
             '- Commands that were run: source inventory only; no application tests/deploy.',
             '', '## Project-specific context (complete after examining source)', '',
             '| Concern | Verified facts + path evidence | Status |','|---|---|---|',
             '| Repository ownership | TBD | UNVERIFIED |','| Client/API/worker entrypoints | TBD | UNVERIFIED |',
             '| Modules and boundaries | TBD | UNVERIFIED |','| Contracts and database | TBD | UNVERIFIED |',
             '| Security / authorization | TBD | UNVERIFIED |','| Test/build commands | TBD | NOT_RUN |',''])
    # Refuse *all* writes if any target would overwrite an unmanaged document.
    for target,rendered in plan.items():
        if target.exists() and target.read_text(encoding='utf-8')!=rendered:
            merge_generated(target.read_text(encoding='utf-8'),rendered)
    # Important: a new filename can claim a Markdown path formerly owned by
    # another source (e.g. view.py -> view.md, then an extensionless view added).
    # Never merge another file's human notes into the new file. Preserve them.
    previous_doc_owners={item['document']:item['source'] for item in prev_items.values()}
    reassigned=[]
    for item in items:
        other=previous_doc_owners.get(item['document'])
        if other and other!=item['source']:
            previous_path=out/item['document']
            if previous_path.is_file():reassigned.append(previous_path)
    archive_root=out/'archive'/now.replace(':','-').replace('+','_')
    def archive_managed_doc(file_path:Path):
        if not file_path.is_file():return False
        if not file_path.resolve().is_relative_to((out/'tree').resolve()):
            raise ValueError('Refusing archive outside project tree: '+str(file_path))
        if SENTINEL_START not in file_path.read_text(encoding='utf8'):
            raise ValueError('Refusing archive of unmanaged project document: '+str(file_path))
        dest=archive_root/file_path.relative_to(out)
        dest=dest.with_suffix(dest.suffix+'.txt')
        dest.parent.mkdir(parents=True,exist_ok=True)
        suffix=1
        while dest.exists():
            dest=dest.with_name(dest.name.rsplit('.txt',1)[0]+f'.{suffix}.txt')
            suffix+=1
        shutil.move(str(file_path),str(dest))
        return True
    archived_reassigned=sum(archive_managed_doc(path) for path in reassigned)
    errors=[];created=updated=unchanged=0
    for path,text in plan.items():
        path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists():
            old=path.read_text(encoding='utf-8')
            if old!=text:
                try: merged=merge_generated(old,text)
                except ValueError as ex:
                    errors.append(f'{path.relative_to(kit)}: {ex}');continue
                if merged!=old:
                    path.write_text(merged,encoding='utf-8',newline='\n');updated+=1
                else:unchanged+=1
            else:unchanged+=1
        else:
            path.write_text(text,encoding='utf-8',newline='\n');created+=1
    if errors:
        for e in errors:print('ERROR:',e,file=sys.stderr)
        raise ValueError('Some source mirrors conflict with pre-existing unmanaged docs; resolve before refreshing index')
    # The source map is committed only after mirror pages are generated successfully.
    (out/'SOURCE_MAP.json').write_text(json.dumps(map_data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    structure=out/'PROJECT_STRUCTURE.md'
    summary_block=SENTINEL_START+'\n'+summary_txt+'\n'+SENTINEL_END
    if structure.exists():
        old_structure=structure.read_text(encoding='utf-8')
        if SENTINEL_START in old_structure and SENTINEL_END in old_structure:
            updated_structure=merge_generated(old_structure,summary_block)
            if updated_structure!=old_structure:structure.write_text(updated_structure,encoding='utf-8')
        elif 'NOT GENERATED' in old_structure:
            structure.write_text('# Project structure — source map of target repository\n\n'+summary_block+'\n\n## Verified architecture decisions (manual)\n\n- [ ] Source-backed owner/caller notes.\n',encoding='utf-8')
        else:
            raise ValueError('PROJECT_STRUCTURE.md is not managed; refusing overwrite')
    else:
        structure.write_text('# Project structure — source map of target repository\n\n'+summary_block+'\n\n## Verified architecture decisions (manual)\n\n- [ ] Source-backed owner/caller notes.\n',encoding='utf-8')
    by_evidence=defaultdict(int)
    for item in items:by_evidence[item['status']]+=1
    coverage=['# Source coverage summary','',
              f'- Source files mapped: **{len(paths)}**; source folders documented: **{len(directories)}**',
              f'- Scan method: `{mode}`; Git HEAD: `{revision}`',
              '- Every scanned source file has one Markdown document; binary/secret/large files are metadata-only.',
              '- Source evidence is static; routing/behavior/test/deployment remains UNVERIFIED until checked separately.','',
              '| Evidence status | Files |','|---|---:|']
    coverage += [f'| `{kind}` | {num} |' for kind,num in sorted(by_evidence.items())]
    coverage_block=SENTINEL_START+'\n'+'\n'.join(coverage)+'\n'+SENTINEL_END
    coverage_path=out/'COVERAGE.md'
    if coverage_path.exists():
        old_coverage=coverage_path.read_text(encoding='utf-8')
        if SENTINEL_START in old_coverage and SENTINEL_END in old_coverage:
            updated_coverage=merge_generated(old_coverage,coverage_block)
            if updated_coverage!=old_coverage:coverage_path.write_text(updated_coverage,encoding='utf-8')
        else:
            raise ValueError('COVERAGE.md is not managed; refusing overwrite')
    else:
        coverage_path.write_text('# Source mirror coverage — target repository\n\n'+coverage_block+'\n',encoding='utf-8')
    profile=out/'PROJECT.md'
    profile_block=SENTINEL_START+'\n'+'\n'.join([
        '- **Snapshot:** `SOURCE_SCANNED_NEEDS_REVIEW`.',
        f'- **HEAD:** `{revision}`; **branch:** `{branch}`; **sync UTC:** `{now}`.',
        f'- **Source files:** `{len(paths)}`; **source folders:** `{len(directories)}`.',
        '- **Runtime/entrypoints/auth/data/deployment:** `NOT_VERIFIED` — cần xác nhận qua code và test.',
        '- **Đọc tiếp:** [trạng thái](STATE.md), [cây thư mục](PROJECT_STRUCTURE.md), [bản đồ file](SOURCE_MAP.json).'
    ])+'\n'+SENTINEL_END
    if profile.exists():
        content=profile.read_text(encoding='utf8')
        profile.write_text(merge_generated(content,profile_block),encoding='utf8')
    else:
        profile.write_text('# Project profile — actual repository\n\n'+profile_block+
                           '\n\nverification_status: UNREVIEWED\n\n## Verified facts (manual)\n\n- [ ] Entrypoints/contracts/tests evidenced by actual source.\n',encoding='utf8')
    state=out/'STATE.md'
    state_block=SENTINEL_START+'\n'+'\n'.join([
        f'- **Last sync (UTC):** `{now}`',
        f'- **Repository HEAD:** `{revision}`; **branch:** `{branch}`; **scan mode:** `{mode}`',
        f'- **Files/folders:** `{len(paths)}` / `{len(directories)}`',
        f'- **Changed since previous sync:** files added `{len(added)}`, modified `{len(changed)}`, removed `{len(removed)}`; folders added `{len(added_folders)}`, removed `{len(removed_folders)}`',
        f'- **Git dirty entries (observed):** `{len(git_dirty_lines)}` (không hiển thị dữ liệu nhạy cảm)',
        '- **Source index:** [SOURCE_MAP.json](SOURCE_MAP.json); [source tree](tree/README.md).',
        '- **Application runtime/test/deployment:** `NOT_VERIFIED` / `NOT_RUN` trừ khi bổ sung bằng chứng thủ công.',
    ])+'\n'+SENTINEL_END
    if state.exists():
        state.write_text(merge_generated(state.read_text(encoding='utf8'),state_block),encoding='utf8')
    else:state.write_text('# Project state (live scan snapshot)\n\n'+state_block+
                          '\n\n## Open questions / verified task status (manual)\n\n- Chưa được xác minh.\n',encoding='utf8')
    log=out/'CHANGES.md'
    if not log.exists():
        log.write_text('# Project context changes\n\n<!-- PROJECT_CHANGE_HISTORY -->\n',encoding='utf8')
    def limited_names(seq):
        clean=[p for p in seq if not is_sensitive(p)]
        return ', '.join('`'+p.replace('`','')+'`' for p in clean[:15]) or 'không có đường dẫn công khai'
    log_text='\n'.join([
        f'\n### {now} — `{revision[:12]}` ({mode})',
        f'- Files: `{len(paths)}`, dirs: `{len(directories)}`; delta `+{len(added)} / ~{len(changed)} / -{len(removed)}`; folders `+{len(added_folders)} / -{len(removed_folders)}`.',
        f'- Added: {limited_names(added)}.',
        f'- Modified: {limited_names(changed)}.',
        f'- Removed: {limited_names(removed)}.',
        '- Source inspection only; no build/test/deploy was performed by sync script.',''
    ])
    old_log=log.read_text(encoding='utf8')
    if added or changed or removed or added_folders or removed_folders or not prev_data or prev_data.get('gitCommit')!=revision:
        log.write_text(old_log.rstrip()+'\n'+log_text+'\n',encoding='utf8')
    # Archive obsolete kit-managed docs while keeping their notes available;
    # project/tree/ remains an accurate mirror of the current scanned structure.
    old_targets={out/ent['document'] for ent in prev_items.values()}
    old_dirs={out/'tree'/folder/'README.md' for folder in previous_dirs if folder}
    for ent in prev_items.values():
        parts=PurePosixPath(ent['source']).parts[:-1]
        old_dirs.update(out/'tree'/Path(*parts[:i])/'README.md' for i in range(1,len(parts)+1))
    old_dirs.add(out/'tree'/'README.md')
    obsolete=(old_targets|old_dirs)-set(plan)
    archived=archived_reassigned
    for old_doc in sorted(obsolete):
        if old_doc.is_file():archived+=int(archive_managed_doc(old_doc))
    for folder in sorted((out/'tree').rglob('*'),key=lambda x:len(x.parts),reverse=True):
        if folder.is_dir():
            try:folder.rmdir()  # only truly empty folders, no removal of user files
            except OSError:pass
    print(f'Archived outdated project mirror docs: {archived} (human notes preserved).')
    print(f'CONTEXT BUILT: {len(paths)} source -> {len(paths)} file docs; {len(directories)} README dirs; files created={created}, updated={updated}, unchanged={unchanged}; mode={mode}')
    return 0


def main():
    ap=argparse.ArgumentParser(description='Universal source-to-Markdown context builder (no framework lock-in)')
    ap.add_argument('--repo',default=str(Path(__file__).resolve().parents[3]),help='Repository root; default parent of .agents')
    ap.add_argument('--dry-run',action='store_true',help='Preview scan without any writes')
    ap.add_argument('--check',action='store_true',help='Read-only drift check vs last source snapshot; returns 1 on stale context')
    ap.add_argument('--refresh',action='store_true',help='Regenerate managed sections; preserve manual notes in per-file docs')
    ap.add_argument('--refresh-project',action='store_true',help='Explicitly overwrite PROJECT.md scaffold (review first)')
    ap.add_argument('--allow-external-repo',action='store_true',help='Explicit override for test or external checkout; writes to kit location only')
    ap.add_argument('--max-files',type=int,default=25000)
    ap.add_argument('--max-read-bytes',type=int,default=256000)
    ap.add_argument('--preview',type=int,default=8)
    ns=ap.parse_args()
    if ns.check and (ns.dry_run or ns.refresh):ap.error('--check cannot be combined with --dry-run or --refresh')
    try:return cmd_run(ns)
    except (ValueError,OSError) as err:
        print('ERROR:',err,file=sys.stderr)
        return 2

if __name__=='__main__':sys.exit(main())
