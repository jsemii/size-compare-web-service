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

- 옷장 CRUD 5개 구현 (등록/목록/상세/수정/삭제)

- 스키마·서비스·라우터 3개 층으로 나눠서 작성

- 모든 조회에 본인 것만 보이도록 필터 적용

- Swagger로 전체 동작 확인 — 등록 201, 삭제 204, 없는 id 404

- 일부만 수정해도 나머지 값이 안 지워지는지 확인

- 다른 계정으로 로그인해서 남의 옷이 안 보이는지 확인

### 7/21

- 옷장에 category 추가, 위시리스트에 category·쇼핑몰명·사진 추가

- 컬럼 추가 후 테이블 다시 만들고 반영 확인

- 위시리스트 CRUD 5개 구현 (옷장과 같은 3계층 구조)

- 치수에 음수나 0이 들어오면 막도록 검증 추가 (422)

- Swagger로 전체 동작 + 검증 + 본인 데이터만 보이는지 확인

- 비교 API(`GET /compare`) 구현 — 내 옷 1개와 위시 1개의 치수를 항목별 비교

- cm↔inch 변환 지원, `Literal`로 단위 값 제한(잘못된 단위는 422)

- 한쪽이라도 치수가 없으면 에러 없이 누락 처리, 비교/누락 건수 함께 응답

- 카테고리 불일치 400, 미존재·타계정 데이터 404로 구분 처리

### 7/22

- pytest 도입 — 코드가 제대로 도는지 자동으로 검사하는 도구

- tests/ 폴더를 app/과 나란히 만들어 검사 코드 분리

- requirements.txt와 requirements-dev.txt 분리: 배포용에는 pytest 미포함

- 비교 기능 테스트 10개 (단위 변환 4, 문장 생성 3, 비교 로직 3)

- 비교 테스트는 DB 없이 가짜 옷 객체를 만들어 검사

- 인증 테스트 6개 (비밀번호 해싱 3, 토큰 발급 3)

- 치수가 하나 빠진 경우, inch로 요청한 경우도 각각 확인

### 7/23

- 모든 요청을 기록하는 로깅 기능 추가 (미들웨어)

- 요청번호·주소·결과·걸린시간을 JSON 한 줄로 기록

- 요청이 들어올 때 시간을 재고, 나갈 때 계산해서 남기는 방식

- 에러가 나도 기록이 빠지지 않도록 처리 (try/finally)

- /boom 이라는 임시 주소로 일부러 에러를 내서 기록 남는지 확인 후 삭제

- 기존 테스트 16개 그대로 통과하는지 재확인


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