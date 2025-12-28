from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import auth_service

router = APIRouter()

@router.post("/google-login")
async def google_login(token_data: dict = Body(...), db: Session = Depends(get_db)):
    token = token_data.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Token is required")
    
    auth_data = auth_service.authenticate_google_user(db, token)
    if not auth_data:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    
    return auth_data
