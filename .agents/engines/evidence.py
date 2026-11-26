"""Các adapter kiểm tra cục bộ; không chấp nhận argv tùy ý hoặc exit 0 đơn thuần."""
import json, subprocess, sys, tempfile, hashlib, xml.etree.ElementTree as ET, os, ast
import re
from pathlib import Path
from context import safe, digest, canonical

def run(argv, cwd, timeout=180, env=None):
    p=subprocess.run(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout,env=env)
    return p.returncode,p.stdout

def junit(path):
    root=ET.parse(path).getroot(); cases=list(root.iter('testcase'))
    passed=[x for x in cases if not any(x.find(k) is not None for k in ('failure','error','skipped'))]
    if not cases or len(passed)!=len(cases):raise ValueError('JUnit không có ca thực thi thành công đầy đủ')
    return {'cases':len(cases),'passed':len(passed),'tests':[x.get('classname','')+'::'+x.get('name','') for x in cases]}

def in_scope(root,path,scopes):
    rel=Path(canonical(root,path))
    return any(rel==Path(x) or Path(x) in rel.parents for x in scopes)

def scoped_coverage(root,cwd,report,scopes,tests,source_root):
    """Chứng minh ca chạy thực sự chạm thân hàm trong mã app thuộc target; không chứng minh ý nghĩa assertion."""
    data=json.loads(report.read_text()); hits={}; accepted=set()
    for name,info in data.get('files',{}).items():
        p=(cwd/name).resolve()
        if not p.is_relative_to(source_root) or not p.is_file() or not in_scope(root,p.relative_to(root).as_posix(),scopes):continue
        tree=ast.parse(p.read_text(encoding='utf8'));body=set()
        for node in ast.walk(tree):
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
                for stmt in node.body:
                    if isinstance(stmt,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) or (isinstance(stmt,ast.Expr) and isinstance(stmt.value,ast.Constant) and isinstance(stmt.value.value,str)):continue
                    body.update(range(stmt.lineno,stmt.end_lineno+1))
        for line,contexts in info.get('contexts',{}).items():
            if int(line) not in body:continue
            for ctx in contexts:
                if not ctx.endswith('|run'):continue
                nodeid=ctx[:-4]; parts=nodeid.split('::'); module=parts[0].removesuffix('.py').replace('/','.')
                test=module+'::'+'::'.join(parts[1:])
                # JUnit biểu diễn class bằng dấu chấm; chuẩn hóa cả class methods.
                if len(parts)>2:test=module+'.'+'.'.join(parts[1:-1])+'::'+parts[-1]
                if test in tests:accepted.add(test);hits.setdefault(p.relative_to(root).as_posix(),set()).add(int(line))
    if not accepted:raise ValueError('Không có ca test thực thi thân hàm ứng dụng trong phạm vi target')
    return sorted(accepted),{k:sorted(v) for k,v in hits.items()}

