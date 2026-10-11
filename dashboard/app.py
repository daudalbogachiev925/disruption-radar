import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API = os.getenv("API_URL", "http://api:8000")

st.set_page_config(page_title="Disruption Radar", layout="wide")
st.title("Disruption Radar")

@st.cache_data(ttl=30)
def fetch(path):
    return requests.get(f"{API}{path}").json()

trends = pd.DataFrame(fetch("/api/trends"))
alerts = pd.DataFrame(fetch("/api/alerts"))
articles = pd.DataFrame(fetch("/api/articles?limit=200"))

c1, c2, c3 = st.columns(3)
c1.metric("Трендов", len(trends))
c2.metric("Алертов", len(alerts))
c3.metric("Статей", len(articles))

st.subheader("Тренды по количеству статей")
if len(trends):
    st.plotly_chart(px.bar(trends, x="cluster_id", y="article_count"))

st.subheader("Emerging-тренды")
if len(alerts):
    st.dataframe(alerts)

st.subheader("Последние статьи")
if len(articles):
    st.dataframe(articles[["title","source","sentiment"]].head(50))
