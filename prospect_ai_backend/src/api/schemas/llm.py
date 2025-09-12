from pydantic import BaseModel
from typing import Optional, Dict, Any

class GenerateIn(BaseModel):
    prompt: str
    params: Optional[Dict[str, Any]] = None

class GenerateOut(BaseModel):
    output: str