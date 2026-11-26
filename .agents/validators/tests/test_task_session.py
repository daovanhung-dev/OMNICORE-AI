import unittest,tempfile,shutil,sys,json,subprocess,concurrent.futures
from unittest.mock import patch
from pathlib import Path
A=Path(__file__).resolve().parents[2];sys.path.insert(0,str(A/'engines'))
from session import Engine,policies
from context import getplan
from evidence import inspect_check
from template_adapter import create_dd,verify_dd
from planning import order
class SessionTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.a=self.root/'.agents';shutil.copytree(A,self.a,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache','dist','sessions'));shutil.copyfile(A.parent/"AGENTS.md",self.root/"AGENTS.md");self.e=Engine(self.a)
    def tearDown(self):self.tmp.cleanup()
    def begin(self,route='dd-api',id='T1'):
        self.e.begin(route,id,'Nhiệm vụ');self.e.load(id)
    def target(self,id='T1',key='A',deps=(),kinds=('dd-api',),paths=()):self.e.target(id,key,'Mục tiêu','Có bằng chứng',list(deps),list(kinds),list(paths or (['.agents/review-reports'] if 'review-report' in kinds else ['backend'] if 'api-test' in kinds else ['dd'])))
    def test_route_all(self):
        for route in json.loads((self.a/'routing.json').read_text())['tasks']:self.assertTrue(getplan(self.a,route)['paths']);self.assertTrue(policies(self.a)[route])
    def test_create_codebase_backend_scope_does_not_require_fe_test(self):
        self.begin('create-codebase')
        self.e.target('T1','BE01','Backend nền','API, DB và migration được kiểm chứng',[],['architecture','api-test','build','context'],['apps/api'])
        self.e.start('T1')
        self.assertEqual(self.e.current('T1')['state'],'IN_PROGRESS')
    def test_create_codebase_backend_scope_can_finish_without_fe_test(self):
        self.begin('create-codebase')
        checks=[kind for kind in policies(self.a)['create-codebase'] if kind!='fe-test']
        self.e.target('T1','BE01','Backend nền','API, DB và migration được kiểm chứng',[],checks,['apps/api'])
        self.e.start('T1')
        state=self.e.current('T1');target=state['targets']['BE01']
        target['done']=True
        target['receipts']={kind:{'status':'PASS','source':{},'session':'T1','target':'BE01','scope':['apps/api'],'artifacts':{}} for kind in checks}
        with self.e.tx() as db:self.e.save(db,state)
        with patch('session.snapshot',return_value={}):self.e.finish('T1','Backend nền đạt các cổng đã khai báo')
        self.assertEqual(self.e.current('T1')['state'],'COMPLETED')
    def test_create_codebase_frontend_scope_still_requires_fe_test(self):
        self.begin('create-codebase')
        checks=[kind for kind in policies(self.a)['create-codebase'] if kind!='fe-test']
        self.e.target('T1','FULL01','Monorepo','BE và FE được kiểm chứng',[],checks,['apps/api','apps/web'])
        with self.assertRaisesRegex(ValueError,'cổng bắt buộc'):self.e.start('T1')
    def test_api_test_adapter_accepts_backend_package_coverage(self):
        package=self.root/'apps/api/omnicore_api';package.mkdir(parents=True);(package/'__init__.py').write_text('')
        (package/'maths.py').write_text('def add(left, right):\n    return left + right\n')
        tests=self.root/'apps/api/tests';tests.mkdir(parents=True)
        (tests/'test_api.py').write_text('from omnicore_api.maths import add\n\ndef test_add():\n    assert add(2, 3) == 5\n')
        result=inspect_check(self.root,self.a,'api-test',{'cwd':'apps/api','tests':'tests/test_api.py','coverage_source':'omnicore_api'},['apps/api'])
        self.assertEqual(result['details']['cases'],1)
        self.assertTrue(result['details']['executed_source'])
    def test_original_resources(self):self.assertIn('.agents/skills-original/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md',getplan(self.a,'dd-api')['paths'])
    def test_missing_context(self):
        self.e.begin('dd-api','T1','DD')
        with self.assertRaises(ValueError):self.target()
    def test_stale_context(self):
        self.begin();p=self.a/'rules/backend.md';p.write_text(p.read_text()+'\nthay doi\n')
        with self.assertRaises(ValueError):self.target()
    def test_fake_test_cli_rejected(self):
        p=subprocess.run([sys.executable,str(self.a/'tools/task.py'),'check','T1','--label','test','--',sys.executable,'-c','pass'],capture_output=True)
        self.assertNotEqual(p.returncode,0)
    def test_pending_and_no_dd(self):
        self.begin();self.target();self.e.start('T1')
        with self.assertRaises(ValueError):self.e.check('T1','A','dd-api',{'path':'absent'})
        with self.assertRaises(ValueError):self.e.verify('T1','A')
        with self.assertRaises(ValueError):self.e.finish('T1','Không được đóng')
    def test_original_template_unfilled(self):
        self.begin();self.target();self.e.start('T1');p=create_dd(self.a,'api','original',self.root/'dd')
        self.assertTrue((p/'00_Cover.md').is_file());self.assertTrue(verify_dd(self.a,'api',p,'original')['issues'])
        with self.assertRaises(ValueError):self.e.check('T1','A','dd-api',{'path':'dd'})
    def test_path_escape(self):
        self.begin()
        with self.assertRaises(ValueError):self.e.declare('T1','../../etc/passwd','all','read')
    def test_cycle(self):
        self.begin();self.target(key='A',deps=['B']);self.target(key='B',deps=['A'])
        with self.assertRaises(ValueError):self.e.start('T1')
    def test_missing_dep(self):
        self.begin();self.target(deps=['B'])
        with self.assertRaises(ValueError):self.e.start('T1')
    def test_order(self):
        self.begin();self.target();self.target(key='B',deps=['A']);self.e.start('T1')
        with self.assertRaises(ValueError):self.e.check('T1','B','dd-api',{'path':'absent'})
    def test_duplicate(self):
        self.begin()
        with self.assertRaises(ValueError):self.e.begin('dd-api','T1','Nhiệm vụ')
    def test_prior_same_type(self):
        self.e.begin('review','R','Review');self.e.begin('coding-api','B','Code');s=self.e.begin('coding-screen','C','Code');self.assertTrue(any('/B.md' in p for p in s['prior']));self.assertFalse(any('/R.md' in p for p in s['prior']))
    def test_conflict(self):
        self.begin();self.e.conflict('T1','Hai nguồn khác nhau')
        with self.assertRaises(ValueError):self.target()
        self.e.resolve('T1','Người dùng chọn nguồn A');self.e.load('T1');self.target()
    def test_lock_concurrent(self):
        self.begin(id='T1');self.begin(route='dd-screen',id='T2')
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(self.target,'T1','A',(),('dd-api',),('docs',)),pool.submit(self.target,'T2','B',(),('dd-screen',),('docs/sub',))]
            result=[]
            for f in futures:
                try:f.result();result.append(True)
                except ValueError:result.append(False)
        self.assertEqual(sum(result),1)
    def test_recover_projection(self):
        self.begin();self.target();(self.a/'target.md').write_text('hỏng');self.e.sync();self.assertIn('T1: A', (self.a/'target.md').read_text())
        self.e.block('T1','Chờ nguồn');self.e.resume('T1');self.e.start('T1');self.assertEqual(self.e.current('T1')['state'],'IN_PROGRESS')
    def test_review_report(self):
        self.begin('review');self.target(kinds=['review-report']);self.e.start('T1')
        p=self.a/'review-reports/R.json';p.parent.mkdir();p.write_text(json.dumps({'scope':'mã nguồn','limits':'chỉ đọc','tests_run':False,'findings':[]}))
        self.e.check('T1','A','review-report',{'path':'.agents/review-reports/R.json'});self.e.verify('T1','A');self.e.finish('T1','Đã kiểm tra cấu trúc báo cáo');self.assertEqual(self.e.current('T1')['state'],'COMPLETED')
    def test_review_source_changed(self):
        self.begin('review');self.target(kinds=['review-report']);self.e.start('T1');(self.root/'source.py').write_text('changed')
        p=self.a/'review-reports/R.json';p.parent.mkdir();p.write_text(json.dumps({'scope':'mã','limits':'chỉ đọc','tests_run':False,'findings':[]}))
        self.e.check('T1','A','review-report',{'path':'.agents/review-reports/R.json'});self.e.verify('T1','A')
        with self.assertRaises(ValueError):self.e.finish('T1','Không được đóng')
    def test_stale_receipt(self):
        self.begin('review');self.target(kinds=['review-report']);self.e.start('T1')
        p=self.a/'review-reports/R.json';p.parent.mkdir();p.write_text(json.dumps({'scope':'mã','limits':'chỉ đọc','tests_run':False,'findings':[]}))
        self.e.check('T1','A','review-report',{'path':'.agents/review-reports/R.json'});self.e.verify('T1','A');p.write_text(p.read_text()+'\n')
        with self.assertRaises(ValueError):self.e.finish('T1','Không được đóng')
    def test_positive_api_test_receipt(self):
        shutil.copytree(self.a/'reference/backend',self.root/'backend');self.begin('test-api');self.load_contract();self.target(kinds=['contract','api-test']);self.e.start('T1')
        self.e.check('T1','A','contract',{'path':'backend/docs/test-trace.json'})
        r=self.e.check('T1','A','api-test',{'cwd':'backend','tests':'tests/test_items.py::test_success'});self.assertEqual(r['details']['cases'],1);self.e.verify('T1','A');self.e.finish('T1','Test đã chạy')
    def load_contract(self,tests=None):
        p=self.root/'backend/docs/test-trace.json';p.parent.mkdir(parents=True,exist_ok=True)
        src='backend/docs/dd/API-001/02-overview.md'
        p.write_text(json.dumps({'decision_source':src,'requirements':[{'id':'T01','expected':'Danh sách có hai mục','source':src,'tests':tests or ['tests.test_items::test_success']}]}))
        for name in [src,'backend/docs/test-trace.json']:self.e.declare('T1',name,'toàn bộ','truy vết')
        self.e.load('T1')
    def test_root_context(self):
        self.assertIn('AGENTS.md',getplan(self.a,'coding-api')['paths'])
    def test_canonical_lock(self):
        self.begin(id='T1');self.begin(id='T2');self.target(paths=['docs/target'])
        with self.assertRaises(ValueError):self.target(id='T2',paths=['docs/../docs/target'])
    def test_required_scope(self):
        self.begin()
        with self.assertRaises(ValueError):self.e.target('T1','A','Mục tiêu','Kiểm tra',[],['dd-api'],[])
    def test_dd_empty_content(self):
        p=create_dd(self.a,'module','original',self.root/'dd')
        for f in p.rglob('*.md'):f.write_text('ok')
        self.assertTrue(verify_dd(self.a,'module',p,'original')['issues'])
        self.begin('dd-module-mobile');self.target(kinds=['dd-module'],paths=['dd']);self.e.start('T1')
        with self.assertRaisesRegex(ValueError,'DD chưa đạt'):self.e.check('T1','A','dd-module',{'path':'dd','deliverable':'draft'})
    def test_dd_wrong_target(self):
        self.begin('dd-module-mobile');self.target(kinds=['dd-module'],paths=['docs/new-dd']);self.e.start('T1')
        create_dd(self.a,'module','original',self.root/'docs/other-dd')
        with self.assertRaisesRegex(ValueError,'ngoài phạm vi'):self.e.check('T1','A','dd-module',{'path':'docs/other-dd','deliverable':'draft'})
    def test_dd_approval_not_automatic(self):
        self.begin('dd-module-mobile');self.target(kinds=['dd-module'],paths=['dd']);self.e.start('T1')
        with self.assertRaisesRegex(ValueError,'deliverable=draft'):self.e.check('T1','A','dd-module',{'path':'dd'})
    def test_dd_draft_positive(self):
        p=create_dd(self.a,'module','adapted',self.root/'dd')
        def doc(title,content):return '# '+title+'\n\n'+content+'\n'
        common='\n\n## Điều kiện, phụ thuộc và ngoại lệ\nNgười dùng chỉ đọc danh mục, khi không có dữ liệu trả danh sách trống.\n\n## Truy vết\nF-001 → FN-001 → V-001 → TC-001: đọc danh mục.'
        table='| ID | Nội dung |\n|---|---|\n| F-001 | Đọc danh mục công khai; FN-001 xử lý, V-001 hiển thị |'
        docs={'Overall.md':doc('Tổng quan',table+common),'List_Features.md':doc('Danh sách chức năng',table+common),'Function_List.md':doc('Danh sách hàm','| ID | Trách nhiệm |\n|---|---|\n| FN-001 | Đọc danh mục F-001 |\n\n## FN-001 — Hợp đồng một hàm\nĐầu vào trang, đầu ra danh sách.\n\n## Thuật toán, giao dịch và bảo mật\nChỉ đọc dữ liệu, thứ tự theo ID; không ghi.'),'Views.md':doc('Giao diện',table+common),'Import_File.md':doc('Bản đồ mã',table+common),'README.md':doc('DD bản nháp','Bản mô tả danh mục, cần duyệt nghiệp vụ.'),'history/CHANGELOG.md':doc('Lịch sử','Khởi tạo bản mô tả, chưa duyệt.'),'assets/README.md':doc('Tài nguyên','Không có tài nguyên bổ sung.'),'diagrams/README.md':doc('Sơ đồ','Luồng đọc đơn giản, chưa cần sơ đồ riêng.')}
        for name,content in docs.items():(p/name).write_text(content)
        self.assertEqual(verify_dd(self.a,'module',p,'adapted')['issues'],[])
        self.begin('dd-module-mobile');self.target(kinds=['dd-module'],paths=['dd']);self.e.start('T1')
        self.e.check('T1','A','dd-module',{'path':'dd','template':'adapted','deliverable':'draft'});self.e.verify('T1','A');self.e.finish('T1','Bản nháp đạt cấu trúc')
        state=self.e.current('T1');self.assertEqual(state['acceptance_level'],'MECHANICAL_ONLY');self.assertEqual(state['semantic_review'],'HUMAN_REQUIRED')
    def test_dummy_no_coverage(self):
        shutil.copytree(self.a/'reference/backend',self.root/'backend');p=self.root/'backend/tests/test_dummy.py';p.write_text('def test_dummy():\n    assert True\n')
        self.begin('test-api');self.load_contract(['tests.test_dummy::test_dummy']);self.target(kinds=['contract','api-test']);self.e.start('T1')
        self.e.check('T1','A','contract',{'path':'backend/docs/test-trace.json'})
        with self.assertRaisesRegex(ValueError,'Không có ca test'):self.e.check('T1','A','api-test',{'cwd':'backend','tests':'tests/test_dummy.py'})
    def test_wrong_test_scope(self):
        shutil.copytree(self.a/'reference/backend',self.root/'backend');self.begin('test-api');self.load_contract();self.target(kinds=['contract','api-test'],paths=['backend/app/core/refresh_tokens.py']);self.e.start('T1')
        self.e.check('T1','A','contract',{'path':'backend/docs/test-trace.json'})
        with self.assertRaisesRegex(ValueError,'Không có ca test'):self.e.check('T1','A','api-test',{'cwd':'backend','tests':'tests/test_items.py::test_success'})
    def test_missing_gate(self):
        self.begin('coding-api');self.target(kinds=['api-test'])
        with self.assertRaises(ValueError):self.e.start('T1')
if __name__=='__main__':unittest.main()
