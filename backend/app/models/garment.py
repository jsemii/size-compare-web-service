from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Garment(Base):
    __tablename__ = "garments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)

    total_length_cm = Column(DECIMAL(5, 1), nullable=True)
    shoulder_cm = Column(DECIMAL(5, 1), nullable=True)
    chest_cm = Column(DECIMAL(5, 1), nullable=True)
    sleeve_cm = Column(DECIMAL(5, 1), nullable=True)
    waist_cm = Column(DECIMAL(5, 1), nullable=True)
    hip_cm = Column(DECIMAL(5, 1), nullable=True)
    photo_url = Column(String(500), nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="garments")
