#!/usr/bin/env python3
"""Kiểm tra từng byte của thư viện gốc theo danh mục hai nguồn."""
import argparse, hashlib, json, sys
from pathlib import Path
A=Path(__file__).resolve().parents[1]
def verify(root=A):
    m=json.loads((root/'original-skills.json').read_text()); d=root/'skills-original'
    expected=m['files']; actual={p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file() or p.is_symlink()}
    errors=[]
    if actual!=set(expected):errors.append(f"Thiếu={sorted(set(expected)-actual)}; thừa={sorted(actual-set(expected))}")
    if len(expected)!=m['expected_count']:errors.append('Số tệp không khớp')
    for rel,v in expected.items():
        p=d/rel
        if not p.resolve().is_relative_to(d.resolve()) or p.is_symlink() or not p.is_file():errors.append(rel);continue
        b=p.read_bytes();h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        if hashlib.sha256(b).hexdigest()!=v['sha256'] or h!=v['git_blob'] or len(b)!=v['size']:errors.append('Sai hash: '+rel)
    for k,rel in m['routing'].items():
        if rel not in expected:errors.append('Thiếu điểm vào: '+k)
    return errors,len(expected)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true',required=True);p.parse_args()
    errs,n=verify();print(f'Kiểm định skill gốc: {n} tệp; '+('FAIL' if errs else 'PASS'))
    for e in errs:print(e,file=sys.stderr)
    sys.exit(bool(errs))
