def test_llm_generate(client):
    r = client.post("/api/llm/generate", json={"prompt": "Hello", "params": {"temperature": 0}})
    assert r.status_code == 200
    data = r.json()
    assert data["output"] == "mocked:Hello"