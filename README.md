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

- 개발 환경 세팅 (pyenv, 가상환경, GitHub 레포)

- FastAPI 프로젝트 뼈대 생성, 로컬 서버 실행 확인

- Docker로 MySQL 컨테이너 띄우고 DB 연결

- 테이블 설계 및 모델 작성 (users, garments, wishlist)

### 7/16

- .env로 DB 접속 정보 분리, init_db.py로 테이블 생성

- 회원가입 API — 비밀번호는 해싱해서 저장, 이메일 중복이면 409

- 로그인 API — 성공 시 JWT 토큰 발급, 실패 시 401 (이메일/비번 구분 없이)

- feature 브랜치에서 작업 후 main에 머지

### 7/20

- 로그인한 사람이 누구인지 알아내는 기능 구현 (토큰 해석)

- 옷장 CRUD 5개 구현 (스키마·서비스·라우터 3층 구조)

- 본인 데이터만 보이도록 필터 적용

- Swagger로 검증 — 등록 201, 삭제 204, 없는 id 404

- 다른 계정으로 남의 옷이 안 보이는지 확인

### 7/21

- 옷장·위시리스트에 카테고리 등 컬럼 추가 후 테이블 재생성

- 위시리스트 CRUD 5개 구현 (옷장과 같은 3층 구조)

- 치수에 음수·0이 들어오면 막도록 검증 추가 (422)

- 비교 API 구현 — 내 옷과 위시 상품의 치수를 항목별 비교

- cm↔inch 변환, 치수 누락 시 에러 없이 처리, 상황별 400·404 구분


### 7/22

- pytest 도입 — 코드가 제대로 도는지 자동 검사

- tests/ 폴더를 app/과 나란히 분리, 배포용에는 pytest 미포함

- 비교 기능 테스트 10개 (단위 변환·문장 생성·비교 로직)

- 인증 테스트 6개 (비밀번호 해싱·토큰 발급)

- DB 없이 가짜 옷 객체로 검사하는 방식 적용

### 7/23

- 모든 요청을 기록하는 로깅 기능 추가 (요청번호·주소·결과·걸린시간)

- 에러가 나도 기록이 빠지지 않도록 처리 (try/finally)

- 백엔드를 도커 통에 넣는 설명서 작성, 불필요한 파일 제외로 90MB→3.7kB

- docker-compose로 백엔드와 MySQL을 명령어 하나로 실행

- 데이터 보관함 연결 — 컨테이너를 지워도 데이터 유지 확인

### 7/24

- 프론트 폴더 분리, 로그인 화면 작성 (HTML/JavaScript)

- fetch로 백엔드 로그인 API 호출 → 토큰 받아오기 성공

- 브라우저가 다른 출처 요청을 막아 백엔드에 CORS 허용 설정 추가

- 받은 토큰을 localStorage에 저장 — 새로고침해도 유지


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