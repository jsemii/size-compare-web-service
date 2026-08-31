from sqlalchemy.orm import Session

from app.models.garment import Garment
from app.schemas.garment import GarmentCreate, GarmentUpdate
from app.services.image_service import upload_image


def create_garment(db: Session, user_id: int, data: GarmentCreate) -> Garment:
    garment = Garment(user_id=user_id, **data.model_dump())
    db.add(garment)
    db.commit()
    db.refresh(garment)
    return garment


def set_garment_photo(db: Session, user_id: int, garment_id: int, file) -> Garment | None:
    garment = get_garment(db, user_id, garment_id)
    if garment is None:
        return None

    key = upload_image(file)        # S3에 업로드 → key 받기
    garment.photo_key = key         # DB에 key 저장
    db.commit()
    db.refresh(garment)
    return garment


def get_garments(db: Session, user_id: int) -> list[Garment]:
    return (
        db.query(Garment)
        .filter(Garment.user_id == user_id)
        .order_by(Garment.created_at.desc())
        .all()
    )


def get_garment(db: Session, user_id: int, garment_id: int) -> Garment | None:
    return (
        db.query(Garment)
        .filter(Garment.id == garment_id, Garment.user_id == user_id)
        .first()
    )


def update_garment(db: Session, user_id: int, garment_id: int, data: GarmentUpdate) -> Garment | None:
    garment = get_garment(db, user_id, garment_id)
    if garment is None:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(garment, field, value)

    db.commit()
    db.refresh(garment)
    return garment


def delete_garment(db: Session, user_id: int, garment_id: int) -> bool:
    garment = get_garment(db, user_id, garment_id)
    if garment is None:
        return False

    db.delete(garment)
    db.commit()
    return True