def inspect_check(root,a,kind,params,scopes=None):
    if not scopes:raise ValueError('Thiếu phạm vi target')
    def require_scope(path):
        if not in_scope(root,path,scopes):raise ValueError('Sản phẩm nằm ngoài phạm vi target: '+str(path))

    py=sys.executable; out=b''; artifacts={}; details={}; code=0
    if kind in {'api-test','regression','integration','migration'}:
        cwd=safe(root,params.get('cwd','backend')); selector=params.get('tests','tests')
        sel=selector.split('::')[0]; path=safe(cwd,sel)
        if sel.startswith('-') or not sel:raise ValueError('Selector sai')
        if not path.exists() or not (path.is_dir() or path.suffix=='.py'):raise ValueError('Thiếu tệp/thư mục test Python')
        if kind in {'regression','integration','migration'} and (not path.is_file() or '::' not in selector):raise ValueError('Cần chọn ca test cụ thể theo target')
        coverage_source=params.get('coverage_source','app')
        if not isinstance(coverage_source,str) or not re.fullmatch(r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*',coverage_source):raise ValueError('coverage_source sai')
        source_root=(cwd/Path(*coverage_source.split('.'))).resolve()
        if not source_root.is_relative_to(cwd) or not source_root.exists():raise ValueError('Không tìm thấy package nguồn trong cwd')
        with tempfile.TemporaryDirectory() as t:
            xml=Path(t)/'report.xml'; coverage_json=Path(t)/'coverage.json'
            env=dict(os.environ,COVERAGE_FILE=str(Path(t)/'.coverage'))
            code,out=run([py,'-m','pytest','-q',selector,'--junitxml='+str(xml),'--cov='+coverage_source,'--cov-context=test','--cov-report='],cwd,env=env)
            if code or not xml.is_file():raise ValueError(f'pytest thất bại, exit={code}')
            details=junit(xml);details['report_sha256']=digest(xml)
            covcode,_=run([py,'-m','coverage','json','--show-contexts','-o',str(coverage_json)],cwd,env=env)
            if covcode or not coverage_json.is_file():raise ValueError('Thiếu báo cáo coverage theo ca')
            details['scoped_tests'],details['executed_source']=scoped_coverage(root,cwd,coverage_json,scopes,details['tests'],source_root)
            details['coverage_sha256']=digest(coverage_json);details['semantic_review']='HUMAN_REQUIRED'
    elif kind=='contract':
        p=safe(root,params['path']); j=json.loads(p.read_text())
        req=j.get('requirements',[])
        if not req or not j.get('decision_source'):raise ValueError('Thiếu yêu cầu hoặc nguồn quyết định')
        decision=safe(root,j['decision_source'])
        if not decision.is_file() or not decision.stat().st_size:raise ValueError('Thiếu tài liệu quyết định')
        artifacts[j['decision_source']]=digest(decision); ids=set()
        for r in req:
            if not r.get('id') or r['id'] in ids or not r.get('expected') or not r.get('source') or not r.get('tests'):raise ValueError('Truy vết yêu cầu chưa đủ')
            ids.add(r['id']); src=safe(root,r['source'])
            if not src.is_file() or not src.stat().st_size:raise ValueError('Thiếu nguồn yêu cầu')
            artifacts[r['source']]=digest(src)
            for name in r['tests']:
                if not isinstance(name,str) or '::' not in name:raise ValueError('Cần ID ca test cụ thể (module::test)')
        artifacts[p.relative_to(root).as_posix()]=digest(p); details={'requirements':len(req),'expected_tests':sorted({x for r in req for x in r['tests']}),'semantic_review':'HUMAN_REQUIRED'}
    elif kind=='architecture':
        argv=[py,str(a/'validators/validate_architecture.py'),'--backend',str(safe(root,params.get('backend','backend')))]
        backend_only=params.get('backend_only',False)
        if not isinstance(backend_only,bool):raise ValueError('backend_only phải là boolean')
        if backend_only:
            package=params.get('backend_package','app')
            if not isinstance(package,str) or not re.fullmatch(r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*',package):raise ValueError('backend_package sai')
            argv.extend(['--backend-package',package])
            allow_empty_modules=params.get('allow_empty_modules',False)
            if not isinstance(allow_empty_modules,bool):raise ValueError('allow_empty_modules phải là boolean')
            if allow_empty_modules:argv.append('--allow-empty-modules')
        else:
            argv.extend(['--frontend',str(safe(root,params.get('frontend','frontend')))])
        code,out=run(argv,root)
        details=json.loads(out); 
        if code or details.get('status')!='PASS_STATIC':raise ValueError('Kiểm định kiến trúc thất bại')
    elif kind=='context':
        code,out=run([py,str(a/'workflows/tools/build-context.py'),'--check'],root)
        if code or not (a/'project/SOURCE_MAP.json').is_file():raise ValueError('Context chưa đồng bộ')
        artifacts['.agents/project/SOURCE_MAP.json']=digest(a/'project/SOURCE_MAP.json')
    elif kind=='build':
        cwd=safe(root,params.get('cwd','frontend'))
        require_scope(cwd.relative_to(root).as_posix())
        runtime=params.get('runtime','typescript')
        if runtime=='python-uv':
            package=params.get('package')
            if not isinstance(package,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*',package):raise ValueError('Tên package Python sai')
            with tempfile.TemporaryDirectory(prefix='codex-python-build-') as output_dir:
                code,out=run(['uv','build','--package',package,'--wheel','--out-dir',output_dir],root)
                wheels=list(Path(output_dir).glob('*.whl'))
                if code or len(wheels)!=1:raise ValueError('Build Python không sinh đúng một wheel')
                details={'package':package,'wheel':wheels[0].name,'wheel_sha256':digest(wheels[0])}
        elif runtime=='typescript':
            code,out=run(['tsc','--project','tsconfig.json'],cwd)
            if code or not (cwd/'dist/main.js').is_file():raise ValueError('Build không sinh dist/main.js')
            artifacts[(cwd/'dist/main.js').relative_to(root).as_posix()]=digest(cwd/'dist/main.js')
        else:raise ValueError('Runtime build chưa được hỗ trợ: '+str(runtime))
    elif kind in {'fe-test','browser'}:
        cwd=safe(root,params.get('cwd','frontend'))
        require_scope(cwd.relative_to(root).as_posix())
        # Adapter kiểm chứng đúng nền TypeScript kèm kit; không tự chạy npm script dự án lạ.
        if kind=='browser':
            raise ValueError('Chưa có adapter trình duyệt kiểm chứng độc lập; ghi BLOCKED')
        code,out=run(['tsc','--project','tsconfig.json'],cwd)
        if code:raise ValueError('Biên dịch FE thất bại')
        code,out=run(['node','--test','--test-reporter=tap','tests/model_check.mjs'],cwd)
        tests=re.search(rb'^# tests (\d+)$',out,re.M); passed=re.search(rb'^# pass (\d+)$',out,re.M)
        if code or not tests or not passed or int(tests[1])==0 or tests[1]!=passed[1]:raise ValueError('Thiếu TAP hoặc ca test thất bại')
        details={'cases':int(tests[1]),'passed':int(passed[1]),'tests':['node::'+x.decode() for x in re.findall(rb'^ok \d+ - ([^\r\n]+)$',out,re.M)],'semantic_review':'HUMAN_REQUIRED'}
    elif kind.startswith('dd-'):
        from template_adapter import verify_dd
        require_scope(params['path'])
        if canonical(root,params['path']) not in scopes:raise ValueError('DD phải trùng thư mục sản phẩm đã đăng ký trong target')
        if params.get('deliverable')!='draft':raise ValueError('Chỉ nghiệm thu cấu trúc DD với deliverable=draft; phê duyệt nghiệp vụ độc lập')
        details=verify_dd(a,kind[3:],safe(root,params['path']),params.get('template','original'))
        if details['issues']:raise ValueError('DD chưa đạt: '+'; '.join(details['issues'][:5]))
        for p in safe(root,params['path']).rglob('*'):
            if p.is_file() and not p.is_symlink():artifacts[p.relative_to(root).as_posix()]=digest(p)
    elif kind=='utc':
        require_scope(params['spec']);require_scope(params['workbook'])
        spec=safe(root,params['spec']); workbook=safe(root,params['workbook']); base=a/'skills-original/utc-screen-skill/scripts'
        with tempfile.TemporaryDirectory() as t:
            report=Path(t)/'report.json'; generated=Path(t)/'utc.xlsx'
            code,out=run([py,str(base/'kiem_tra_utc.py'),'--input',str(spec),'--report',str(report)],root)
            if code or not report.exists():raise ValueError('Kiểm định UTC thất bại')
            details=json.loads(report.read_text()); data=json.loads(spec.read_text())
            if not details.get('du_dieu_kien_phe_duyet') and params.get('deliverable')!='plan':raise ValueError('UTC chưa đủ điều kiện phê duyệt; chỉ nghiệm thu kế hoạch với deliverable=plan')
            if not data.get('test_cases',data.get('testcases',data.get('cases',[]))):raise ValueError('UTC không có ca kiểm thử')
            code,out=run([py,str(base/'kiem_tra_excel.py'),'--input',str(workbook)],root)
            if code:raise ValueError('Excel UTC không hợp lệ')
            # Không chứng minh workbook được sinh từ spec chỉ bằng sự tồn tại; tạo lại và đối chiếu nội dung ô.
            code,out=run([py,str(base/'tao_utc.py'),'--input',str(spec),'--output',str(generated)],root)
            if code:raise ValueError('Không tái tạo được UTC')
            from openpyxl import load_workbook
            def cells(p):
                w=load_workbook(p,read_only=True,data_only=False)
                return [(s.title,list(s.values)) for s in w]
            if cells(generated)!=cells(workbook):raise ValueError('Workbook không khớp đặc tả tái tạo')
        artifacts={p.relative_to(root).as_posix():digest(p) for p in (spec,workbook)}
    elif kind=='review-report':
        # Chỉ đọc; kiểm tra cấu trúc và vị trí tham chiếu, không tự tuyên bố đúng ngữ nghĩa.
        require_scope(params['path'])
        p=safe(root,params['path']); j=json.loads(p.read_text());
        if not p.is_relative_to(a/'review-reports'):raise ValueError('Báo cáo review phải ở .agents/review-reports')
        if not j.get('scope') or not j.get('limits') or j.get('tests_run') is not False or not isinstance(j.get('findings'),list):raise ValueError('Thiếu hợp đồng review')
        for f in j['findings']:
            src=safe(root,f['file']); line=f['line']
            if not isinstance(line,int) or not 1<=line<=len(src.read_text().splitlines()) or not f.get('impact') or not f.get('evidence'):raise ValueError('Phát hiện thiếu vị trí hoặc bằng chứng')
        artifacts[p.relative_to(root).as_posix()]=digest(p); details={'findings':len(j['findings']),'semantic_review':'HUMAN_REQUIRED'}
    else:raise ValueError('Adapter chưa được triển khai: '+kind+'; không nghiệm thu giả')
    return {'kind':kind,'details':details,'artifacts':artifacts,'output_sha256':hashlib.sha256(out).hexdigest()}
