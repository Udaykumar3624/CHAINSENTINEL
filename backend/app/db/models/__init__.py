import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum
from typing import Optional, List
from sqlalchemy import (
    String, Text, Integer, Float, Boolean, DateTime, Enum, ForeignKey, Index, Table, Column, JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class UserRole(str, PyEnum):
    ANALYST = "analyst"
    LEAD_INVESTIGATOR = "lead_investigator"
    ADMIN = "admin"


class RiskLevel(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, PyEnum):
    NEW = "new"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class CasePriority(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CaseStatus(str, PyEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


# Many-to-Many junction table for Cases <-> Addresses
case_addresses = Table(
    "case_addresses",
    Base.metadata,
    Column("case_id", String(36), ForeignKey("cases.id", ondelete="CASCADE"), primary_key=True),
    Column("address_id", String(36), ForeignKey("addresses.id", ondelete="CASCADE"), primary_key=True),
)

# Many-to-Many junction table for Cases <-> Transactions
case_transactions = Table(
    "case_transactions",
    Base.metadata,
    Column("case_id", String(36), ForeignKey("cases.id", ondelete="CASCADE"), primary_key=True),
    Column("transaction_id", String(36), ForeignKey("transactions.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.ANALYST, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    cases: Mapped[List["Case"]] = relationship("Case", back_populates="assigned_user")
    notes: Mapped[List["CaseNote"]] = relationship("CaseNote", back_populates="author")


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    address: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    cluster_label: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    risk_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW, index=True, nullable=False)
    total_received_btc: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_sent_btc: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    balance_btc: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    tx_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_known_entity: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    entity_category: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    first_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True, nullable=False)

    alerts: Mapped[List["Alert"]] = relationship("Alert", foreign_keys="[Alert.subject_id]", primaryjoin="and_(Alert.subject_id==Address.address, Alert.subject_type=='address')", back_populates="address_subject", lazy="select")
    cases: Mapped[List["Case"]] = relationship("Case", secondary=case_addresses, back_populates="linked_addresses")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    txid: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    block_height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    block_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    total_input_btc: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_output_btc: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    fee_btc: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    inputs_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    outputs_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), default=RiskLevel.LOW, index=True, nullable=False)
    raw_payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True, nullable=False)

    cases: Mapped[List["Case"]] = relationship("Case", secondary=case_transactions, back_populates="linked_transactions")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    alert_code: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    subject_type: Mapped[str] = mapped_column(String(20), index=True, nullable=False) # 'address' or 'transaction'
    subject_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), index=True, nullable=False)
    status: Mapped[AlertStatus] = mapped_column(Enum(AlertStatus), default=AlertStatus.NEW, index=True, nullable=False)
    top_signal: Mapped[str] = mapped_column(String(200), nullable=False)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True, nullable=False)

    address_subject: Mapped[Optional["Address"]] = relationship("Address", foreign_keys=[subject_id], primaryjoin="and_(Alert.subject_id==Address.address, Alert.subject_type=='address')", back_populates="alerts", uselist=False, viewonly=True)


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    case_number: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[CasePriority] = mapped_column(Enum(CasePriority), default=CasePriority.MEDIUM, nullable=False)
    status: Mapped[CaseStatus] = mapped_column(Enum(CaseStatus), default=CaseStatus.OPEN, index=True, nullable=False)
    assigned_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    assigned_investigator: Mapped[Optional[str]] = mapped_column(String(120), nullable=True, default="Demo Investigator")
    evidence_payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    network_context: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    risk_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    risk_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    linked_addresses_json: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    linked_transactions_json: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    assigned_user: Mapped[Optional["User"]] = relationship("User", back_populates="cases")
    notes: Mapped[List["CaseNote"]] = relationship("CaseNote", back_populates="case", cascade="all, delete-orphan")
    linked_addresses: Mapped[List["Address"]] = relationship("Address", secondary=case_addresses, back_populates="cases")
    linked_transactions: Mapped[List["Transaction"]] = relationship("Transaction", secondary=case_transactions, back_populates="cases")


class CaseNote(Base):
    __tablename__ = "case_notes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    case_id: Mapped[str] = mapped_column(String(36), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    note_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    case: Mapped["Case"] = relationship("Case", back_populates="notes")
    author: Mapped["User"] = relationship("User", back_populates="notes")


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    subject_type: Mapped[str] = mapped_column(String(20), nullable=False)
    subject_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    data_source: Mapped[str] = mapped_column(String(40), nullable=False)
    analysis_payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True, nullable=False)


class ApiCache(Base):
    __tablename__ = "api_cache"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    cache_key: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    response_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    actor_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False)
    details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True, nullable=False)
