from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.garment import Garment
from app.models.user import User
from app.models.wishlist import Wishlist
from app.schemas.compare import CompareResponse
from app.services.compare import compare_garment_with_wish

router = APIRouter(prefix="/compare", tags=["compare"])


@router.get("", response_model=CompareResponse)
def compare(
    garment_id: int = Query(..., description="비교할 내 옷 ID"),
    wishlist_id: int = Query(..., description="비교할 위시 상품 ID"),
    unit: Literal["cm", "inch"] = Query("cm", description="결과 단위"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    garment = (
        db.query(Garment)
        .filter(Garment.id == garment_id, Garment.user_id == current_user.id)
        .first()
    )
    if garment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 옷을 찾을 수 없습니다",
        )

    wish = (
        db.query(Wishlist)
        .filter(Wishlist.id == wishlist_id, Wishlist.user_id == current_user.id)
        .first()
    )
    if wish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 위시 상품을 찾을 수 없습니다",
        )

    if garment.category != wish.category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="카테고리가 다른 항목은 비교할 수 없습니다",
        )

    return compare_garment_with_wish(garment, wish, unit)