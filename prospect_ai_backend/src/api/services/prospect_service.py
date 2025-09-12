from typing import List, Optional, Dict, Any

class ProspectService:
    async def list(
        self,
        search: Optional[str],
        industries: Optional[List[str]],
        statuses: Optional[List[str]],
    ) -> List[Dict[str, Any]]:
        # Minimal mock implementation; replace with DB later
        data = [
            {"id": "p1", "name": "Jane Doe", "company": "Acme", "status": "Lead", "industry": "Technology", "lastContactDate": "2025-09-01"},
            {"id": "p2", "name": "John Smith", "company": "Globex", "status": "Qualified", "industry": "Finance", "lastContactDate": "2025-09-05"},
            {"id": "p3", "name": "Janet Roe", "company": "Initech", "status": "Contacted", "industry": "Technology", "lastContactDate": None},
        ]
        def match(p):
            if search and search.lower() not in f"{p['name']} {p['company']}".lower(): return False
            if industries and p["industry"] not in industries: return False
            if statuses and p["status"] not in statuses: return False
            return True
        return [p for p in data if match(p)]

def get_prospect_service() -> ProspectService:
    return ProspectService()