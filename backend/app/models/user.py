import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        Enum(UserRole, native_enum=True),
        nullable=False,
        default=UserRole.user,
        server_default=UserRole.user.value,
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    garments = relationship("Garment", back_populates="user", cascade="all, delete-orphan")
    wishlist_items = relationship("Wishlist", back_populates="user", cascade="all, delete-orphan")
