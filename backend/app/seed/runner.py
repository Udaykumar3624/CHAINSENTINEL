import sys
import os
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.logging import logger
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.db.models import (
    User, UserRole, Address, Transaction, Alert, AlertStatus, RiskLevel, Case, CasePriority, CaseStatus, CaseNote
)
from app.seed.seed_data import DEMO_SCENARIOS, SEED_ALERTS

def seed_database():
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # 1. Seed Demo Admin & Analyst Users
        existing_user = db.scalars(select(User).where(User.username == "analyst_lead")).first()
        if not existing_user:
            user = User(
                username="analyst_lead",
                email="analyst.lead@chainsentinel.gov",
                full_name="Lead Cybercrime Analyst",
                role=UserRole.LEAD_INVESTIGATOR,
                is_active=True
            )
            db.add(user)
            db.flush()
            logger.info("Seeded lead investigator user.")
        else:
            user = existing_user

        # 2. Seed Addresses from Scenarios & Alerts
        for scenario in DEMO_SCENARIOS:
            if scenario["subject_type"] == "address":
                addr_str = scenario["subject_id"]
                existing_addr = db.scalars(select(Address).where(Address.address == addr_str)).first()
                if not existing_addr:
                    risk_lvl = RiskLevel(scenario["risk_level"])
                    addr = Address(
                        address=addr_str,
                        cluster_label=scenario["title"],
                        risk_score=scenario["expected_score"],
                        risk_level=risk_lvl,
                        total_received_btc=15.4,
                        total_sent_btc=14.2,
                        balance_btc=1.2,
                        tx_count=24,
                        is_known_entity=(risk_lvl in [RiskLevel.HIGH, RiskLevel.CRITICAL]),
                        entity_category="Demo Flagged Entity" if risk_lvl == RiskLevel.CRITICAL else "Monitored Wallet"
                    )
                    db.add(addr)
                    logger.info(f"Seeded address entity: {addr_str}")

        # 3. Seed Transactions
        for scenario in DEMO_SCENARIOS:
            if scenario["subject_type"] == "transaction":
                tx_hash = scenario["subject_id"]
                existing_tx = db.scalars(select(Transaction).where(Transaction.txid == tx_hash)).first()
                if not existing_tx:
                    risk_lvl = RiskLevel(scenario["risk_level"])
                    tx = Transaction(
                        txid=tx_hash,
                        block_height=840120,
                        block_time=datetime.now(timezone.utc),
                        total_input_btc=25.0,
                        total_output_btc=24.995,
                        fee_btc=0.005,
                        inputs_count=1,
                        outputs_count=2,
                        risk_score=scenario["expected_score"],
                        risk_level=risk_lvl
                    )
                    db.add(tx)
                    logger.info(f"Seeded transaction entity: {tx_hash}")

        # 4. Seed Alerts
        for alert_data in SEED_ALERTS:
            existing_alert = db.scalars(select(Alert).where(Alert.id == alert_data["id"])).first()
            if not existing_alert:
                alert = Alert(
                    id=alert_data["id"],
                    alert_code=alert_data["alert_code"],
                    title=alert_data["title"],
                    subject_type=alert_data["subject_type"],
                    subject_id=alert_data["subject_id"],
                    risk_score=alert_data["risk_score"],
                    risk_level=RiskLevel(alert_data["risk_level"]),
                    status=AlertStatus(alert_data["status"]),
                    top_signal=alert_data["top_signal"],
                    evidence=alert_data["evidence"]
                )
                db.add(alert)
                logger.info(f"Seeded alert: {alert_data['alert_code']}")

        # 5. Seed Demo Investigative Case
        existing_case = db.scalars(select(Case).where(Case.case_number == "CASE-2026-004")).first()
        if not existing_case:
            demo_case = Case(
                case_number="CASE-2026-004",
                title="Suspected Peeling Chain & Rapid Forwarding Triage",
                description="Investigative case tracking high-risk demo entities involved in rapid forwarding and peeling chain patterns.",
                priority=CasePriority.HIGH,
                status=CaseStatus.IN_PROGRESS,
                assigned_user_id=user.id
            )
            db.add(demo_case)
            db.flush()

            note = CaseNote(
                case_id=demo_case.id,
                author_id=user.id,
                note_text="Initial automated triage completed. Behavioral indicators flag 1-hop distance to known ransomware cluster."
            )
            db.add(note)
            logger.info("Seeded demo case CASE-2026-004.")

        db.commit()
        logger.info("Database seeding completed successfully.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
