from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass
class Settings:
    api_key: str
    model: str
    base_url: str


def load_settings() -> Settings:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()

    return Settings(api_key=api_key, model=model, base_url=base_url)
