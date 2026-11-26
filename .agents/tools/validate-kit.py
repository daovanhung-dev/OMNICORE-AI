#!/usr/bin/env python3
"""Điểm vào duy nhất của bộ kiểm định gói; dùng cùng engine với agentkit validate."""
import subprocess,sys
from pathlib import Path
if __name__=='__main__':
    sys.exit(subprocess.call([sys.executable,str(Path(__file__).resolve().parents[1]/'workflows/tools/agentkit.py'),'validate',*sys.argv[1:]]))
