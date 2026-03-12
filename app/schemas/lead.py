from pydantic import BaseModel
from typing import Optional, List

class LeadBase(BaseModel):
    name: str
    website: Optional[str] = None
    niche: str
    location: str
    details: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    details: Optional[str] = None
    analysis: Optional[str] = None
    proposal_text: Optional[str] = None
    status: Optional[str] = None

class LeadInDB(LeadBase):
    id: int
    analysis: Optional[str] = None
    proposal_text: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

class LeadSearchParams(BaseModel):
    niche: str
    location: str
    details: Optional[str] = None
