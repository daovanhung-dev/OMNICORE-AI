"""Token opaque ngẫu nhiên, lưu hash; xoay một lần trong giao dịch SQLite. Không phải endpoint đăng nhập."""
from contextlib import closing
import hashlib,secrets,sqlite3,time
from pathlib import Path
from .responses import ApiError

def token_digest(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

class RefreshStore:
    def __init__(self, path: Path):self.path=path
    def issue(self, subject: str, ttl: int=86400) -> str:
        if not subject or not 1<=ttl<=2592000:raise ValueError('Thông số refresh không hợp lệ')
        token=secrets.token_urlsafe(32)
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('INSERT INTO refresh_tokens (digest, subject, expires) VALUES (?, ?, ?)',(token_digest(token),subject,int(time.time())+ttl))
        return token
    def rotate(self, token: str) -> tuple[str,str]:
        if not token or len(token)>256:raise ApiError(401,'INVALID_REFRESH','Phiên không hợp lệ')
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT subject, expires FROM refresh_tokens WHERE digest=?',(token_digest(token),)).fetchone()
            if not row or row[1]<=int(time.time()):raise ApiError(401,'INVALID_REFRESH','Phiên không hợp lệ')
            new=secrets.token_urlsafe(32)
            db.execute('DELETE FROM refresh_tokens WHERE digest=?',(token_digest(token),))
            db.execute('INSERT INTO refresh_tokens (digest, subject, expires) VALUES (?, ?, ?)',(token_digest(new),row[0],row[1]))
        return row[0],new
    def revoke(self, token: str) -> None:
        with closing(sqlite3.connect(self.path)) as db, db:db.execute('DELETE FROM refresh_tokens WHERE digest=?',(token_digest(token),))
