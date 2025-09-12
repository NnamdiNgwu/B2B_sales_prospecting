from fastapi import APIRouter, Depends
from typing import List
from ..schemas.campaign import CampaignOut
from ..services.campaign_service import CampaignService, get_campaign_service

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.get("", response_model=List[CampaignOut])
async def list_campaigns(svc: CampaignService = Depends(get_campaign_service)):
    return await svc.list()