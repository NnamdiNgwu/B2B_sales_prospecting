from fastapi import BackgroundTasks
from typing import Dict, Any
import uuid
import os

from ..schemas.automation import RunCampaignIn, RunResultOut
from src.captcha_handler import CaptchaHandler
from src.contact_form_manager import ContactFormManager
from .llm_service import LLMService
from .mcp_client import MCPClient

class AutomationService:
    def __init__(self) -> None:
        self._llm = LLMService()
        self._captcha = CaptchaHandler()
        self._mcp = MCPClient(server_url=os.getenv("MCP_SERVER_URL", "http://localhost:8765"))

    async def enqueue_campaign(self, payload: RunCampaignIn, bg: BackgroundTasks) -> RunResultOut:
        job_id = str(uuid.uuid4())
        bg.add_task(self._run_sync, job_id, payload.dict())
        return RunResultOut(job_id=job_id, status="queued")

    def _run_sync(self, job_id: str, data: Dict[str, Any]) -> None:
        mgr = ContactFormManager(llm_manager=self._llm._mgr, captcha_handler=self._captcha)
        # Minimal call; adapt to your manager API
        mgr.run_campaign(
            targets=[t for t in data["targets"]],
            message_template=data["message_template"],
            campaign_id=data.get("campaign_id"),
        )

def get_automation_service() -> AutomationService:
    return AutomationService()