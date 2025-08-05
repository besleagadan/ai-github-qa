import requests
from app.core.config import settings

def get_python_files_from_repo(owner: str, repo: str, branch: str = "main") -> list:
    # tree_url = settings.github_tree_url(branch)
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    tree_resp = requests.get(tree_url)

    if tree_resp.status_code != 200:
        raise Exception(f"Failed to fetch repo tree: {tree_resp.json()}")

    files = tree_resp.json().get("tree", [])
    python_files = [f["path"] for f in files if f["path"].endswith(".py") and f["type"] == "blob"]

    return python_files


def fetch_file_content(owner: str, repo: str, branch: str, path: str) -> str:
    # raw_url = settings.github_raw_file_url(path, branch)
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    raw_resp = requests.get(raw_url)

    if raw_resp.status_code != 200:
        raise Exception(f"Failed to fetch file: {raw_url}")

    return raw_resp.text


def fetch_repo_code(owner: str, repo: str, branch: str = "main") -> dict:
    files = get_python_files_from_repo(owner, repo, branch)
    code_data = {}

    for path in files:
        content = fetch_file_content(owner, repo, branch, path)
        code_data[path] = content

    return code_data
