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

parser = argparse.ArgumentParser(description ='Monitor new contratos_menores files')
parser.add_argument('--selected_year',
                    default=None,
                    type = int,
                    help ='selected year')

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_file(url, path):
    with requests.get(url, stream=True, timeout=60, verify=False) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)

print(time.strftime("%Y-%m-%d %H:%M:%S"), "- Checking for updates...")
args = parser.parse_args()
updated_files = []

try:

    # Download latest version
    path = kagglehub.dataset_download("davidcariboo/player-scores")
    print("Path to dataset files:", path)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_path = os.path.join(
        DOWNLOAD_DIR,
        f"dataset_{timestamp}.zip"
    )

    # Descarga de archivo en path temporal
    download_file(path, new_path)

except Exception as e:
    print(f"Error during check: {e}")
