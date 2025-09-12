from fastapi import APIRouter, BackgroundTasks, Depends
from ..schemas.automation import RunCampaignIn, RunResultOut
from ..services.automation_service import AutomationService, get_automation_service

router = APIRouter(prefix="/automation", tags=["automation"])

@router.post("/contact-forms/run", response_model=RunResultOut)
async def run_contact_forms(
    payload: RunCampaignIn,
    bg: BackgroundTasks,
    svc: AutomationService = Depends(get_automation_service),
):
    return await svc.enqueue_campaign(payload, bg)