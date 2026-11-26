from pathlib import Path
import json, hashlib

def getplan(a,route):
    r=json.loads((a/'routing.json').read_text()); spec=r['tasks'][route]
    paths=list(dict.fromkeys(r['common']+[spec['workflow']]+spec['context']+spec['skills']+spec.get('original_skills',[])))
    reg=json.loads((a/'workflows/registry.json').read_text())
    for skill in reg['skills'].values():
        if skill['entry'] in spec['skills']:
            paths.extend(x for x in skill['resources'] if '/examples/' not in x and '/vi-du/' not in x)
    paths.extend(['engines/policies.json','engines/evidence.py','engines/context.py','engines/session.py','engines/planning.py','engines/template_adapter.py','validators/validate_architecture.py'])
    paths=list(dict.fromkeys(paths))
    if spec.get('original_skills'):
        m=json.loads((a/'original-skills.json').read_text())
        for entry in spec['original_skills']:
            group=entry.split('/')[1]
            for rel in sorted(m['files']):
                if not rel.startswith(group+'/'):continue
                tail=rel[len(group)+1:]
                if (group=='create_dd_api' and '/DD_API_Template_MD/' in '/'+tail) or (group=='create_dd_screen' and tail.startswith(('00-GUIDES/','01-TEMPLATES/'))) or (group=='create-dd-mobile' and tail.startswith(('references/','template/','checklists/')) and not tail.startswith('references/11-')) or (group=='utc-screen-skill' and tail.startswith(('huong-dan/','schema/','mau/'))) or (group=='code-review' and tail.startswith('references/')):
                    paths.append('skills-original/'+rel)
        paths=list(dict.fromkeys(paths))
    for p in paths:
        if not (a/p).resolve().is_relative_to(a.resolve()) or not (a/p).is_file():raise ValueError('Tài nguyên không tồn tại: '+p)
    typ='review' if 'review' in route else ('fix' if route=='fix' else ('test' if route.startswith(('test','utc')) else ('docs' if route.startswith(('dd','requirement','update-context','worklog')) else 'coding')))
    if not (a.parent/'AGENTS.md').is_file():raise ValueError('Thiếu AGENTS.md gốc')
    return {'route':route,'primary_task_type':typ,'paths':['AGENTS.md']+['.agents/'+p for p in paths],'original_skills':spec.get('original_skills',[])}


def safe(root, rel):
    p=root/rel
    if Path(rel).is_absolute() or not p.resolve().is_relative_to(root.resolve()) or any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(root)):
        raise ValueError('Đường dẫn không an toàn: '+str(rel))
    return p.resolve()

def canonical(root,rel):
    return safe(root,rel).relative_to(root.resolve()).as_posix()

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def snapshot(root):
    # Không băm secret, dependency, build, nhật ký hoặc dữ liệu DB.
    skip={'.git','.agents','node_modules','dist','build','__pycache__','.pytest_cache','.venv','venv','.next','coverage'}
    out={}
    import os
    for base, dirs, names in os.walk(root,followlinks=False):
        dirs[:]=sorted(d for d in dirs if d not in skip and not (Path(base)/d).is_symlink())
        for n in sorted(names):
            p=Path(base)/n
            if p.is_symlink() or n.startswith('.env') or p.suffix.lower() in {'.db','.sqlite','.sqlite3','.pem','.key','.pyc','.log'}:continue
            if p.is_file():out[p.relative_to(root).as_posix()]=digest(p)
    return out
