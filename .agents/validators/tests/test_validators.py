import unittest, tempfile, shutil, importlib.util, sys
from pathlib import Path
A=Path(__file__).resolve().parents[2]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
validator=module('validator',A/'validators/validate_architecture.py');gen=module('generator',A/'tools/create-codebase.py');inv=validator.inv
class ArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'project';gen.create(self.root,'fastapi-typescript');self.be=self.root/'backend';self.fe=self.root/'frontend';self.api=self.be/'app/modules/shared/api_001_items_list';self.screen=self.fe/'src/app/features/shared/SH01'
    def tearDown(self):self.tmp.cleanup()
    def rules(self):return {i['rule'] for i in validator.validate(self.be,self.fe)}
    def test_valid(self):self.assertEqual(self.rules(),set())
    def test_backend_only_package_without_business_modules(self):
        package=self.root/'apps/api/omnicore_api';package.mkdir(parents=True);(package/'__init__.py').write_text('')
        self.assertEqual(validator.validate(self.root/'apps/api',backend_package='omnicore_api',allow_empty_modules=True),[])
    def test_backend_only_requires_package(self):
        issues=validator.validate(self.root/'apps/api',backend_package='omnicore_api',allow_empty_modules=True)
        self.assertIn('BE-001',{issue['rule'] for issue in issues})
    def test_backend_only_detects_python_parse_errors(self):
        package=self.root/'apps/api/omnicore_api';package.mkdir(parents=True);(package/'__init__.py').write_text('')
        (package/'broken.py').write_text('def broken(:\n')
        self.assertIn('PARSE',{issue['rule'] for issue in validator.validate(self.root/'apps/api',backend_package='omnicore_api',allow_empty_modules=True)})
    def test_missing_api_file(self):(self.api/'query.py').unlink();self.assertIn('BE-001',self.rules())
    def test_sql_in_view(self):
        with (self.api/'view.py').open('a') as f:f.write('\nWRONG="SELECT * FROM items"\n')
        self.assertIn('BE-007',self.rules())
    def test_db_in_validate(self):
        with (self.api/'validate.py').open('a') as f:f.write('\ndef wrong(db): db.execute("x")\n')
        self.assertIn('BE-003',self.rules())
    def test_db_query_in_validate(self):
        with (self.api/'validate.py').open('a') as f:f.write('\ndef bad(db): return db.query("items")\n')
        self.assertIn('BE-003',self.rules())
    def test_alias_in_validate(self):
        with (self.api/'validate.py').open('a') as f:f.write('\ndef bad(db):\n    call=db.query\n    return call("items")\n')
        self.assertIn('BE-003',self.rules())
    def test_cycle_import(self):
        (self.be/'app/core/a.py').write_text('from app.core import b\n');(self.be/'app/core/b.py').write_text('from app.core import a\n');self.assertIn('BE-010',self.rules())
    def test_generator_agent(self):self.assertTrue((self.root/'AGENTS.md').is_file());self.assertTrue((self.root/'.agents/tools/task.py').is_file())
    def test_model_in_view(self):
        with (self.api/'view.py').open('a') as f:f.write('\nclass Wrong: pass\n')
        self.assertIn('BE-002',self.rules())
    def test_query_logic(self):
        with (self.api/'query.py').open('a') as f:f.write('\ndef wrong(): return 1\n')
        self.assertIn('BE-005',self.rules())
    def test_core_import(self):
        with (self.be/'app/core/config.py').open('a') as f:f.write('\nfrom app.modules.shared import something\n')
        self.assertIn('BE-010',self.rules())
    def test_extra_screen_dir(self):(self.screen/'domain').mkdir();self.assertIn('FE-001',self.rules())
    def test_ui_http(self):
        (self.screen/'ui/wrong.ts').write_text('export const wrong=()=>fetch("/api");');self.assertIn('FE-006',self.rules())
    def test_reverse_import(self):
        (self.fe/'src/app/core/wrong.ts').write_text('import "../features/shared/SH01/pages/item-page.js";');self.assertIn('FE-010',self.rules())
    def test_missing_route(self):(self.screen.parent/'shared.route.ts').unlink();self.assertIn('FE-008',self.rules())
    def test_model_sideeffect(self):
        (self.screen/'models/wrong.ts').write_text('const x=()=>localStorage.setItem("a","b");');self.assertIn('FE-005',self.rules())
    def test_query_call_assignment(self):
        with (self.api/'query.py').open('a') as f:f.write('\nDYNAMIC=make_query()\n')
        self.assertIn('BE-005',self.rules())
    def test_ui_router(self):
        (self.screen/'ui/wrong.ts').write_text('import {Router} from "@angular/router";');self.assertIn('FE-010',self.rules())
    def test_cross_screen_import(self):
        (self.screen/'pages/wrong.ts').write_text('import "../../SH02/pages/other.js";');self.assertIn('FE-010',self.rules())
    def test_no_overwrite(self):
        with self.assertRaises(FileExistsError):gen.create(self.root,'fastapi-typescript')
    def test_reproducible(self):
        second=self.root.parent/'second';gen.create(second,'fastapi-typescript')
        for f in self.root.rglob('*'):
            if f.is_file():self.assertEqual(f.read_bytes(),(second/f.relative_to(self.root)).read_bytes())
    def test_symbols(self):
        source='export const add=(a:number,b:number):number=>a+b; class First {run(){}} class Second {async run(){}}'
        r=inv.ts_batch([{'path':'test.ts','text':source}])[0];self.assertEqual(r['status'],'STATIC_AST');self.assertTrue({'add','First.run','Second.run'} <= {x['name'] for x in r['symbols']})
    def test_python_symbols(self):
        r=inv.py_symbols('class First:\n def run(self):\n  def inner(): pass\n');self.assertEqual([x['name'] for x in r],['First','First.run','First.run.inner'])
if __name__=='__main__':unittest.main()
