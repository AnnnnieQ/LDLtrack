"""Pre-sample app posteriors for fast deployment startup.

Run from repo root:
    python scripts/precompute_posteriors.py

This writes NetCDF InferenceData files under artifacts/posteriors/.
The Streamlit app reads these files directly instead of running MCMC at
startup, so deployment opens quickly.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.app_models import POSTERIOR_DIR, save_all_posteriors


if __name__ == "__main__":
    paths = save_all_posteriors(POSTERIOR_DIR, draws=2000, overwrite=True)
    print("\nSaved posteriors:")
    for path in paths:
        print(f"  {path.relative_to(REPO_ROOT)}")
