from pydantic import BaseModel, AnyUrl, Field
from typing import Optional, Dict, Any, List

class AnalyzeRequest(BaseModel):
    url: AnyUrl

class ServiceDetail(BaseModel):
    status: str
    score: float
    raw: Dict[str, Any] | None = None

class AnalyzeResponse(BaseModel):
    url: str
    domain: str
    verdict: str
    risk_score: float = Field(ge=0, le=100)
    blocked: bool
    services: Dict[str, ServiceDetail]

class HistoryItem(BaseModel):
    id: int
    url: str
    domain: str
    submitted_at: str
    verdict: str
    risk_score: float
    blocked: bool

class BlockDomainRequest(BaseModel):
    domain: str
    reason: Optional[str] = "manual"

class BlockDomainResponse(BaseModel):
    domain: str
    blocked: bool
    reason: str
