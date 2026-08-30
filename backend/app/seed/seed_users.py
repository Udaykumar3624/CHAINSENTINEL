from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.logging import logger
from app.core.security import hash_password
from app.db.models import User, UserRole

def seed_demo_user(db: Session) -> User:
    """Seeds default demo investigator account or updates existing demo user with current credentials."""
    existing_user = db.query(User).filter(
        (User.username == settings.DEMO_USERNAME) | (User.email == settings.DEMO_EMAIL)
    ).first()

    if existing_user:
        existing_user.username = settings.DEMO_USERNAME
        existing_user.email = settings.DEMO_EMAIL
        existing_user.password_hash = hash_password(settings.DEMO_PASSWORD)
        existing_user.is_active = True
        db.commit()
        db.refresh(existing_user)
        logger.info(f"Updated demo investigator account '{existing_user.username}' ({existing_user.email})")
        return existing_user

    demo_user = User(
        username=settings.DEMO_USERNAME,
        email=settings.DEMO_EMAIL,
        full_name=settings.DEMO_FULL_NAME,
        password_hash=hash_password(settings.DEMO_PASSWORD),
        role=UserRole.LEAD_INVESTIGATOR,
        is_active=True
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)
    logger.info(f"Successfully seeded demo investigator account '{demo_user.username}' ({demo_user.email})")
    return demo_user
