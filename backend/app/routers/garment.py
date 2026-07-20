from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.garment import GarmentCreate, GarmentResponse, GarmentUpdate
from app.services import garment as garment_service

router = APIRouter(prefix = "/garments", tags=["garments"])

@router.post("", response_model=GarmentResponse, status_code=status.HTTP_201_CREATED)
def create_garment(
    data: GarmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return garment_service.create_garment(db, current_user.id, data)

@router.get("", response_model=list[GarmentResponse])
def get_garments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return garment_service.get_garments(db, current_user.id)

@router.get("/{garment_id}", response_model=GarmentResponse)
def get_garment(
    garment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    garment = garment_service.get_garment(db, current_user.id, garment_id)
    if garment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="옷을 찾을 수 없습니다",
        )
    return garment

@router.put("/{garment_id}", response_model=GarmentResponse)
def update_garment(
    garment_id: int,
    data: GarmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    garment = garment_service.update_garment(db, current_user.id, garment_id, data)
    if garment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="옷을 찾을 수 없습니다",
        )
    return garment

@router.delete("/{garment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_garment(
    garment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = garment_service.delete_garment(db, current_user.id, garment_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="옷을 찾을 수 없습니다",
        )
