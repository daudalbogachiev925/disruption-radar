from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Article

router = APIRouter()

@router.get("")
def list_articles(limit: int = Query(100, le=1000),
                  cluster_id: Optional[int] = None,
                  db: Session = Depends(get_db)):
    q = db.query(Article)
    if cluster_id is not None:
        q = q.filter(Article.cluster_id == cluster_id)
    rows = q.order_by(Article.published.desc().nullslast()) \
            .limit(limit).all()
    return [{"id": r.id, "source": r.source, "title": r.title,
             "url": r.url, "cluster_id": r.cluster_id,
             "sentiment": r.sentiment,
             "published": r.published.isoformat() if r.published else None}
            for r in rows]
