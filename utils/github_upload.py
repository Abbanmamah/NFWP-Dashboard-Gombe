import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO")


def upload_file(local_file, github_file):

    with open(local_file, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{github_file}"

    # Check if file already exists
    r = requests.get(url, headers=headers)

    sha = None

    if r.status_code == 200:
        sha = r.json()["sha"]

    body = {
        "message": f"Update {github_file}",
        "content": content
    }

    if sha:
        body["sha"] = sha

    response = requests.put(
        url,
        headers=headers,
        json=body
    )

    response.raise_for_status()