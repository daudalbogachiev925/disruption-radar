from app.nlp.sentiment import classify

def test_classify_returns_labels():
    labels = classify(["Amazing product", "Terrible failure"])
    assert len(labels) == 2
    assert all(l in ("POSITIVE", "NEGATIVE", "NEUTRAL") for l in labels)
