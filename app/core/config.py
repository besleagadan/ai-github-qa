from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # GITHUB Config
    GITHUB_OWNER: str
    GITHUB_REPO: str
    GITHUB_BRANCH: str = "main"  # Default branch

    # OPENAI Config
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / "dev.env",
        case_sensitive=True
    )

    def github_tree_url(self, branch: str = None) -> str:
        branch = branch or self.GITHUB_BRANCH
        return (
            f"https://api.github.com/repos/"
            f"{self.GITHUB_OWNER}/{self.GITHUB_REPO}/git/trees/"
            f"{branch}?recursive=1"
        )

    def github_raw_file_url(self, path: str, branch: str = None) -> str:
        branch = branch or self.GITHUB_BRANCH
        return (
            f"https://raw.githubusercontent.com/"
            f"{self.GITHUB_OWNER}/{self.GITHUB_REPO}/"
            f"{branch}/{path}"
        )

settings = Settings()
