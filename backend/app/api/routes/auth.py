from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.db.session import get_db
from app.db.models import User, UserRole
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, UserResponse, TokenResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login_for_access_token(
    login_data: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate user with username/email and password, returning signed JWT token."""
    username_input = login_data.username.strip()
    password_input = login_data.password

    if not username_input or not password_input:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username/email and password are required."
        )

    user = db.query(User).filter(
        (User.username == username_input) | (User.email == username_input)
    ).first()

    if not user or not verify_password(password_input, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Access denied."
        )

    access_token = create_access_token(data={
        "sub": user.username,
        "user_id": user.id,
        "role": user.role.value if hasattr(user.role, 'value') else str(user.role),
        "email": user.email
    })

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_new_user(
    req: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """Registers a new investigator account."""
    existing_username = db.query(User).filter(User.username == req.username.strip()).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{req.username}' is already taken."
        )

    existing_email = db.query(User).filter(User.email == req.email.strip()).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{req.email}' is already registered."
        )

    user_role = UserRole.ANALYST
    if req.role and req.role.lower() in ["lead_investigator", "admin"]:
        user_role = UserRole(req.role.lower())

    new_user = User(
        username=req.username.strip(),
        email=req.email.strip(),
        full_name=req.full_name.strip(),
        password_hash=hash_password(req.password),
        role=user_role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.model_validate(new_user)

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """Logs out the active user session."""
    return {"message": "Successfully logged out active investigator session."}

@router.get("/me", response_model=UserResponse)
def get_current_authenticated_user(current_user: User = Depends(get_current_user)):
    """Returns profile details of current authenticated user."""
    return UserResponse.model_validate(current_user)
