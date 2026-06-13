from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.donation import Donation, DonationStatus, DonationCategory
from app.models.request import MaterialRequest, RequestStatus
from app.core.dependencies import get_current_user
from app.models.user import User, UserRole
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


# ── DONATION MANAGEMENT ──────────────────────────────────────────

@router.patch("/donations/{donation_id}/approve")
def approve_donation(
    donation_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    donation.status = DonationStatus.approved
    db.commit()
    return {"message": "Donation approved"}


@router.patch("/donations/{donation_id}/reject")
def reject_donation(
    donation_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    donation.status = DonationStatus.rejected
    db.commit()
    return {"message": "Donation rejected"}


class CategorizeBody(BaseModel):
    category: DonationCategory


@router.patch("/donations/{donation_id}/categorize")
def categorize_donation(
    donation_id: int,
    body: CategorizeBody,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    donation.category = body.category
    db.commit()
    return {"message": f"Donation categorized as {body.category}"}


# ── REQUEST MANAGEMENT ───────────────────────────────────────────

@router.patch("/requests/{request_id}/approve")
def approve_request(
    request_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    req = db.query(MaterialRequest).filter(MaterialRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    req.status = RequestStatus.matched
    db.commit()
    return {"message": "Request approved"}


@router.patch("/requests/{request_id}/reject")
def reject_request(
    request_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    req = db.query(MaterialRequest).filter(MaterialRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    req.status = RequestStatus.closed
    db.commit()
    return {"message": "Request rejected"}


# ── IMPACT DASHBOARD ─────────────────────────────────────────────

@router.get("/impact")
def get_impact(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    from app.models.user import User as UserModel
    total_users = db.query(UserModel).count()
    total_donations = db.query(Donation).count()
    total_requests = db.query(MaterialRequest).count()
    approved_donations = db.query(Donation).filter(
        Donation.status == DonationStatus.approved
    ).count()

    return {
        "total_users": total_users,
        "total_donations": total_donations,
        "total_requests": total_requests,
        "approved_donations": approved_donations,
    }