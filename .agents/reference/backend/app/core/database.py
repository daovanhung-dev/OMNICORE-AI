from contextlib import contextmanager
from collections.abc import Iterator
import sqlite3
from .config import Settings

@contextmanager
def get_db(settings: Settings) -> Iterator[sqlite3.Connection]:
    """Mở kết nối chỉ đọc; luôn đóng khi thoát, không tự commit."""
    db = sqlite3.connect(settings.database_path.as_uri() + "?mode=ro", uri=True)
    try:
        db.row_factory = sqlite3.Row
        yield db
    finally:
        db.close()
