from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.wishlist import WishlistCreate, WishlistResponse, WishlistUpdate
from app.services import wishlist as wishlist_service

router = APIRouter(prefix = "/wishlists", tags=["wishlists"])

@router.post("", response_model=WishlistResponse, status_code=status.HTTP_201_CREATED)
def create_wishlist(
    data: WishlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return wishlist_service.create_wishlist(db, current_user.id, data)

@router.get("", response_model=list[WishlistResponse])
def get_wishlists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return wishlist_service.get_wishlists(db, current_user.id)

@router.get("/{wishlist_id}", response_model=WishlistResponse)
def get_wishlist(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    wishlist = wishlist_service.get_wishlist(db, current_user.id, wishlist_id)
    if wishlist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="찾을 수 없습니다"
        )
    return wishlist

@router.put("/{wishlist_id}", response_model=WishlistResponse)
def update_wishlist(
    wishlist_id: int,
    data: WishlistUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    wishlist = wishlist_service.update_wishlist(db, current_user.id, wishlist_id, data)
    if wishlist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="찾을 수 없습니다"
        )
    return wishlist

@router.delete("/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wishlist(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = wishlist_service.delete_wishlist(db, current_user.id, wishlist_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="찾을 수 없습니다",
        )
