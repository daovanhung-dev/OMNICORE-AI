#!/usr/bin/env python3
"""Static symbol inventory; no execution or secret/body extraction."""
import argparse, ast, json, pathlib, re, subprocess, hashlib, os, collections
SKIP={'.git','.agents','node_modules','dist','build','.venv','venv','__pycache__','.angular','.next','.dart_tool','vendor','target','coverage'}
EXT={'.py','.pyi','.ts','.tsx','.js','.jsx','.mjs','.cjs','.dart','.go','.rs','.cs','.java','.kt','.swift','.rb','.php','.vue','.svelte','.sql','.html','.css','.scss','.json','.yaml','.yml','.toml','.md','.sh'}
def files(root):
 try:
  raw=subprocess.check_output(['git','-C',str(root),'ls-files','-z','--cached','--others','--exclude-standard'],stderr=subprocess.DEVNULL)
  names=sorted(set(os.fsdecode(x) for x in raw.split(b'\0') if x))
 except (OSError,subprocess.CalledProcessError):
  names=[]
  for b,dirs,fs in os.walk(root,followlinks=False):
   dirs[:]=[d for d in dirs if d not in SKIP and not (pathlib.Path(b)/d).is_symlink()]
   names.extend((pathlib.Path(b)/f).relative_to(root).as_posix() for f in fs)
 for n in names:
  p=pathlib.PurePosixPath(n); f=root/n
  if p.is_absolute() or '..' in p.parts or any(x in SKIP for x in p.parts) or not f.is_file() or f.is_symlink() or not f.resolve().is_relative_to(root):continue
  yield n,f
def py_symbols(text):
 t=ast.parse(text); out=[]
 class Visitor(ast.NodeVisitor):
  def __init__(self):self.prefix=[]
  def declaration(self,n):
   row={'name':'.'.join([*self.prefix,n.name]),'kind':type(n).__name__,'line':n.lineno,'end_line':n.end_lineno}
   if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
    a=n.args; args=[*a.posonlyargs,*a.args,*a.kwonlyargs]+([a.vararg] if a.vararg else [])+([a.kwarg] if a.kwarg else [])
    row['parameters']=[{'name':x.arg,'type':ast.unparse(x.annotation) if x.annotation else None} for x in args];row['return_type']=ast.unparse(n.returns) if n.returns else None
   out.append(row);self.prefix.append(n.name);self.generic_visit(n);self.prefix.pop()
  visit_ClassDef=declaration
  visit_FunctionDef=declaration
  visit_AsyncFunctionDef=declaration
 Visitor().visit(t);return out

def ts_batch(inputs):
 if not inputs:return []
 try:
  result=subprocess.run(['node',str(pathlib.Path(__file__).with_name('parse-typescript.cjs'))],input=json.dumps(inputs),text=True,capture_output=True,timeout=120,check=True)
  return json.loads(result.stdout)
 except (OSError,subprocess.SubprocessError,ValueError):
  return [{'path':x['path'],'status':'PARSER_UNAVAILABLE','symbols':[],'imports':[],'calls':[]} for x in inputs]

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,default=pathlib.Path('.'));ns=p.parse_args();root=ns.repo.resolve();out=root/'.agents/project';out.mkdir(parents=True,exist_ok=True)
 rows=[]; folders=collections.defaultdict(list); ts_inputs=[]
 for name,f in files(root):
  row={'path':name,'status':'PATH_ONLY','symbols':[]};folders[str(pathlib.PurePosixPath(name).parent)].append(name)
  sensitive=f.name.startswith('.env') or f.name.lower() in {'credentials.json','service-account.json','id_rsa','id_ed25519','.npmrc'} or f.suffix.lower() in {'.pem','.key','.p12','.pfx','.jks','.keystore'}
  if sensitive:row['status']='PATH_ONLY_SENSITIVE'
  elif f.suffix.lower() in EXT and f.stat().st_size<=1000000:
   try:
    b=f.read_bytes(); t=b.decode('utf8');row['sha256']=hashlib.sha256(b).hexdigest()
    if f.suffix in {'.py','.pyi'}:row['symbols']=py_symbols(t);row['status']='STATIC_AST'
    elif f.suffix in {'.ts','.tsx','.js','.jsx','.mjs','.cjs'}:ts_inputs.append({'path':name,'text':t});row['status']='PENDING_PARSER'
    elif f.suffix in {'.dart','.go','.rs','.cs','.java','.kt','.swift','.rb','.php','.vue','.svelte'}:row['status']='PARSER_UNAVAILABLE'
    else:row['status']='TEXT_PATH_ONLY'
   except (UnicodeError,SyntaxError,OSError):row['status']='PARSE_BLOCKED'
  rows.append(row)
 by_path={r['path']:r for r in rows}
 for i in range(0,len(ts_inputs),100):
  for parsed in ts_batch(ts_inputs[i:i+100]):
   row=by_path[parsed['path']];row['status']=parsed['status'];row['symbols']=parsed['symbols'];row['imports']=parsed['imports']
 target=out/'SYMBOL_INVENTORY.json';temp=target.with_suffix('.tmp');temp.write_text(json.dumps({'schema':1,'warning':'Chỉ khai báo tĩnh; không chứng minh hành vi. Ngôn ngữ chưa có bộ phân tích được ghi rõ.','folders':dict(folders),'files':rows},ensure_ascii=False,indent=2)+'\n');temp.replace(target)
 print(f'{len(rows)} files; {sum(len(r["symbols"]) for r in rows)} static symbols; {target}')
if __name__=='__main__':main()
