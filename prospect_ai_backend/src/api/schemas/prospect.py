from pydantic import BaseModel
from typing import Optional

class ProspectOut(BaseModel):
    id: str
    name: str
    company: str
    status: str
    industry: Optional[str] = None
    lastContactDate: Optional[str] = None