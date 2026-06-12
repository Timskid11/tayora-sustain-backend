from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.donation import DonationCreate, DonationOut, DonationUpdate
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
def get_donations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Donation).filter(Donation.donor_id == current_user.id).all()


@router.get("/all", response_model=List[DonationOut])
def get_all_donations(db: Session = Depends(get_db)):
    return db.query(Donation).all()


@router.get("/{donation_id}", response_model=DonationOut)
def get_donation(donation_id: int, db: Session = Depends(get_db)):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation


@router.put("/{donation_id}", response_model=DonationOut)
def update_donation(
    donation_id: int,
    updated: DonationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    if donation.donor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for key, value in updated.dict(exclude_unset=True).items():
        setattr(donation, key, value)

    db.commit()
    db.refresh(donation)
    return donation


@router.delete("/{donation_id}", status_code=204)
def delete_donation(
    donation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    if donation.donor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(donation)
    db.commit()