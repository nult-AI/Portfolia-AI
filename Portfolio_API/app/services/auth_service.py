import os
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session
from app.models.models import User
from app.core import security

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

import requests as py_requests

def verify_google_token(token: str):
    try:
        # If it's an access_token (from useGoogleLogin), we fetch user info from Google's API
        response = py_requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            return None
            
        return response.json()
    except Exception as e:
        print(f"Token verification error: {e}")
        return None

def authenticate_google_user(db: Session, token: str):
    google_info = verify_google_token(token)
    if not google_info:
        return None
    
    email = google_info.get("email")
    google_id = google_info.get("sub")
    full_name = google_info.get("name")
    picture = google_info.get("picture")
    
    # Check if user exists
    user = db.query(User).filter(User.google_id == google_id).first()
    
    if not user:
        # Create user if doesn't exist
        user = User(
            email=email,
            google_id=google_id,
            full_name=full_name,
            picture_url=picture
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
    # Generate access token
    access_token = security.create_access_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "picture_url": user.picture_url
        }
    }
