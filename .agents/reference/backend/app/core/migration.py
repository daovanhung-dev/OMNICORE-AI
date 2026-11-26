"""Migration SQLite tại DB cục bộ đã được chỉ định, mỗi phiên bản nguyên tử."""
from pathlib import Path
from contextlib import closing
import sqlite3,hashlib

def migrate(path: Path, folder: Path) -> list[int]:
    if not path.is_file():raise FileNotFoundError('Chỉ migration DB đã tồn tại')
    versions=sorted(folder.glob('[0-9][0-9][0-9].sql')); applied=[]
    if not versions:raise ValueError('Thiếu migration')
    with closing(sqlite3.connect(path)) as db, db:
        db.execute('CREATE TABLE IF NOT EXISTS schema_versions (version INTEGER PRIMARY KEY, checksum TEXT NOT NULL)')
        for file in versions:
            version=int(file.stem); raw=file.read_bytes(); checksum=hashlib.sha256(raw).hexdigest()
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT checksum FROM schema_versions WHERE version=?',(version,)).fetchone()
            if row:
                if row[0]!=checksum:raise ValueError('Migration đã áp dụng bị đổi')
                db.commit();continue
            # Chỉ đọc bộ SQL tin cậy, không dùng executescript vì tự commit.
            buf=''
            for line in raw.decode('utf8').splitlines(keepends=True):
                buf+=line
                if sqlite3.complete_statement(buf):
                    if buf.lstrip().upper().startswith(('BEGIN','COMMIT','ROLLBACK','VACUUM','ATTACH','DETACH','PRAGMA')):raise ValueError('SQL điều khiển giao dịch không được phép')
                    db.execute(buf);buf=''
            if buf.strip():raise ValueError('SQL chưa kết thúc')
            db.execute('INSERT INTO schema_versions VALUES (?,?)',(version,checksum));db.commit();applied.append(version)
    return applied
