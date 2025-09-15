from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any

class ProspectOut(BaseModel):
    id: str
    name: str
    company: str
    status: str
    industry: Optional[str] = None
    lastContactDate: Optional[str] = None

# class Prospect(BaseModel):
#     id: str
#     company: str
#     website: Optional[str] = None
#     contact_email: Optional[EmailStr] = None
#     contact_name: Optional[str] = None
#     title: Optional[str] = None
#     industry: Optional[str] = None
#     status: str = "new"
#     lastContactDate: Optional[str] = None
#     notes: Optional[str] = None

# class ImportTextIn(BaseModel):
#     text: str
#     mapping: Optional[Dict[str, Any]] = None  # reserved for future column mapping

# class ImportResult(BaseModel):
#     imported: int
#     skipped: int
#     total: int
#     sample_ids: List[str]

# class GoogleSheetsSyncIn(BaseModel):
#     spreadsheet_id: str
#     range_name: str
#     # one of: inline creds JSON (dict), or path via env GOOGLE_SERVICE_ACCOUNT_JSON_PATH
#     service_account_json: Optional[Dict[str, Any]] = None
#     # optional mapping of column names -> Prospect fields
#     mapping: Optional[Dict[str, str]] = None