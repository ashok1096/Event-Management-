from fastapi import Header, HTTPException, status, Depends
from app.auth.security import decode_token
from typing import List, Optional


def get_current_user(authorization: str = Header(None)):
    """Extract and validate current user from JWT token."""
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return payload


def require_role(required_roles: List[str]):
    """Factory function to create role-based access control dependency.
    
    Accepts Role enum values or plain strings. Normalises both the
    user's JWT role claim and the required_roles list to uppercase
    so comparisons are case-insensitive.
    """
    # Pre-compute the normalised set once at dependency-creation time
    _normalised = {
        (r.value if hasattr(r, "value") else str(r)).upper()
        for r in required_roles
    }

    def check_role(current_user: dict = Depends(get_current_user)):
        user_role = (current_user.get("role") or "").upper()
        if user_role not in _normalised:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This operation requires one of the following roles: {', '.join(_normalised)}"
            )
        return current_user
    return check_role


def require_admin(current_user: dict = Depends(get_current_user)):
    """Dependency to require admin role."""
    if (current_user.get("role") or "").upper() != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )
    return current_user


def require_organizer(current_user: dict = Depends(get_current_user)):
    """Dependency to require organizer or admin role."""
    if (current_user.get("role") or "").upper() not in ["ORGANIZER", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer or admin role required"
        )
    return current_user