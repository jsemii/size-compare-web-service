from app.db.base import Base
from app.db.session import engine

#모델 불러와야 Base가 테이블 정보 알 수 있음
from app.models import user, garment, wishlist

Base.metadata.create_all(bind=engine)
print("테이블 생성 완료")