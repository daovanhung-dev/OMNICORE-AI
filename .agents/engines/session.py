"""Kho trạng thái cục bộ SQLite; các thao tác trạng thái dùng transaction và khóa ghi."""
import sqlite3,json,datetime as dt,re,os,tempfile,sys
from pathlib import Path
from contextlib import contextmanager
from context import getplan,safe,digest,snapshot,canonical
from planning import order
from evidence import inspect_check
ID=re.compile(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z')
HEADER='| STT | Tên target | Tiến độ hoàn thiện |\n|---:|---|---:|\n'

def plain(s):
    if not s or any(x in s for x in '\r\n|'):raise ValueError('Giá trị một dòng, không chứa dấu phân cách bảng')
    return s

def atomic(p,s):
    p.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf8',dir=p.parent,delete=False) as f:f.write(s);tmp=f.name
    os.replace(tmp,p)

def policies(a):return json.loads((a/'engines/policies.json').read_text())
class Engine:
    def __init__(self,a):self.a=a.resolve();self.root=self.a.parent;self.db=self.a/'sessions/state.sqlite3'
    @contextmanager
    def tx(self):
        self.db.parent.mkdir(exist_ok=True)
        db=sqlite3.connect(self.db,timeout=30);db.execute('PRAGMA foreign_keys=ON');db.execute('PRAGMA busy_timeout=30000')
        try:
            db.execute('BEGIN IMMEDIATE');db.execute('CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
            yield db;db.commit()
        except BaseException:db.rollback();raise
        finally:db.close()
    def read(self,db,id):
        row=db.execute('SELECT payload FROM sessions WHERE id=?',(id,)).fetchone()
        if not row:raise ValueError('Phiên không tồn tại')
        return json.loads(row[0])
    def save(self,db,s):
        db.execute('INSERT INTO sessions VALUES (?,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload',(s['id'],json.dumps(s,ensure_ascii=False)))
    def project(self,db):
        rows=[]
        for _,data in db.execute('SELECT id,payload FROM sessions ORDER BY id'):
            s=json.loads(data)
            for k,t in s['targets'].items():
                if not t.get('done'):rows.append((s['id']+': '+k+' '+t['name'],t['progress']))
            # Worklog là projection phục hồi được; không lưu nội dung nguồn hoặc stdout nhạy cảm.
            lines=['---','primary_task_type: '+s['type'],'route: '+s['route'],'session_id: '+s['id'],'---','# '+s['title'],'','Trạng thái: '+s['state'],'','## READ_PLAN']
            lines += [f"- `{p}` — {x['reason']} — {x.get('sha256','CHƯA ĐỌC')}" for p,x in s['sources'].items()]
            lines += ['', '## PRIOR_WORKLOG_REVIEW',f"Đã chọn {len(s['prior'])}/3; nhận xét ngữ nghĩa cần agent xác minh.",'','## LEAF_TARGET_PLAN']
            lines += [f"- {k}: {t['name']} — {t['accept']} — {t['progress']}% — {'Đạt cổng cấu trúc' if t.get('done') else 'Chưa đạt'}" for k,t in s['targets'].items()]
            lines += ['', '## TARGET_UPDATES','```json',json.dumps(s['events'],ensure_ascii=False,indent=2),'```','','## Kiểm tra','```json',json.dumps(s['checks'],ensure_ascii=False,indent=2),'```','','## Kết thúc',s.get('summary','Chưa nghiệm thu.')]
            if s['state']=='COMPLETED':lines+=['SESSION_CLOSED: true','ACCEPTANCE_LEVEL: MECHANICAL_ONLY','SEMANTIC_REVIEW: HUMAN_REQUIRED']
            atomic(self.a/'worklog'/s['day']/(s['id']+'.md'),'\n'.join(lines)+'\n')
        atomic(self.a/'target.md',HEADER+''.join(f'| {i} | {n} | {v}% |\n' for i,(n,v) in enumerate(rows,1)))
    def sync(self):
        with self.tx() as db:self.project(db)
    def begin(self,route,id,title):
        if not ID.fullmatch(id):raise ValueError('Mã phiên không hợp lệ')
        plain(title);p=getplan(self.a,route);prior=[]
        for f in sorted((self.a/'worklog').glob('????-??-??/*.md'),reverse=True):
            if f.is_symlink():continue
            if re.search(r'^primary_task_type:\s*'+re.escape(p['primary_task_type'])+r'\s*$',f.read_text()[:1024],re.M):prior.append(f.relative_to(self.root).as_posix())
            if len(prior)==3:break
        with self.tx() as db:
            if db.execute('SELECT 1 FROM sessions WHERE id=?',(id,)).fetchone() or list((self.a/'worklog').glob('????-??-??/'+id+'.md')):raise ValueError('Phiên trùng')
            s={'id':id,'route':route,'type':p['primary_task_type'],'title':title,'day':dt.date.today().isoformat(),'state':'CREATED','sources':{x:{'reason':'Nguồn bắt buộc','section':'toàn bộ'} for x in p['paths']+prior},'prior':prior,'targets':{},'checks':{},'events':[], 'baseline':snapshot(self.root),'blocked':None,'conflicts':[]}
            self.save(db,s)
        self.sync();return s
    def current(self,id):
        with self.tx() as db:return self.read(db,id)
    def mutate(self,id,fn):
        with self.tx() as db:
            s=self.read(db,id)
            if s['state']=='COMPLETED':raise ValueError('Phiên đã đóng')
            result=fn(s,db);self.save(db,s)
        self.sync();return result
    def declare(self,id,path,section,reason):
        path=canonical(self.root,path);plain(path);plain(section);plain(reason)
        def f(s,db):
            if path not in s['sources']:s['sources'][path]={'section':section,'reason':reason};s['state']='CREATED'
        self.mutate(id,f)
    def load(self,id,path=None):
        def f(s,db):
            names=list(s['sources']) if path is None else [canonical(self.root,path)]
            for name in names:
                if name not in s['sources']:raise ValueError('Chưa khai báo nguồn')
                p=safe(self.root,name)
                if not p.is_file():raise ValueError('Thiếu nguồn: '+name)
                s['sources'][name]['sha256']=digest(p)
            if all(x.get('sha256') for x in s['sources'].values()) and not s['conflicts']:s['state']='PLANNED' if s['targets'] else 'CONTEXT_READY'
        self.mutate(id,f)
    def conflict(self,id,description):
        plain(description)
        self.mutate(id,lambda s,db:(s['conflicts'].append(description),s.update(state='BLOCKED')))
    def resolve(self,id,decision):
        plain(decision)
        def f(s,db):
            if not s['conflicts']:raise ValueError('Không có mâu thuẫn')
            s['events'].append({'resolved_conflicts':s['conflicts'],'decision':decision});s['conflicts']=[];s['state']='CREATED'
        self.mutate(id,f)
    def fresh(self,s):
        if s['conflicts']:raise ValueError('Còn mâu thuẫn nguồn')
        for name,x in s['sources'].items():
            p=safe(self.root,name)
            if not p.is_file() or x.get('sha256')!=digest(p):raise ValueError('Nguồn chưa nạp hoặc lỗi thời: '+name)
    def target(self,id,key,name,accept,deps,checks,paths):
        if not ID.fullmatch(key):raise ValueError('ID target sai')
        plain(name);plain(accept)
        def f(s,db):
            self.fresh(s)
            if s['state'] not in {'CONTEXT_READY','PLANNED'}:raise ValueError('Chưa sẵn sàng lập kế hoạch')
            if key in s['targets']:raise ValueError('Target trùng')
            if not checks or len(set(checks))!=len(checks) or not set(checks)<=set(policies(self.a)[s['route']]):raise ValueError('Target cần loại kiểm tra đã đăng ký theo tuyến')
            if not paths:raise ValueError("Phải khai báo phạm vi sản phẩm hoặc mã nguồn")
            scopes=list(dict.fromkeys(canonical(self.root,p) for p in paths))
            if "." in scopes:raise ValueError("Phạm vi gốc quá rộng; khai báo thư mục hoặc tệp cụ thể")
            # Phạm vi khai báo không trùng với target mở ở phiên khác; chỉ là khóa hợp tác.
            for _,data in db.execute('SELECT id,payload FROM sessions WHERE id<>?',(id,)):
                other=json.loads(data)
                if other['state']=='COMPLETED':continue
                for t in other['targets'].values():
                    if any(Path(x)==Path(y) or Path(x) in Path(y).parents or Path(y) in Path(x).parents for x in scopes for y in t['paths']):raise ValueError('Tài nguyên đang được phiên khác giữ')
            s['targets'][key]={'name':name,'accept':accept,'deps':deps,'kinds':checks,'paths':scopes,'progress':0,'done':False,'receipts':{}}
            s['state']='PLANNED'
        self.mutate(id,f)
    def start(self,id):
        def f(s,db):
            self.fresh(s);order(s['targets'])
            if not s['targets'] or set(policies(self.a)[s['route']])-set(k for t in s['targets'].values() for k in t['kinds']):raise ValueError('Kế hoạch chưa phủ các cổng bắt buộc')
            if s['state']!='PLANNED':raise ValueError('Cần lập kế hoạch trước')
            s['state']='IN_PROGRESS'
        self.mutate(id,f)
    def check(self,id,key,kind,params):
        s=self.current(id);self.fresh(s)
        if s['state'] not in {'IN_PROGRESS','VERIFYING'}:raise ValueError('Phiên chưa bắt đầu hoặc đang blocked')
        t=s['targets'][key]
        if t['done'] or kind not in t['kinds'] or any(not s['targets'][d]['done'] for d in t['deps']):raise ValueError('Target không đúng thứ tự hoặc loại kiểm tra')
        if s['type']=='review' and kind!='review-report':raise ValueError('Review chỉ đọc')
        before=snapshot(self.root)
        try:
            if kind=='contract':
                contract=params.get('path','')
                if contract not in s['sources']:raise ValueError('Contract chưa được khai báo/nạp')
                cj=json.loads(safe(self.root,contract).read_text())
                for name in [cj.get('decision_source','')]+[x.get('source','') for x in cj.get('requirements',[])]:
                    if not name or name not in s['sources']:raise ValueError('Nguồn quyết định/yêu cầu chưa được nạp')
            receipt=inspect_check(self.root,self.a,kind,params,scopes=t['paths'])
            receipt.update(target=key,session=id,scope=t['paths'])
            after=snapshot(self.root)
            if before!=after:raise ValueError('Source đổi trong khi chạy kiểm tra')
            receipt.update(source=after,params=params,status='PASS')
        except Exception as e:
            receipt={'status':'FAIL','kind':kind,'error':str(e)}
        def f(state,db):
            if state['state'] not in {'IN_PROGRESS','VERIFYING'} or state['targets'][key]['done']:raise ValueError('Trạng thái thay đổi khi kiểm tra')
            state['checks'][key+'/'+kind]=receipt;state['targets'][key]['receipts'][kind]=receipt
            state['targets'][key]['progress']=int(99*sum(x.get('status')=='PASS' for x in state['targets'][key]['receipts'].values())/len(t['kinds']))
            state['state']='VERIFYING'
        self.mutate(id,f)
        if receipt['status']!='PASS':raise ValueError(receipt['error'])
        return {k:v for k,v in receipt.items() if k!='source'}
    def valid_receipt(self,r,now,session,target,scope):
        if r.get('status')!='PASS' or r.get('source')!=now or r.get('session')!=session or r.get('target')!=target or r.get('scope')!=scope:return False
        return all(safe(self.root,p).is_file() and digest(safe(self.root,p))==sha for p,sha in r.get('artifacts',{}).items())
    def verify(self,id,key):
        def f(s,db):
            self.fresh(s);t=s['targets'][key];now=snapshot(self.root)
            if s['state'] not in {'IN_PROGRESS','VERIFYING'} or any(not s['targets'][x]['done'] for x in t['deps']):raise ValueError('Chưa đến lượt target')
            if any(not self.valid_receipt(t['receipts'].get(k,{}),now,s['id'],key,t['paths']) for k in t['kinds']):raise ValueError('Thiếu bằng chứng hợp lệ hoặc đã lỗi thời')
            t.update(done=True,progress=99);s['events'].append({'verified':key,'kinds':t['kinds']})
        self.mutate(id,f)
    def reopen(self,id,key):
        def f(s,db):
            if key not in s['targets']:raise ValueError('Không có target')
            todo={key}
            while True:
                more={k for k,t in s['targets'].items() if set(t['deps'])&todo}
                if more<=todo:break
                todo|=more
            for k in todo:s['targets'][k].update(done=False,progress=0,receipts={})
            s['state']='IN_PROGRESS';s['events'].append({'reopened':sorted(todo)})
        self.mutate(id,f)
    def block(self,id,reason):
        plain(reason);self.mutate(id,lambda s,db:s.update(state='BLOCKED',blocked=reason))
    def resume(self,id):
        def f(s,db):
            if s['state']!='BLOCKED' or s['conflicts']:raise ValueError('Phiên không thể phục hồi')
            self.fresh(s);s['blocked']=None;s['state']='PLANNED' if s['targets'] else 'CONTEXT_READY'
        self.mutate(id,f)
    def finish(self,id,summary):
        plain(summary)
        def f(s,db):
            self.fresh(s);now=snapshot(self.root);order(s['targets'])
            if s['state'] not in {'IN_PROGRESS','VERIFYING'} or not s['targets'] or any(not t['done'] for t in s['targets'].values()):raise ValueError('Còn target chưa xác minh')
            for key,t in s['targets'].items():
                if any(not self.valid_receipt(t['receipts'].get(k,{}),now,s['id'],key,t['paths']) for k in t['kinds']):raise ValueError('Bằng chứng lỗi thời; mở lại target')
            if set(policies(self.a)[s['route']])-set(k for t in s['targets'].values() for k in t['kinds']):raise ValueError('Thiếu cổng bắt buộc')
            if 'contract' in policies(self.a)[s['route']]:
                for key,t in s['targets'].items():
                    if 'contract' not in t['receipts']:continue
                    descendants={key}
                    while True:
                        next_ids={k for k,v in s['targets'].items() if set(v['deps'])&descendants}
                        if next_ids<=descendants:break
                        descendants|=next_ids
                    expected=set(t['receipts']['contract']['details']['expected_tests'])
                    observed={x for k in descendants for r in s['targets'][k]['receipts'].values() for x in r['details'].get('scoped_tests',[])}
                    if expected-observed:raise ValueError('Thiếu ca kiểm thử theo phạm vi và truy vết target '+key+': '+', '.join(sorted(expected-observed)))
            if s['type']=='review':
                report={p for t in s['targets'].values() for r in t['receipts'].values() for p in r.get('artifacts',{})}
                if {p:v for p,v in now.items() if p not in report}!={p:v for p,v in s['baseline'].items() if p not in report}:raise ValueError('Review đã thay đổi source')
            s.update(state='COMPLETED',summary=summary,acceptance_level='MECHANICAL_ONLY',semantic_review='HUMAN_REQUIRED')
        self.mutate(id,f)
