# Size Compare Web Service

## 프로젝트 개요

(추후 작성)

## 기술 스택

- FastAPI
- SQLAlchemy
- MySQL
- Docker

## 로컬 실행법

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 디렉터리 구조

```
backend/
├── app/
│   ├── main.py       # FastAPI 앱 진입점
│   ├── core/         # 설정, 보안
│   ├── routers/      # API 엔드포인트
│   ├── models/        # SQLAlchemy 모델
│   ├── schemas/       # Pydantic 스키마
│   ├── db/            # DB 세션, base
│   └── services/      # 비즈니스 로직(사이즈 비교)
├── tests/
└── requirements.txt
docs/
├── ERD.md
└── API_SPEC.md
```
