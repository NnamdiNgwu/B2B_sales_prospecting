def test_automation_run_enqueues_job(client):
    payload = {
        "campaign_id": "camp-1",
        "message_template": "Hi {{name}}",
        "targets": [{"domain": "example.com", "company": "Example"}],
    }
    r = client.post("/api/automation/contact-forms/run", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "queued"
    assert data["job_id"]