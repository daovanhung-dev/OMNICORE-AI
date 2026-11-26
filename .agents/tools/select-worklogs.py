#!/usr/bin/env python3
import argparse,re,pathlib
p=argparse.ArgumentParser();p.add_argument('--type',required=True);p.add_argument('--limit',type=int,default=3);args=p.parse_args()
base=pathlib.Path(__file__).resolve().parents[1]/'worklog'
rows=[]
for f in base.glob('????-??-??/*.md'):
 if f.is_symlink():continue
 with f.open(encoding='utf8') as stream: header=stream.read(1024).split('---',2)
 if len(header)>2 and re.search(r'^primary_task_type:\s*'+re.escape(args.type)+r'\s*$',header[1],re.M):rows.append(f)
rows.sort(key=lambda f:f.as_posix());rows.sort(key=lambda f:f.parent.name,reverse=True)
for f in rows[:max(0,args.limit)]:print(f.relative_to(base.parent.parent))
