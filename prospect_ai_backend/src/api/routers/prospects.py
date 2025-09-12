from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from ..schemas.prospect import ProspectOut
from ..services.prospect_service import ProspectService, get_prospect_service

router = APIRouter(prefix="/prospects", tags=["prospects"])

@router.get("", response_model=List[ProspectOut])
async def list_prospects(
    search: Optional[str] = None,
    industry: Optional[str] = Query(None, description="CSV list"),
    status: Optional[str] = Query(None, description="CSV list"),
    svc: ProspectService = Depends(get_prospect_service),
):
    industries = industry.split(",") if industry else None
    statuses = status.split(",") if status else None
    return await svc.list(search=search, industries=industries, statuses=statuses)