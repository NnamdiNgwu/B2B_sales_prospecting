from pydantic import BaseModel
from typing import List, Optional

class Target(BaseModel):
    domain: str
    contact_url: Optional[str] = None
    company: Optional[str] = None

class RunCampaignIn(BaseModel):
    campaign_id: Optional[str] = None
    message_template: str
    targets: List[Target]

class RunResultOut(BaseModel):
    job_id: str
    status: str = "queued"