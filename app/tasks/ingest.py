from worker import celery
from app.database import SessionLocal
from app.ingestion.pipeline import ingest_feeds, recluster

@celery.task(name="ingest_feeds")
def ingest_feeds_task():
    db = SessionLocal()
    try:
        result = ingest_feeds(db)
        cluster_result = recluster(db)
        return {**result, **cluster_result}
    finally:
        db.close()
