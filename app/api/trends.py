from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Trend, Article

router = APIRouter()

@router.get("")
def list_trends(db: Session = Depends(get_db)):
    trends = db.query(Trend).order_by(Trend.article_count.desc()).all()
    return [{"cluster_id": t.cluster_id, "keywords": t.keywords,
             "article_count": t.article_count,
             "growth_rate": t.growth_rate} for t in trends]

@router.get("/emerging")
def emerging(db: Session = Depends(get_db), threshold: float = 1.5):
    trends = db.query(Trend).filter(Trend.growth_rate >= threshold).all()
    return [{"cluster_id": t.cluster_id, "keywords": t.keywords,
             "growth_rate": t.growth_rate} for t in trends]
