from functools import lru_cache
from transformers import pipeline
from app.config import settings

@lru_cache(maxsize=1)
def classifier():
    return pipeline("sentiment-analysis", model=settings.SENTIMENT_MODEL)

def classify(texts):
    out = []
    for t in texts:
        try:
            out.append(classifier()(t[:400])[0]["label"])
        except Exception:
            out.append("NEUTRAL")
    return out
