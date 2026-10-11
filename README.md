# disruption-radar
Описание: радар рыночных угроз. Парсинг новостей, кластеризация трендов, детекция emerging-технологий, алерты.  Стек: Python, FastAPI, scikit-learn, transformers, PostgreSQL, Streamlit, feedparser, Docker.

# disruption-radar

Радар рыночных угроз и emerging-трендов.

## Возможности
- Парсинг RSS-лент
- Кластеризация статей (KMeans + sentence-transformers)
- Sentiment-анализ
- Детекция emerging-трендов
- Алерты warning/critical
- Streamlit-дашборд
- Celery + beat для периодического обновления

## Быстрый старт

cp .env.example .env
docker-compose up --build

API: http://localhost:8000/docs
Dashboard: http://localhost:8501

## Ручной запуск пайплайна

docker-compose exec worker celery -A worker.celery call ingest_feeds

## Тесты

pytest tests/ -v

## Лицензия
MIT
