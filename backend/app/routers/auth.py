"""Auth router — registration, login, JWT, admin role promotion."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.models.user_model import User
from app.models.role_enum import Role
from app.schemas.user_schema import UserRegister, UserLogin, TokenResponse
from app.auth.security import hash_password, verify_password, create_access_token
from app.auth.dependencies import get_current_user, require_role

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ── Public: Self-Registration ─────────────────────────────────────────────────
@router.post("/register", status_code=status.HTTP_200_OK)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    """
    Public endpoint — anyone can register.
    Role is ALWAYS hardcoded to ATTENDEE regardless of what the client sends.
    Admin accounts can ONLY be created by an existing Admin via /auth/promote.
    """
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    req_role = user.role.lower().strip()
    if req_role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin accounts cannot be created through public registration."
        )
    
    valid_role = Role.ORGANIZER if req_role == "organizer" else Role.ATTENDEE

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=valid_role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.user_id,
        "role": new_user.role,
    }


# ── Public: Login ─────────────────────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return a signed JWT token."""
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({
        "user_id": db_user.user_id,
        "email": db_user.email,
        "role": db_user.role.value if hasattr(db_user.role, "value") else db_user.role,
    })

    return {"access_token": token, "token_type": "bearer"}


# ── Protected: Current user info ──────────────────────────────────────────────
@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """Return the currently authenticated user's profile from JWT."""
    return current_user


# ── Admin-only: Role Promotion ────────────────────────────────────────────────
@router.put("/promote/{user_id}", status_code=status.HTTP_200_OK)
def promote_user(
    user_id: int,
    new_role: Role,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role([Role.ADMIN])),
):
    """
    Admin-only endpoint — promote or change a user's role.
    Only an existing Admin can grant ADMIN, ORGANIZER, or ATTENDEE roles.
    This is the ONLY way to create admin accounts after bootstrap.
    """
    target_user = db.query(User).filter(User.user_id == user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent self-demotion
    if target_user.user_id == current_user.get("user_id") and new_role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admins cannot demote themselves"
        )

    old_role = target_user.role
    target_user.role = new_role
    db.add(target_user)
    db.commit()

    return {
        "message": f"User role updated successfully",
        "user_id": user_id,
        "old_role": old_role,
        "new_role": new_role,
    }