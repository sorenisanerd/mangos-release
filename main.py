import os
import requests
from pathlib import Path


# === CONFIG ===
GITHUB_REPO = "Mastercard/mangos"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # optional
STATIC_DIR = Path(__file__).parent / "static"
SUMS_FILE = STATIC_DIR / "SHA256SUMS"
# ==============

HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def list_releases(repo):
    releases = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo}/releases?per_page=100&page={page}"
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        releases.extend(data)
        page += 1
    return releases


def build():
    STATIC_DIR.mkdir(exist_ok=True)
    with open(SUMS_FILE, "w") as f:
        for release in list_releases(GITHUB_REPO):
            for asset in release.get("assets", []):
                name = asset["name"]
                digest = asset.get("digest")
                if digest and digest.startswith("sha256:"):
                    digest = digest.split(":", 1)[1]
                    f.write(f"{digest} *{name}\n")
                else:
                    raise ValueError(f"Asset {name} does not have a valid digest")


if __name__ == "__main__":
    build()
