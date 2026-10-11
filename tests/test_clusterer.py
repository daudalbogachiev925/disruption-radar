import numpy as np
from app.nlp.clusterer import cluster_embeddings, top_keywords

def test_cluster_embeddings():
    emb = np.random.rand(20, 16)
    labels = cluster_embeddings(emb, n_clusters=3)
    assert len(labels) == 20
    assert len(set(labels)) <= 3

def test_top_keywords():
    texts = ["ai breakthrough", "ai research", "retail boom", "retail sales"]
    labels = [0, 0, 1, 1]
    kw = top_keywords(texts, labels)
    assert 0 in kw and 1 in kw
    assert len(kw[0]) >= 1
