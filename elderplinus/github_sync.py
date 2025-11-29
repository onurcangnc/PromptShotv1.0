# elderplinus/github_sync.py
"""
ElderPlinus Payload Sync
Pull ALL payload files (.mkd, .txt) from the L1B3RT4S repo root.
"""

import json
from pathlib import Path
from datetime import datetime
import requests

REPO_RAW = "https://raw.githubusercontent.com/elder-plinius/L1B3RT4S/main"
REPO_API = "https://api.github.com/repos/elder-plinius/L1B3RT4S/contents"

CACHE_DIR = Path("elderplinus_cache")
META_FILE = CACHE_DIR / "metadata.json"


def _download_text(url: str) -> str:
    r = requests.get(url, timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"Download failed: {url}")
    return r.text


def sync_elderplinus(verbose: bool = True) -> bool:
    """
    Sync ALL payload files (mkd, txt) from root of L1B3RT4S repo.
    """
    try:
        CACHE_DIR.mkdir(exist_ok=True)

        api_list = requests.get(REPO_API, timeout=20).json()
        synced_files = []

        for item in api_list:
            name = item["name"]
            if not (name.endswith(".mkd") or name.endswith(".txt")):
                continue

            download_url = f"{REPO_RAW}/{name}"
            try:
                text = _download_text(download_url)
                (CACHE_DIR / name).write_text(text, encoding="utf-8")
                synced_files.append(name)
            except Exception:
                pass

        META_FILE.write_text(json.dumps({
            "synced_at": datetime.now().isoformat(),
            "file_count": len(synced_files),
            "files": synced_files
        }, indent=2))

        if verbose:
            print(f"✅ Synced {len(synced_files)} ElderPlinus payload files.")

        return True

    except Exception as e:
        if verbose:
            print(f"❌ ElderPlinus sync failed: {e}")
        return False


def is_cache_valid(max_age_hours=72):
    if not META_FILE.exists():
        return False
    try:
        meta = json.loads(META_FILE.read_text())
        from datetime import datetime
        synced_at = datetime.fromisoformat(meta["synced_at"])
        age = (datetime.now() - synced_at).total_seconds() / 3600
        return age < max_age_hours
    except:
        return False


def ensure_elderplinus(verbose=True):
    if is_cache_valid():
        if verbose:
            print("✅ ElderPlinus cache valid")
        return True
    return sync_elderplinus(verbose)
