import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / ".agents" / "skills" / "vectordeckppt" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
