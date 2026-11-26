from pathlib import Path
from fastapi.testclient import TestClient
from app.core.config import Settings
from app.core.security import TokenConfig,Principal,issue_access,authenticate,require_owner
from app.core.refresh_tokens import RefreshStore,token_digest
from app.core.migration import migrate
from app.core.cache import TTLCache
from app.core.responses import ApiError
from app.main import create_app
from seed import seed
import pytest,sqlite3,jwt,time

@pytest.fixture
def setup(tmp_path):
    path=tmp_path/'test.db';seed(path)
    config=TokenConfig('x'*32,'local','demo');return path,config

def test_protected(setup):
    path,cfg=setup
    with TestClient(create_app(Settings(path,cfg,True))) as c:
        assert c.get('/api/v1/items').status_code==401
        token=issue_access(cfg,Principal('user',('other',)))
        assert c.get('/api/v1/items',headers={'Authorization':'Bearer '+token}).status_code==403
        token=issue_access(cfg,Principal('user',('reader',)))
        r=c.get('/api/v1/items',headers={'Authorization':'Bearer '+token});assert r.status_code==200 and r.json()['data']['total']==2
        assert len(r.headers['X-Request-ID'])==32

def test_jwt_wrong_audience(setup):
    _,cfg=setup;token=issue_access(cfg,Principal('user',('reader',)))
    with pytest.raises(ApiError):authenticate(TokenConfig(cfg.secret,cfg.issuer,'other'),'Bearer '+token)

def test_jwt_expired(setup):
    _,cfg=setup;token=issue_access(cfg,Principal('user',('reader',)))
    payload=jwt.decode(token,cfg.secret,algorithms=['HS256'],audience=cfg.audience);payload['exp']=int(time.time())-1
    with pytest.raises(ApiError):authenticate(cfg,'Bearer '+jwt.encode(payload,cfg.secret,algorithm='HS256'))

def test_owner():
    require_owner(Principal('a',()),'a')
    with pytest.raises(ApiError):require_owner(Principal('a',()),'b')

def test_refresh_and_migration(setup):
    path,_=setup;folder=Path(__file__).resolve().parents[1]/'migrations'
    assert migrate(path,folder)==[1,2];assert migrate(path,folder)==[]
    store=RefreshStore(path);old=store.issue('user');subject,new=store.rotate(old);assert subject=='user' and old!=new
    with pytest.raises(ApiError):store.rotate(old)
    with sqlite3.connect(path) as db:assert db.execute('SELECT digest FROM refresh_tokens').fetchone()[0]==token_digest(new)
    store.revoke(new)
    with pytest.raises(ApiError):store.rotate(new)

def test_migration_rollback(setup,tmp_path):
    path,_=setup;folder=tmp_path/'bad';folder.mkdir();(folder/'001.sql').write_text('CREATE TABLE temp_demo (id INT);\nINVALID SQL;\n')
    with pytest.raises(sqlite3.Error):migrate(path,folder)
    with sqlite3.connect(path) as db:assert db.execute("SELECT name FROM sqlite_master WHERE name='temp_demo'").fetchone() is None

def test_cache():
    cache=TTLCache(1);cache.set('a',1,1);assert cache.get('a')==1;cache.set('b',2,1);assert cache.get('a') is None;cache.invalidate('b');assert cache.get('b') is None

def test_health(setup,tmp_path):
    path,cfg=setup
    with TestClient(create_app(Settings(path))) as c:assert c.get('/health/live').status_code==200 and c.get('/health/ready').status_code==200
    with TestClient(create_app(Settings(tmp_path/'absent.db'))) as c:assert c.get('/health/ready').status_code==503
