from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.garment import GarmentCreate, GarmentResponse, GarmentUpdate
from app.services import garment as garment_service
from app.services.image_service import get_image_url

router = APIRouter(prefix="/garments", tags=["garments"])


def to_response(garment) -> GarmentResponse:
    response = GarmentResponse.model_validate(garment)
    if garment.photo_key:
        response.photo_url = get_image_url(garment.photo_key)
    return response


@router.post("", response_model=GarmentResponse, status_code=status.HTTP_201_CREATED)
def create_garment(
    data: GarmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    garment = garment_service.create_garment(db, current_user.id, data)
    return to_response(garment)


@router.post("/{garment_id}/photo", response_model=GarmentResponse)
def upload_garment_photo(
    garment_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    garment = garment_service.set_garment_photo(db, current_user.id, garment_id, file)
    if garment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="옷을 찾을 수 없습니다",
        )
    return to_response(garment)


@router.get("", response_model=list[GarmentResponse])
def get_garments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    garments = garment_service.get_garments(db, current_user.id)
    return [to_response(garment) for garment in garments]


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
    return to_response(garment)


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
    return to_response(garment)


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