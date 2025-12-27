from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core import security
from app.models.models import User
from typing import Optional

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/google-login"
)

optional_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/google-login",
    auto_error=False
)

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    user_id = security.verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_optional_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(optional_oauth2)
) -> Optional[User]:
    # This is useful for public pages that might show different things to logged in users
    if not token:
        return None
    try:
        user_id = security.verify_token(token)
        if not user_id:
            return None
        return db.query(User).filter(User.id == user_id).first()
    except Exception:
        return None
