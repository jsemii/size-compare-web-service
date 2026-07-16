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

## 개발 로그

### 7/15

- 로컬 개발 환경 세팅 (pyenv, 가상환경, Python 버전 맞추기)

- GitHub 레포 생성

- FastAPI 프로젝트 스켈레톤 생성

- 로컬 서버 실행 확인 (/health 동작 확인)

- DB 연결 및 SQLAlchemy 모델구현 (user, garments, wishlist)

- Docker Desktop 설치, MySQL 컨테이너 구동

## 7/16

- .env 연동 및 테이블 생성(init_db.py)

- 회원가입 API 구현(POST/auth/signup)

- 회원가입 bcrypt 해싱 저장, 이메일 중복 시 409 처리

- 회원가입 201 확인 및 DB 저장(해싱된 비번) 검증 완료

- 로그인 API 구현(POST/auth/login, JWT 발급)

- 로그인 성공 200 + 토큰 발급 확인, 실패 시 401 (이메일/비번 구분 X)

- feature/login 브랜치에서 작업 후 main에 merge(브랜치 전략)


## 트러블슈팅
개발 중 발생한 문제와 해결 과정은 [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)에 정리했습니다.


## 추후 로드맵

### 1단계 — MVP (현재)
- 회원가입/로그인: 이메일 + 비밀번호 + 비밀번호 해싱(bcrypt)
- 내 옷장 등록 / 위시 상품 등록 / 사이즈 비교
- 배포 및 운영

### 2단계 — 디벨롭 (MVP 완성 후)
- 이메일 인증
- 소셜 로그인 (카카오/구글)
- 비밀번호 복잡도 강제