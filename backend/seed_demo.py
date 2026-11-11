"""Create an isolated local demo account and sample comparison records."""

from app.db.session import SessionLocal
from app.models.garment import Garment
from app.models.user import User
from app.models.wishlist import Wishlist
from app.services.security import hash_password


DEMO_EMAIL = "demo@example.com"
DEMO_PASSWORD = "demo1234"


def seed_demo_data() -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == DEMO_EMAIL).first()
        if user:
            print(f"데모 계정이 이미 있습니다: {DEMO_EMAIL}")
            return

        user = User(email=DEMO_EMAIL, password_hash=hash_password(DEMO_PASSWORD))
        db.add(user)
        db.flush()
        db.add_all(
            [
                Garment(
                    user_id=user.id,
                    name="잘 맞는 기본 셔츠",
                    category="상의",
                    total_length_cm=70,
                    shoulder_cm=46,
                    chest_cm=54,
                    sleeve_cm=61,
                ),
                Wishlist(
                    user_id=user.id,
                    name="비교해 볼 셔츠",
                    shop_name="로컬 데모",
                    category="상의",
                    total_length_cm=72,
                    shoulder_cm=47,
                    chest_cm=56,
                    sleeve_cm=60,
                ),
            ]
        )
        db.commit()
        print(f"로컬 데모 데이터 생성 완료: {DEMO_EMAIL} / {DEMO_PASSWORD}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
