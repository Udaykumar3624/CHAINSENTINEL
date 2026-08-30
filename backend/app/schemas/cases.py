from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class CaseCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=5)
    priority: str = Field("medium", description="low, medium, high, critical")
    status: str = Field("open", description="open, in_progress, closed")
    assigned_investigator: Optional[str] = Field("Demo Investigator", description="Display identity")
    linked_addresses: List[str] = []
    linked_transactions: List[str] = []
    linked_alert_ids: List[str] = []

class CaseUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_investigator: Optional[str] = None

class CaseNoteCreateRequest(BaseModel):
    note_text: str = Field(..., min_length=2)
    author_name: Optional[str] = "Demo Investigator"

class CaseNoteItem(BaseModel):
    id: str
    case_id: str
    author_name: str
    note_text: str
    created_at: str

class AuditLogItem(BaseModel):
    id: str
    action: str
    actor_id: str
    entity_type: str
    entity_id: str
    details: Optional[Dict[str, Any]] = None
    created_at: str

class CaseResponse(BaseModel):
    id: str
    case_number: str
    title: str
    description: str
    priority: str
    status: str
    assigned_investigator: str
    created_at: str
    updated_at: str
    linked_addresses: List[str] = []
    linked_transactions: List[str] = []
    notes: List[CaseNoteItem] = []
    audit_logs: List[AuditLogItem] = []
