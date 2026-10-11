def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200

def test_list_articles(client):
    r = client.get("/api/articles")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_list_trends(client):
    r = client.get("/api/trends")
    assert r.status_code == 200

def test_alerts(client):
    r = client.get("/api/alerts")
    assert r.status_code == 200
