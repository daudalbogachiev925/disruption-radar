from sqlalchemy.orm import Session
from app.models import Article, Trend
from app.ingestion.rss import parse_feed
from app.nlp.embedder import embed
from app.nlp.clusterer import cluster_embeddings, top_keywords
from app.nlp.sentiment import classify
from app.config import settings

def ingest_feeds(db: Session) -> dict:
    raw = []
    for url in settings.feeds:
        try:
            raw.extend(parse_feed(url))
        except Exception as e:
            print(f"Feed error {url}: {e}")

    new_articles = []
    for item in raw:
        if not item["url"]:
            continue
        existing = db.query(Article).filter(Article.url == item["url"]).first()
        if existing:
            continue
        new_articles.append(item)

    if not new_articles:
        return {"ingested": 0}

    texts = [(a["title"] or "") + ". " + (a["summary"] or "") for a in new_articles]
    vectors = embed(texts)
    sentiments = classify(texts)

    db_articles = []
    for item, vec, sent in zip(new_articles, vectors, sentiments):
        a = Article(
            source=item["source"],
            title=item["title"],
            summary=item["summary"],
            url=item["url"],
            published=item["published"],
            sentiment=sent,
            embedding=vec.tolist(),
        )
        db.add(a)
        db_articles.append(a)
    db.commit()
    for a in db_articles:
        db.refresh(a)

    return {"ingested": len(db_articles)}

def recluster(db: Session, n_clusters: int = None) -> dict:
    articles = db.query(Article).filter(Article.embedding.isnot(None)).all()
    if len(articles) < 2:
        return {"clusters": 0}

    import numpy as np
    vectors = np.array([a.embedding for a in articles])
    labels = cluster_embeddings(vectors, n_clusters)
    texts = [a.title or "" for a in articles]

    for a, lbl in zip(articles, labels):
        a.cluster_id = int(lbl)
    db.commit()

    keywords = top_keywords(texts, labels)

    db.query(Trend).delete()
    db.commit()

    for cid, kws in keywords.items():
        count = int((labels == cid).sum())
        t = Trend(cluster_id=cid, keywords=kws, article_count=count,
                  growth_rate=0.0)
        db.add(t)
    db.commit()

    return {"clusters": len(keywords)}
