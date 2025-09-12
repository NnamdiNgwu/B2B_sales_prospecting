from typing import List, Dict, Any

class CampaignService:
    async def list(self) -> List[Dict[str, Any]]:
        return [{"id":"c1","name":"Q3 Outreach","channel":"Email","sent":1200,"opens":640,"clicks":210,"responses":55}]

def get_campaign_service() -> CampaignService:
    return CampaignService()