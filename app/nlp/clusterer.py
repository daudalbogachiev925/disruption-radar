import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from app.config import settings

def cluster_embeddings(embeddings: np.ndarray, n_clusters: int = None) -> np.ndarray:
    n = n_clusters or min(settings.N_CLUSTERS, len(embeddings))
    km = KMeans(n_clusters=n, random_state=42, n_init=10)
    return km.fit_predict(embeddings)

def top_keywords(texts, labels, top_n: int = 8) -> dict:
    vec = TfidfVectorizer(max_features=2000, ngram_range=(1, 2), min_df=1)
    X = vec.fit_transform(texts)
    terms = vec.get_feature_names_out()
    result = {}
    for label in set(labels):
        mask = np.array(labels) == label
        mean_tfidf = np.asarray(X[mask].mean(axis=0)).ravel()
        top_idx = mean_tfidf.argsort()[::-1][:top_n]
        result[int(label)] = [terms[i] for i in top_idx]
    return result
