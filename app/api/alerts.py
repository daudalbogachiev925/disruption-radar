from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Trend

router = APIRouter()

CRITICAL = 3.0

@router.get("")
def alerts(db: Session = Depends(get_db)):
    trends = db.query(Trend).all()
    out = []
    for t in trends:
        if t.growth_rate >= CRITICAL:
            out.append({
                "cluster_id": t.cluster_id,
                "level": "critical",
                "keywords": t.keywords,
                "growth_rate": t.growth_rate,
            })
        elif t.growth_rate >= 1.5:
            out.append({
                "cluster_id": t.cluster_id,
                "level": "warning",
                "keywords": t.keywords,
                "growth_rate": t.growth_rate,
            })
    return out
