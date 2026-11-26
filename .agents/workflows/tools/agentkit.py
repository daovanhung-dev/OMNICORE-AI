#!/usr/bin/env python3
"""Universal Agent Kit: verify registry, validate docs, scaffold DD, build source context.

No project-specific paths/frameworks; uses Python standard library only.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[2]
REPO=ROOT.parent
REGISTRY=ROOT/'workflows'/'registry.json'
NAME=re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,99}\Z')
MD_LINK=re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')


def load_json(path:Path):return json.loads(path.read_text(encoding='utf-8'))


def inside(target:Path,root:Path):
    target=target.resolve()
    if not target.is_relative_to(root.resolve()):raise ValueError('path escapes allowed root: '+str(target))
    return target


def validate(strict_profile:bool=False):
    errors=[];warnings=[]
    try:
        reg=load_json(REGISTRY)
        inv=load_json(ROOT/reg['skillsInventory'])
    except (ValueError,OSError,KeyError) as err:
        print('ERROR: invalid registry/inventory:',err);return 2
    if reg.get('schemaVersion')!='9.0.0':errors.append('invalid registry schemaVersion')
    needed=set(reg.get('required',[]))|{reg['rootRouter'],reg['projectProfile'],reg['skillsInventory'],reg['skillIntegrity']}
    for k in ('architecture','workflows'):
        needed.update(reg.get(k,{}).values())
    for name,spec in reg.get('skills',{}).items():
        needed.add(spec['entry']);needed.update(spec.get('resources',[]))
        if spec.get('workflow') not in reg.get('workflows',{}):errors.append('unknown workflow for skill '+name)
    for typ,spec in reg.get('templates',{}).items():
        needed.update(str(Path(spec['dir'])/s) for s in spec['files'])
    for item in sorted(needed):
        try:target=inside(ROOT/item,ROOT)
        except ValueError as err:errors.append(str(err));continue
        if not target.is_file():errors.append('missing registry file: '+item)
    actual_skills={p.relative_to(ROOT/'skills').as_posix() for p in (ROOT/'skills').rglob('*') if p.is_file() and p.name not in {'inventory.json','INTEGRITY.md'} and '__pycache__' not in p.parts}
    listed={e['file'] for e in inv.get('files',[])}
    if actual_skills!=listed:errors.append(f'skill inventory mismatch: missing={sorted(listed-actual_skills)}, unexpected={sorted(actual_skills-listed)}')
    if len(listed)!=inv.get('count'):errors.append('skill file count mismatch')
    for item in inv.get('files',[]):
        p=ROOT/'skills'/item['file']
        if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
            errors.append('skill SHA-256 mismatch: '+item['file'])
    skill_dirs={p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')}
    if skill_dirs!=set(reg.get('skills',{})):errors.append('skill entry/registry mismatch')
    documents=[p for p in ROOT.rglob('*.md') if not p.is_relative_to(ROOT/'skills-original')]
    for doc in documents:
        try:contents=doc.read_text(encoding='utf-8')
        except UnicodeError:errors.append('invalid UTF-8 MD '+str(doc));continue
        if not contents.endswith('\n'):errors.append('missing newline: '+str(doc.relative_to(ROOT)))
        for line in MD_LINK.findall(contents):
            link=line.strip().split(' "',1)[0].strip('<>')
            if not link or link.startswith(('http:','https:','mailto:','data:','#')) or any(p in link for p in ('__ID__','{{','TBD')):continue
            target=unquote(link.split('#',1)[0].split('?',1)[0])
            if not target or target.startswith('/'):continue
            try:linked=inside(doc.parent/target,ROOT)
            except ValueError:errors.append('escaping Markdown link: '+str(doc.relative_to(ROOT))+' -> '+link);continue
            if not linked.exists():errors.append('broken Markdown link: '+str(doc.relative_to(ROOT))+' -> '+link)
    # Reference example integrity is separate from actual project source mirror.
    # The one-API/one-screen count here constrains only the distributed example.
    try:
        ref=reg.get('referenceTemplate',{})
        ex=load_json(ROOT/ref['manifest'])
        cfg=load_json(ROOT/ref['config'])
        api=ex['apiExamples'];screens=ex['screenExamples'];examples=ex['examples']
        if ex.get('mode')!='TEMPLATE_ONLY' or cfg.get('mode')!='TEMPLATE_ONLY':
            errors.append('reference manifest must be TEMPLATE_ONLY')
        if len(api)!=ref.get('apiCount') or len(screens)!=ref.get('screenCount'):
            errors.append('reference API/Screen example count mismatch')
        if len(examples)!=ref.get('exampleFileCount') or len(set(examples.values()))!=len(examples):
            errors.append('reference source Markdown mapping count/collision')
        for original,relative in examples.items():
            if not original.startswith('apps/') or not relative.startswith('apps/'):
                errors.append('reference source path outside apps: '+original);continue
            try:document=inside(ROOT/'architecture'/relative,ROOT/'architecture')
            except ValueError:
                errors.append('reference path escapes architecture: '+relative);continue
            if not document.is_file():errors.append('missing example Markdown: '+relative)
        for folder in (ROOT/'architecture'/'apps').rglob('*'):
            if folder.is_dir() and not (folder/'README.md').is_file():
                errors.append('missing example folder README: '+str(folder.relative_to(ROOT)))
    except (OSError,ValueError,KeyError,TypeError) as exc:
        errors.append('invalid reference template: '+str(exc))
    profile=(ROOT/reg['projectProfile']).read_text(encoding='utf-8')
    map_file=ROOT/'project'/'SOURCE_MAP.json'
    if map_file.is_file():
        try:
            data=load_json(map_file)
            if len(data['files'])!=data['sourceFileCount']:
                errors.append('SOURCE_MAP file count discrepancy')
            seen=set()
            for ent in data['files']:
                source=ent['source'];dest=ent['document']
                if source in seen:errors.append('duplicate source map entry: '+source)
                seen.add(source)
                try:destpath=inside(ROOT/'project'/dest,ROOT/'project')
                except ValueError:errors.append('map path escapes architecture: '+dest);continue
                if not destpath.is_file():errors.append('missing mirrored Markdown '+dest)
                try:
                    sourcepath=inside(REPO/source,REPO)
                    if sourcepath.exists() and sourcepath.is_symlink():errors.append('symlink source should be omitted: '+source)
                except ValueError:errors.append('source path escapes root: '+source)
            parentdirs=set()
            for ent in data['files']:
                parts=Path(ent['source']).parts[:-1]
                for depth in range(1,len(parts)+1):parentdirs.add(Path(*parts[:depth]))
            for folder in parentdirs:
                if not (ROOT/'project'/'tree'/folder/'README.md').is_file():
                    errors.append('missing project folder README: '+str(folder))
            for label in ('STATE.md','CHANGES.md','PROJECT_STRUCTURE.md','COVERAGE.md'):
                if not (ROOT/'project'/label).is_file():errors.append('missing project summary: '+label)
        except (ValueError,KeyError,TypeError) as err:errors.append('invalid SOURCE_MAP: '+str(err))
    else:
        (errors if strict_profile else warnings).append('project source mirror not initialized; run build-context.py')
    manual_profile=profile.split('<!-- AUTO_CONTEXT_END -->',1)[-1]
    if not re.search(r'(?m)^verification_status:\s*SOURCE_REVIEWED\s*$',manual_profile):
        (errors if strict_profile else warnings).append('PROJECT.md needs source-backed review and completion')
    routing=load_json(ROOT/'routing.json')
    refs=set(routing['common'])
    for name,task in routing['tasks'].items():
        refs.update([task['workflow'],*task['context'],*task['skills'],*task.get('original_skills',[])])
        if name not in reg['workflows'] or task['workflow']!=reg['workflows'][name]:errors.append('Tuyến không khớp registry: '+name)
    for ref in sorted(refs):
        try:
            if not inside(ROOT/ref,ROOT).is_file():errors.append('Thiếu tài nguyên định tuyến: '+ref)
        except ValueError:errors.append('Đường dẫn không an toàn: '+ref)
    manifest=load_json(ROOT/'context-manifest.json')
    for ref in manifest['tools'].values():
        try:
            if not inside(ROOT/ref,ROOT).is_file():errors.append('Thiếu công cụ: '+ref)
        except ValueError:errors.append('Đường dẫn không an toàn: '+ref)
    original_check=subprocess.run([sys.executable,str(ROOT/'tools'/'import-original-skills.py'),'--check'],check=False)
    if original_check.returncode==2:warnings.append('Bản skill gốc chưa đủ; chưa nghiệm thu kế thừa toàn bộ')
    elif original_check.returncode!=0:errors.append('Kiểm định skill gốc thất bại')
    print(f"Định tuyến: {len(routing['tasks'])}; đường dẫn: {len(refs)}")
    print(f'Kiểm định bộ tác nhân: skills={len(reg.get("skills",{}))}; resources={len(listed)}; workflows={len(reg.get("workflows",{}))}; Markdown={len(documents)}')
    for e in errors:print('LỖI:',e)
    for w in warnings:print('CẢNH BÁO:',w)
    print('KẾT QUẢ:','FAIL' if errors else 'PASS'+(' (có cảnh báo khởi tạo)' if warnings else ''))
    return 1 if errors else 0


def new_dd(kind:str,id:str,slug:str,output:str):
    if not NAME.fullmatch(id) or not NAME.fullmatch(slug):
        print('ERROR: unsafe ID/slug',file=sys.stderr);return 2
    reg=load_json(REGISTRY)
    spec=reg.get('templates',{}).get(kind)
    if not spec:print('ERROR: unknown DD type',file=sys.stderr);return 2
    try:
        base=Path(output).expanduser()
        if not base.is_absolute():base=REPO/base
        base=inside(base,REPO)
        dest=inside(base/(id+'-'+slug),REPO)
    except ValueError as err:print('LỖI:',err,file=sys.stderr);return 2
    if dest.exists() or dest.is_symlink():
        print('ERROR: destination already exists: '+str(dest),file=sys.stderr);return 1
    docs=[]
    for file in spec['files']:
        src=inside(ROOT/spec['dir']/file,ROOT)
        if not src.is_file():print('ERROR: missing template '+str(src),file=sys.stderr);return 2
        txt=src.read_text(encoding='utf-8').replace('__ID__',id).replace('__SLUG__',slug).replace('__DATE__',dt.date.today().isoformat())
        docs.append((file,txt))
    dest.mkdir(parents=True,exist_ok=False)
    for file,txt in docs:
        p=dest/file;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(txt,encoding='utf-8',newline='\n')
    print(f'CREATED: {dest} ({len(docs)} tệp DD khởi tạo, yêu cầu chưa xác minh)')
    return 0


def validate_dd(kind:str,path:str,strict:bool=False):
    spec=load_json(REGISTRY).get('templates',{}).get(kind)
    if not spec:print('ERROR: unknown DD type',file=sys.stderr);return 2
    dest=Path(path).expanduser()
    if not dest.is_absolute():dest=REPO/dest
    errors=[];warnings=[]
    for f in spec['files']:
        p=dest/f
        if not p.is_file():errors.append('missing: '+f);continue
        t=p.read_text(encoding='utf-8')
        if not t.strip() or not t.endswith('\n'):errors.append('empty or no newline: '+f)
        if re.search(r'\bTBD\b|__ID__|__SLUG__|NOT_YET_REVIEWED',t):
            (errors if strict else warnings).append('placeholder: '+f)
    print(f'DD validate: type={kind}, path={dest}; needed={len(spec["files"])}')
    for x in errors:print('LỖI:',x)
    for x in warnings:print('CẢNH BÁO:',x)
    print('KẾT QUẢ:','FAIL' if errors else 'PASS'+(' (cảnh báo nội dung chưa xác minh)' if warnings else ''))
    return 1 if errors else 0


def recent_worklogs(task_type:str,limit:int):
    folder=ROOT/'worklog'
    found=[]
    if folder.is_dir():
        for p in folder.glob('*/*.md'):
            try:contents=p.read_text(encoding='utf-8')[:1200]
            except UnicodeError:continue
            x=re.search(r'^primary_task_type:\s*[\'\"]?([\w-]+)',contents,re.M)
            if x and x.group(1)==task_type:found.append(p)
    if not found:print('NONE: no matching worklog')
    else:
        for p in sorted(found,reverse=True)[:max(0,limit)]:print(p.relative_to(ROOT))
    return 0


def main():
    parser=argparse.ArgumentParser(description='Công cụ điều phối tác nhân')
    subs=parser.add_subparsers(dest='cmd',required=True)
    p=subs.add_parser('validate');p.add_argument('--strict-profile',action='store_true')
    for op in ('new-dd','validate-dd'):
        p=subs.add_parser(op)
        p.add_argument('--type',choices=['api','screen','module'],required=True)
        p.add_argument('--template',choices=['adapted','original'],default='adapted')
        if op=='new-dd':
            for x in ('id','slug','output'):p.add_argument('--'+x,required=True)
        else:
            p.add_argument('--path',required=True);p.add_argument('--strict',action='store_true')
    p=subs.add_parser('scan-source',help='Alias to generic source-to-Markdown builder')
    p.add_argument('--dry-run',action='store_true');p.add_argument('--refresh',action='store_true');p.add_argument('--check',action='store_true')
    p=subs.add_parser('recent-worklogs');p.add_argument('--type',required=True);p.add_argument('--limit',type=int,default=3)
    args=parser.parse_args()
    if args.cmd=='validate':return validate(args.strict_profile)
    if args.cmd=='new-dd':
        if args.template=='original':
            sys.path.insert(0,str(ROOT/'engines'))
            from template_adapter import create_dd
            if not NAME.fullmatch(args.id) or not NAME.fullmatch(args.slug):return 2
            try:
                dest=inside(REPO/args.output/(args.id+'-'+args.slug),REPO)
                print(create_dd(ROOT,args.type,'original',dest));return 0
            except (ValueError,OSError) as e:print(e);return 1
        return new_dd(args.type,args.id,args.slug,args.output)
    if args.cmd=='validate-dd':
        if args.template=='original':
            sys.path.insert(0,str(ROOT/'engines'))
            from template_adapter import verify_dd
            try:
                result=verify_dd(ROOT,args.type,inside(REPO/args.path,REPO),'original');print(json.dumps(result,ensure_ascii=False));return int(bool(result['issues']))
            except (ValueError,OSError) as e:print(e);return 1
        return validate_dd(args.type,args.path,args.strict)
    if args.cmd=='recent-worklogs':return recent_worklogs(args.type,args.limit)
    if args.cmd=='scan-source':
        command=[sys.executable,str(ROOT/'workflows'/'tools'/'build-context.py')]
        if args.dry_run:command.append('--dry-run')
        if args.refresh:command.append('--refresh')
        if args.check:command.append('--check')
        return subprocess.run(command,cwd=REPO,check=False).returncode
    return 2

if __name__=='__main__':sys.exit(main())
