import feedparser
from datetime import datetime
from typing import List, Dict

def parse_feed(url: str) -> List[Dict]:
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries:
        published = None
        if getattr(entry, "published_parsed", None):
            published = datetime(*entry.published_parsed[:6])
        items.append({
            "source": feed.feed.get("title", url),
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "url": entry.get("link", ""),
            "published": published,
        })
    return items
