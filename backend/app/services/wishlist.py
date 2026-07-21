from app.schemas.wishlist import WishlistCreate, WishlistUpdate
from sqlalchemy.orm import Session
from app.models.wishlist import Wishlist

def create_wishlist(db: Session, user_id: int, data: WishlistCreate) -> Wishlist:
    wishlist = Wishlist(user_id=user_id, **data.model_dump())
    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)
    return wishlist

def get_wishlists(db: Session, user_id: int) -> list[Wishlist]:
    return (
        db.query(Wishlist)
        .filter(Wishlist.user_id == user_id)
        .order_by(Wishlist.created_at.desc())
        .all()
    )

def get_wishlist(db: Session, user_id: int, wishlist_id: int) -> Wishlist | None:
    return (
        db.query(Wishlist)
        .filter(Wishlist.id == wishlist_id, Wishlist.user_id == user_id)
        .first()
    )

def update_wishlist(db: Session, user_id: int, wishlist_id: int, data: WishlistUpdate) -> Wishlist | None:
    wishlist = get_wishlist(db, user_id, wishlist_id)
    if wishlist is None:
        return None
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(wishlist, field, value)

    db.commit()
    db.refresh(wishlist)
    return wishlist

def delete_wishlist(db: Session, user_id: int, wishlist_id: int) -> bool:
    wishlist = get_wishlist(db, user_id, wishlist_id)
    if wishlist is None:
        return False
    
    db.delete(wishlist)
    db.commit()
    return True