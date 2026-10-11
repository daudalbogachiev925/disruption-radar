from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    source = Column(String, index=True)
    title = Column(String, nullable=False)
    summary = Column(Text)
    url = Column(String, unique=True)
    published = Column(DateTime, index=True)
    cluster_id = Column(Integer, index=True)
    sentiment = Column(String)
    embedding = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, unique=True, index=True)
    keywords = Column(JSON)
    article_count = Column(Integer, default=0)
    growth_rate = Column(Float, default=0.0)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
