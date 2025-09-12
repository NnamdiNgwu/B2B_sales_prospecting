def test_list_campaigns(client):
    r = client.get("/api/campaigns")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert data[0]["id"] == "c1"
    assert "opens" in data[0]


def test_list_prospects_all(client):
    r = client.get("/api/prospects")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 3

def test_list_prospects_filters(client):
    r = client.get("/api/prospects", params={"search": "Jane", "industry": "Technology", "status": "Lead"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["name"] == "Jane Doe"


def test_health_ok(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}