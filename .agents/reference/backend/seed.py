import argparse
import sqlite3
from pathlib import Path

def seed(path: Path) -> None:
    """Chỉ tạo tệp mới, không bao giờ ghi đè DB đã tồn tại."""
    with path.open("xb"):
        pass
    try:
        with sqlite3.connect(path) as db:
            db.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
            db.executemany("INSERT INTO items VALUES (?, ?)", [(1, "Mục thứ nhất"), (2, "Mục thứ hai")])
    except Exception:
        path.unlink(missing_ok=True)
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tạo cơ sở dữ liệu mẫu mới")
    parser.add_argument("path", type=Path)
    seed(parser.parse_args().path)
