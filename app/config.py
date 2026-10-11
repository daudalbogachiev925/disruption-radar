from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@db:5432/radar"
    REDIS_URL: str = "redis://redis:6379/0"
    RSS_FEEDS: str = "https://techcrunch.com/feed/,https://www.vedomosti.ru/rss/news"
    N_CLUSTERS: int = 10
    SENTIMENT_MODEL: str = "distilbert-base-uncased-finetuned-sst-2-english"
    EMBED_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"

    @property
    def feeds(self) -> List[str]:
        return [f.strip() for f in self.RSS_FEEDS.split(",") if f.strip()]

    class Config:
        env_file = ".env"

settings = Settings()
