from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.request import MaterialRequestCreate, MaterialRequestOut
from app.models.request import MaterialRequest
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=MaterialRequestOut, status_code=201)
def create_request(
    request: MaterialRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_request = MaterialRequest(**request.dict(), requester_id=current_user.id)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.get("/", response_model=List[MaterialRequestOut])
def get_requests(db: Session = Depends(get_db)):
    return db.query(MaterialRequest).all()

@router.get("/{request_id}", response_model=MaterialRequestOut)
def get_request(request_id: int, db: Session = Depends(get_db)):
    req = db.query(MaterialRequest).filter(MaterialRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req