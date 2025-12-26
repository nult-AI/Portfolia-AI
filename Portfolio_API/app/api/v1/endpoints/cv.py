from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud
from app.services.llm_service import llm_service
from typing import Any, Optional

router = APIRouter()

@router.post("/process", summary="Analyze CV PDF and optionally apply changes")
async def process_cv(
    file: UploadFile = File(...),
    mode: str = Form("preview"), # mode can be 'preview' or 'replace'
    db: Session = Depends(get_db)
):
    """
    Upload a CV PDF, analyze it using LLM.
    If mode is 'preview', only return the extracted data.
    If mode is 'replace', return extracted data and update the database.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    if mode not in ["preview", "replace"]:
        raise HTTPException(status_code=400, detail="Invalid mode. Use 'preview' or 'replace'.")
    
    try:
        content = await file.read()
        extracted_data = await llm_service.parse_cv(content)
        
        if mode == "replace":
            crud.bulk_replace_cv_data(db, extracted_data.model_dump())
            return {
                "message": "Portfolio updated successfully from CV",
                "success": True,
                "data": extracted_data
            }
        
        # Else mode is 'preview'
        return {
            "message": "CV analyzed successfully",
            "success": True,
            "data": extracted_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")
