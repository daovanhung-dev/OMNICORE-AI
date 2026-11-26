from fastapi.testclient import TestClient
from app.main import create_app
from app.core.config import Settings
from seed import seed
import pytest

@pytest.fixture
def client(tmp_path):
    path = tmp_path / "test.db"
    seed(path)
    with TestClient(create_app(Settings(path))) as c:
        yield c

def test_success(client):
    data = client.get("/api/v1/items").json()["data"]
    assert data["total"] == 2 and [x["id"] for x in data["items"]] == [1, 2]

def test_pagination(client):
    data = client.get("/api/v1/items?page=2&page_size=1").json()["data"]
    assert [x["id"] for x in data["items"]] == [2]

def test_empty(client):
    assert client.get("/api/v1/items?page=3&page_size=1").json()["data"]["items"] == []

@pytest.mark.parametrize("query", ["page=0", "page=-1", "page=abc", "page_size=101", "page=1%20OR%201=1", "page=9999999"])
def test_invalid(client, query):
    r = client.get("/api/v1/items?" + query)
    assert r.status_code == 422 and r.json()["error"]["code"] == "INVALID_PAGE"

def test_missing_db(tmp_path):
    with TestClient(create_app(Settings(tmp_path / "absent.db"))) as c:
        r = c.get("/api/v1/items")
        assert r.status_code == 503 and r.json()["error"]["code"] == "DATA_UNAVAILABLE"
        assert not (tmp_path / "absent.db").exists()

def test_invalid_precedes_db(tmp_path):
    with TestClient(create_app(Settings(tmp_path / "absent.db"))) as c:
        assert c.get("/api/v1/items?page=0").status_code == 422

def test_seed_no_overwrite(tmp_path):
    path = tmp_path / "exists.db"
    path.write_bytes(b"du lieu")
    with pytest.raises(FileExistsError):
        seed(path)
    assert path.read_bytes() == b"du lieu"
