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

print(time.strftime("%Y-%m-%d %H:%M:%S"), "- Checking for updates...")
args = parser.parse_args()
updated_files = []

try:

    # Download latest version
    path = kagglehub.dataset_download("davidcariboo/player-scores")
    print("Path to dataset files:", path)

    

except Exception as e:
    print(f"Error during check: {e}")
