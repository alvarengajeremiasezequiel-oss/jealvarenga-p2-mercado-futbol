from pathlib import Path
import time
import os
import urllib3
import requests
from datetime import datetime
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import argparse
import kagglehub
import certifi
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =====================
# Configuración
# =====================
DOWNLOAD_DIR = "data"
HASH_FILE = os.path.join(DOWNLOAD_DIR, "last_hash.txt")

def save_env_var(env_var, value):
    github_env = os.environ.get("GITHUB_ENV")
    if github_env:
        with open(github_env, "a") as f:
            f.write(f"{env_var}={str(value)}\n")
    else:
        os.environ[env_var] = str(value)

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

print(time.strftime("%Y-%m-%d %H:%M:%S"), "- Checking for updates...")

try:

    # Download latest version
    path = kagglehub.dataset_download("davidcariboo/player-scores")
    print("Path to dataset files:", path)

    save_env_var("DATASET_PATH", path)

except Exception as e:
    print(f"Error during check: {e}")
