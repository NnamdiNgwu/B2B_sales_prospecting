from pydantic import BaseModel

class CampaignOut(BaseModel):
    id: str
    name: str
    channel: str
    sent: int
    opens: int
    clicks: int
    responses: int