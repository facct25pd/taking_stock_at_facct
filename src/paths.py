from pathlib import Path


SRC_DIR = Path(__file__).resolve().parent
REPO_ROOT = SRC_DIR.parent

# Input
POLIS_DATA_DIR = REPO_ROOT / "data" / "polis"
LABELS_DATA_DIR = REPO_ROOT / "data" / "labels"

# Interim = Generated on-the-fly i.e. out/in
INTERIM_DIR = LABELS_DATA_DIR / "interim"

# Output
OUT_DIR = REPO_ROOT / "out"
FIGURES_DIR = OUT_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
