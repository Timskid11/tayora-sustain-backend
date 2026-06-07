from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.donation import DonationCreate, DonationOut
from app.models.donation import Donation
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=DonationOut, status_code=201)
def create_donation(
    donation: DonationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_donation = Donation(**donation.dict(), donor_id=current_user.id)
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)
    return new_donation

@router.get("/", response_model=List[DonationOut])
def get_donations(db: Session = Depends(get_db)):
    return db.query(Donation).all()

@router.get("/{donation_id}", response_model=DonationOut)
def get_donation(donation_id: int, db: Session = Depends(get_db)):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation