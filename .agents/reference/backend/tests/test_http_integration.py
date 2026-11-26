"""Kiểm thử HTTP thật qua proxy + Uvicorn + SQLite tạm, không cần browser."""
import os,sys,subprocess,socket,time,json,sqlite3
from pathlib import Path
from urllib.request import urlopen
from seed import seed

def available_port():
    with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]

def wait(url,proc):
    for _ in range(60):
        if proc.poll() is not None:raise RuntimeError('Tiến trình kết thúc sớm')
        try:
            with urlopen(url,timeout=.3) as r:return r.read()
        except OSError:time.sleep(.1)
    raise RuntimeError('Không khởi động được HTTP')

def test_http_proxy(tmp_path):
    root=Path(__file__).resolve().parents[1];fe=root.parent/'frontend';db=tmp_path/'demo.db';seed(db)
    port=available_port();proxy=available_port();env=os.environ.copy();env.update(DEMO_DB=str(db),DEMO_PROTECTED='0')
    processes=[]
    try:
        be=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app_factory','--factory','--host','127.0.0.1','--port',str(port)],cwd=root,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);processes.append(be)
        wait(f'http://127.0.0.1:{port}/health/ready',be)
        f=subprocess.Popen([sys.executable,'serve.py','--port',str(proxy),'--backend-port',str(port)],cwd=fe,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);processes.append(f)
        assert b'html' in wait(f'http://127.0.0.1:{proxy}/items',f).lower()
        with urlopen(f'http://127.0.0.1:{proxy}/api/v1/items?page=2&page_size=1',timeout=2) as r:
            assert json.load(r)['data']['items']==[{'id':2,'name':'Mục thứ hai'}];assert len(r.headers['X-Request-ID'])==32
        with sqlite3.connect(db) as conn:assert conn.execute('SELECT COUNT(*) FROM items').fetchone()[0]==2
    finally:
        for p in reversed(processes):
            p.terminate()
            try:p.wait(timeout=5)
            except subprocess.TimeoutExpired:p.kill();p.wait()
