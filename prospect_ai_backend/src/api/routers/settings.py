# from fastapi import APIRouter, Depends
# from ..schemas.settings import OrgSettings
# from ..services.settings_service import SettingsService, get_settings_service

# router = APIRouter(prefix="/settings", tags=["settings"])

# @router.get("/org", response_model=OrgSettings)
# def get_org(svc: SettingsService = Depends(get_settings_service)):
#     return OrgSettings(**svc.get_org())

# @router.post("/org", response_model=OrgSettings)
# def save_org(body: OrgSettings, svc: SettingsService = Depends(get_settings_service)):
#     saved = svc.save_org(body.dict())
#     return OrgSettings(**saved)