from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    app_name: str = "LLM Eval Harness"
    llm_api_key: str | None = None
    default_model: str = "gpt-4o-mini"
    default_judge_model: str = "gpt-4o-mini"
    llm_timeout: int = 30
    llm_num_retries: int = 3
    dataset_path: Path = BASE_DIR / "data" / "golden_dataset.json"
    log_path: Path = BASE_DIR / "logs" / "results.jsonl"


@lru_cache
def get_settings() -> Settings:
    return Settings()
