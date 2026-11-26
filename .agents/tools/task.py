#!/usr/bin/env python3
"""Điều phối phiên V11: tải nguồn, kế hoạch DAG, kiểm tra đăng ký, nghiệm thu có receipt."""
import argparse,sys,json
from pathlib import Path
A=Path(__file__).resolve().parents[1];sys.path.insert(0,str(A/'engines'))
from session import Engine,policies
from context import getplan

def main():
    p=argparse.ArgumentParser(description=__doc__);subs=p.add_subparsers(dest='cmd',required=True)
    for cmd in ['plan','begin','declare','load','target','start','check','verify','reopen','block','resume','status','finish','conflict','resolve','sync']:
        q=subs.add_parser(cmd)
        if cmd!='sync':q.add_argument('route' if cmd in {'begin','plan'} else 'id')
        for arg in {'begin':['id','title'],'declare':['path','section','reason'],'target':['key','name','accept'],'check':['key','kind'],'verify':['key'],'reopen':['key'],'block':['reason'],'finish':['summary'],'conflict':['description'],'resolve':['decision']}.get(cmd,[]):q.add_argument('--'+arg,required=True)
        if cmd=='load':q.add_argument('--path')
        if cmd=='target':
            for x in ['deps','checks','paths']:q.add_argument('--'+x,nargs='*',default=[])
        if cmd=='check':q.add_argument('--params',default='{}')
    x=p.parse_args();e=Engine(A)
    try:
        if x.cmd=='plan':r=getplan(A,x.route);r['gates']=policies(A)[x.route]
        elif x.cmd=='begin':r=e.begin(x.route,x.id,x.title)
        elif x.cmd=='declare':r=e.declare(x.id,x.path,x.section,x.reason)
        elif x.cmd=='load':r=e.load(x.id,x.path)
        elif x.cmd=='target':r=e.target(x.id,x.key,x.name,x.accept,x.deps,x.checks,x.paths)
        elif x.cmd=='check':r=e.check(x.id,x.key,x.kind,json.loads(x.params))
        elif x.cmd=='status':r=e.current(x.id)
        elif x.cmd=='verify':r=e.verify(x.id,x.key)
        elif x.cmd=='reopen':r=e.reopen(x.id,x.key)
        elif x.cmd=='block':r=e.block(x.id,x.reason)
        elif x.cmd=='conflict':r=e.conflict(x.id,x.description)
        elif x.cmd=='resolve':r=e.resolve(x.id,x.decision)
        elif x.cmd=='finish':r=e.finish(x.id,x.summary)
        elif x.cmd=='sync':r=e.sync()
        else:r=getattr(e,x.cmd)(x.id)
        if isinstance(r,dict):print(json.dumps(r,ensure_ascii=False,indent=2))
        else:print('Đã ghi trạng thái.')
    except Exception as err:print('LỖI:',err,file=sys.stderr);return 1
    return 0
if __name__=='__main__':sys.exit(main())
