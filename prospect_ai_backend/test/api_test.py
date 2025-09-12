import os
import sys
from typing import List, Optional, Dict, Any
import pytest
from fastapi.testclient import TestClient
from fastapi import BackgroundTasks

# Ensure "src" is importable
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.api.main import create_app
from src.api.services.prospect_service import ProspectService, get_prospect_service
from src.api.services.campaign_service import CampaignService, get_campaign_service
from src.api.services.llm_service import LLMService, get_llm_service
from src.api.services.automation_service import AutomationService, get_automation_service
from src.api.schemas.automation import RunCampaignIn, RunResultOut

# Mocks for dependency overrides
class MockProspectService(ProspectService):
    def __init__(self) -> None:
        self._data = [
            {"id": "p1", "name": "Jane Doe", "company": "Acme", "status": "Lead", "industry": "Technology", "lastContactDate": "2025-09-01"},
            {"id": "p2", "name": "John Smith", "company": "Globex", "status": "Qualified", "industry": "Finance", "lastContactDate": "2025-09-05"},
            {"id": "p3", "name": "Janet Roe", "company": "Initech", "status": "Contacted", "industry": "Technology", "lastContactDate": None},
        ]

    async def list(self, search: Optional[str], industries: Optional[List[str]], statuses: Optional[List[str]]) -> List[Dict[str, Any]]:
        def match(p):
            if search and search.lower() not in f"{p['name']} {p['company']}".lower():
                return False
            if industries and p["industry"] not in industries:
                return False
            if statuses and p["status"] not in statuses:
                return False
            return True
        return [p for p in self._data if match(p)]

class MockCampaignService(CampaignService):
    async def list(self) -> List[Dict[str, Any]]:
        return [{"id":"c1","name":"Q3 Outreach","channel":"Email","sent":1200,"opens":640,"clicks":210,"responses":55}]

class MockLLMService(LLMService):
    def generate(self, prompt: str, **kwargs) -> str:
        return f"mocked:{prompt}"

class RecorderBackgroundTasks(BackgroundTasks):
    def __init__(self):
        super().__init__()
        self.recorded = []

    def add_task(self, func, *args, **kwargs):
        self.recorded.append((func, args, kwargs))
        return super().add_task(func, *args, **kwargs)

class MockAutomationService(AutomationService):
    async def enqueue_campaign(self, payload: RunCampaignIn, bg: BackgroundTasks) -> RunResultOut:
        job = RunResultOut(job_id="job-123", status="queued")
        bg.add_task(lambda: None)
        return job

@pytest.fixture
def app():
    app = create_app()

    app.dependency_overrides[get_prospect_service] = lambda: MockProspectService()
    app.dependency_overrides[get_campaign_service] = lambda: MockCampaignService()
    app.dependency_overrides[get_llm_service] = lambda: MockLLMService()
    app.dependency_overrides[get_automation_service] = lambda: MockAutomationService()

    return app

@pytest.fixture
def client(app):
    return TestClient(app)