"""Sinh lát cắt tham chiếu xác định, không ghi đè kho mã đích."""
import argparse, shutil, sys, tempfile, json
from pathlib import Path
A=Path(__file__).resolve().parents[1]
SKIP=shutil.ignore_patterns('__pycache__','.pytest_cache','dist','node_modules','*.db','*.sqlite3','*.pyc','sessions','*.log')
SUPPORTED={'backend':'fastapi','database':'sqlite','frontend':'typescript','authentication':'optional-jwt','cache':'memory-ttl','agent':True}
def from_config(path):
    data=json.loads(path.read_text(encoding='utf8'))
    if data!=SUPPORTED:raise ValueError('Cấu hình chưa được xác minh. Chỉ hỗ trợ đúng tổ hợp trong engines/generator-config.json')
    return 'fastapi-typescript'
def create(destination: Path, profile: str) -> None:
    if profile!='fastapi-typescript':raise ValueError('Hồ sơ chưa có bộ sinh được xác minh')
    if destination.exists() or destination.is_symlink():raise FileExistsError('Đích đã tồn tại; không ghi đè')
    if not destination.parent.is_dir():raise FileNotFoundError('Thư mục cha không tồn tại')
    with tempfile.TemporaryDirectory(dir=destination.parent) as temp:
        stage=Path(temp)/'project';stage.mkdir()
        for name in ['backend','frontend']:
            shutil.copytree(A/'reference'/name,stage/name,ignore=SKIP)
        shutil.copytree(A,stage/'.agents',ignore=SKIP)
        shutil.copyfile(A.parent/'AGENTS.md',stage/'AGENTS.md')
        shutil.copyfile(A/'reference/README.md',stage/'README.md')
        (stage/'.gitignore').write_text('.env\n.env.*\n!.env.example\n*.db\n*.sqlite3\n__pycache__/\n.pytest_cache/\ndist/\nnode_modules/\n.agents/sessions/\n',encoding='utf8')
        if destination.exists():raise FileExistsError('Đích đã tồn tại')
        stage.rename(destination)
def main():
    p=argparse.ArgumentParser(description='Tạo nền mới');p.add_argument('--destination',type=Path,required=True);group=p.add_mutually_exclusive_group(required=True);group.add_argument('--profile');group.add_argument('--config',type=Path);a=p.parse_args()
    try:create(a.destination.absolute(),a.profile or from_config(a.config))
    except (ValueError,OSError) as e:print('Không tạo được nền:',e,file=sys.stderr);return 1
    print('Đã tạo nền tại',a.destination);return 0
if __name__=='__main__':sys.exit(main())
