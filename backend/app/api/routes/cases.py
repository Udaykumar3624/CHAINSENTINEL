import uuid
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Response, Query, status
from app.schemas.cases import (
    CaseCreateRequest, CaseUpdateRequest, CaseNoteCreateRequest,
    CaseResponse, CaseNoteItem, AuditLogItem
)
from app.services.reports.pdf_generator import PDFReportService

router = APIRouter()
pdf_service = PDFReportService()

# In-Memory DB repository store for Cases & Notes for deterministic offline MVP
CASES_STORE: List[dict] = [
    {
        "id": "case-001",
        "case_number": "CASE-2026-004",
        "title": "Suspected Peeling Chain & Rapid Forwarding Triage",
        "description": "Investigation into high-risk demo entities involved in rapid forwarding and peeling chain behavior linked to demo ransomware payload cluster.",
        "priority": "high",
        "status": "in_progress",
        "assigned_investigator": "Lead Analyst Lead",
        "created_at": "2026-08-27T08:00:00Z",
        "updated_at": "2026-08-27T10:00:00Z",
        "linked_addresses": ["bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0", "bc1qrapid83k92m1n0v9c8x7z6543210forward"],
        "linked_transactions": ["e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"],
        "notes": [
            {
                "id": "note-001",
                "case_id": "case-001",
                "author_name": "Lead Analyst Lead",
                "note_text": "Initial automated triage completed. Behavioral indicators flag 1-hop distance to known ransomware cluster.",
                "created_at": "2026-08-27T08:30:00Z"
            }
        ],
        "audit_logs": [
            {
                "id": "audit-001",
                "action": "CASE_CREATED",
                "actor_id": "analyst_lead",
                "entity_type": "case",
                "entity_id": "case-001",
                "details": {"priority": "high"},
                "created_at": "2026-08-27T08:00:00Z"
            }
        ]
    }
]

@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
def create_case(payload: CaseCreateRequest):
    case_id = str(uuid.uuid4())
    case_num = f"CASE-2026-{len(CASES_STORE) + 5:03d}"
    now_str = datetime.now(timezone.utc).isoformat()

    new_case = {
        "id": case_id,
        "case_number": case_num,
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority.lower(),
        "status": payload.status.lower(),
        "assigned_investigator": payload.assigned_investigator or "Demo Investigator",
        "created_at": now_str,
        "updated_at": now_str,
        "linked_addresses": payload.linked_addresses,
        "linked_transactions": payload.linked_transactions,
        "notes": [],
        "audit_logs": [
            {
                "id": str(uuid.uuid4()),
                "action": "CASE_CREATED",
                "actor_id": payload.assigned_investigator or "Demo Investigator",
                "entity_type": "case",
                "entity_id": case_id,
                "details": {"title": payload.title, "priority": payload.priority},
                "created_at": now_str
            }
        ]
    }

    CASES_STORE.append(new_case)
    return CaseResponse(**new_case)

@router.get("", response_model=List[CaseResponse])
def get_cases(
    status_filter: Optional[str] = Query(None, alias="status"),
    priority_filter: Optional[str] = Query(None, alias="priority")
):
    results = CASES_STORE
    if status_filter:
        results = [c for c in results if c["status"] == status_filter.lower()]
    if priority_filter:
        results = [c for c in results if c["priority"] == priority_filter.lower()]
    
    return [CaseResponse(**c) for c in results]

@router.get("/{case_id}", response_model=CaseResponse)
def get_case_by_id(case_id: str):
    for c in CASES_STORE:
        if c["id"] == case_id or c["case_number"] == case_id:
            return CaseResponse(**c)
    raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found.")

@router.patch("/{case_id}", response_model=CaseResponse)
def update_case(case_id: str, payload: CaseUpdateRequest):
    for c in CASES_STORE:
        if c["id"] == case_id or c["case_number"] == case_id:
            if payload.title is not None: c["title"] = payload.title
            if payload.description is not None: c["description"] = payload.description
            if payload.priority is not None: c["priority"] = payload.priority.lower()
            if payload.status is not None: c["status"] = payload.status.lower()
            if payload.assigned_investigator is not None: c["assigned_investigator"] = payload.assigned_investigator
            c["updated_at"] = datetime.now(timezone.utc).isoformat()

            c["audit_logs"].append({
                "id": str(uuid.uuid4()),
                "action": "CASE_UPDATED",
                "actor_id": c["assigned_investigator"],
                "entity_type": "case",
                "entity_id": c["id"],
                "details": {"status": c["status"], "priority": c["priority"]},
                "created_at": datetime.now(timezone.utc).isoformat()
            })
            return CaseResponse(**c)

    raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found.")

@router.post("/{case_id}/notes", response_model=CaseNoteItem, status_code=status.HTTP_201_CREATED)
def add_case_note(case_id: str, payload: CaseNoteCreateRequest):
    for c in CASES_STORE:
        if c["id"] == case_id or c["case_number"] == case_id:
            note_id = str(uuid.uuid4())
            now_str = datetime.now(timezone.utc).isoformat()
            new_note = {
                "id": note_id,
                "case_id": c["id"],
                "author_name": payload.author_name or "Demo Investigator",
                "note_text": payload.note_text,
                "created_at": now_str
            }
            c["notes"].append(new_note)
            c["audit_logs"].append({
                "id": str(uuid.uuid4()),
                "action": "NOTE_ADDED",
                "actor_id": payload.author_name or "Demo Investigator",
                "entity_type": "case_note",
                "entity_id": note_id,
                "details": {"note_length": len(payload.note_text)},
                "created_at": now_str
            })
            return CaseNoteItem(**new_note)

    raise HTTPException(status_code=404, detail=f"Case with ID {case_id} not found.")

@router.get("/{case_id}/report.pdf")
def export_case_pdf_report(case_id: str):
    target_case = None
    for c in CASES_STORE:
        if c["id"] == case_id or c["case_number"] == case_id:
            target_case = c
            break

    if not target_case:
        # Fallback to default case for PDF generation
        target_case = CASES_STORE[0]

    # Audit event
    target_case["audit_logs"].append({
        "id": str(uuid.uuid4()),
        "action": "PDF_REPORT_GENERATED",
        "actor_id": target_case["assigned_investigator"],
        "entity_type": "report",
        "entity_id": target_case["id"],
        "details": {"format": "pdf"},
        "created_at": datetime.now(timezone.utc).isoformat()
    })

    pdf_bytes = pdf_service.generate_case_pdf(target_case)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=ChainSentinel_Report_{target_case['case_number']}.pdf"
        }
    )
