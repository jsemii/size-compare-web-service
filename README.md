# 옷 사이즈 비교 서비스

> 잘 맞는 **내 옷의 실측 치수**를 기준으로, 사려는 옷의 치수를 항목별로 비교해 온라인 구매 시 사이즈 실패를 줄이는 웹 서비스

<!-- GIF 녹화 후 아래 두 줄의 주석을 풀고 이 줄을 지우세요.
![시연 화면](docs/images/demo.gif)
*서버 종료 후 로컬 Docker 환경에서 재현한 화면*
-->

| 기간 | 역할 | 상태 |
|---|---|---|
| 2026-07-15 ~ 09-01 (7주) | 1인 풀스택 (기획·백엔드·프론트·배포) | 08-31 AWS EC2 배포·외부 접속 검증 후 비용 문제로 종료 → [로컬 실행](#로컬-실행)으로 재현 가능 |

**규모** REST API 14개 · 화면 4개 · pytest 16개 · 트러블슈팅 기록 28건

---

## 문제와 해결

같은 "M"이라도 쇼핑몰마다 실측이 다르고, 상세페이지 숫자만으로는 내 몸에 맞을지 판단하기 어렵습니다. 이미 잘 맞는 내 옷을 기준점으로 삼아 위시 상품과 **총장·어깨·가슴·소매·허리·엉덩이**를 비교하고, `"내 옷보다 +2.0cm 큽니다"`처럼 차이를 보여 줍니다.

## 주요 기능

- **회원가입·로그인** — bcrypt 해싱, JWT 인증, 모든 데이터를 `user_id`로 격리
- **내 옷장 등록** — 상세 치수 + 사진(S3 저장, DB에는 객체 키만 보관)
- **위시 상품 등록** — 쇼핑몰 기재 치수 입력
- **사이즈 비교** — 항목별 차이 계산, cm↔inch 변환, 누락 치수는 해당 항목만 제외, 카테고리가 다르면 400

## 기술 스택

| 구분 | 사용 기술 |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy, python-jose(JWT), bcrypt |
| Frontend | HTML / CSS / JavaScript |
| Data | MySQL 8.0, AWS S3 |
| Infra | Docker Compose, Nginx, AWS EC2 · IAM · Elastic IP |
| Test | pytest, Swagger |

## 아키텍처

```
브라우저 → Nginx ─ "/"    정적 프론트
                └ "/api" → FastAPI ─┬─ MySQL  (사용자·옷·위시)
                                    └─ AWS S3 (사진, presigned URL)
```

- **같은 출처로 통합** — Nginx가 프론트와 `/api`를 함께 서빙해 CORS 미들웨어 없이 동작
- **사진 보안** — S3 퍼블릭 접근 차단 + SSE-S3 암호화, 조회 시에만 10분짜리 presigned URL 발급
- **최소 권한** — 루트 키 대신 이 버킷 접근 권한만 가진 IAM 사용자 사용 (키 유출 시 피해 범위를 버킷 하나로 한정)
- **배포** — 로컬에서 검증한 Compose 구성을 EC2(t3.small)에 그대로 올리고, 공개 주소로 회원가입 → 사진 업로드 → 비교 전 흐름 확인

<details>
<summary>API 목록 (14개)</summary>

| 구분 | Method · Path |
|---|---|
| 인증 | `POST /auth/signup` · `POST /auth/login` |
| 옷장 | `POST /garments` · `GET /garments` · `GET/PUT/DELETE /garments/{id}` · `POST /garments/{id}/photo` |
| 위시 | `POST /wishlists` · `GET /wishlists` · `GET/PUT/DELETE /wishlists/{id}` |
| 비교 | `GET /compare?garment_id=&wishlist_id=&unit=cm\|inch` |

외부에서는 Nginx를 거쳐 `/api` 접두사로 호출합니다. 상세 명세는 로컬 실행 후 Swagger(`http://localhost:8000/docs`)에서 확인할 수 있습니다.

</details>

## 테스트

에러 없이 결과만 틀리는 버그(조회 조건에 엉뚱한 컬럼 비교, 객체를 id 대신 전달)를 연달아 겪은 뒤 pytest를 도입했습니다. DB 없이 가짜 객체로 핵심 로직을 검사합니다.

| 영역 | 개수 | 검증 내용 |
|---|---|---|
| 비교 로직 | 10 | cm↔inch 변환·반올림, 차이 문장(큼/작음/같음), 누락 항목 제외, inch 단위 비교 |
| 인증 | 6 | 해시가 원문과 다르고 매번 달라짐(salt), 비밀번호 검증, JWT에 사용자 id·만료 시간 포함 |

CRUD와 본인 데이터 격리는 Swagger에서 다른 계정으로 직접 확인했습니다. 자동화는 다음 과제입니다.

## 트러블슈팅

28건 전체는 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)에 있습니다. 대표 사례:

- **카테고리를 보냈는데 NULL로 저장** — 스키마에 필드가 없어 pydantic이 값을 조용히 버렸고, 나중에 비교 API의 400으로 드러남 → 스키마 보완. 응답보다 `SELECT`로 실제 저장값부터 확인하는 습관을 얻음
- **새 엔드포인트가 Swagger에 안 보임** — Docker 백엔드가 8000 포트를 먼저 잡고 옛 코드를 서빙 → `lsof`로 점유 프로세스 확인
- **Docker 빌드 컨텍스트 90MB** — `.dockerignore`가 없어 가상환경과 `.env`까지 복사됨 → 3.7kB로 줄이고 비밀정보 유출 위험도 제거

## 로컬 실행

```bash
git clone https://github.com/jsemii/size-compare-web-service.git
cd size-compare-web-service
docker compose up -d --build
docker compose exec backend python init_db.py
docker compose exec backend python seed_demo.py   # 데모 계정·샘플 데이터
```

`http://localhost` 접속 → `demo@example.com` / `demo1234`로 로그인

<details>
<summary>설정 참고</summary>

- Compose는 로컬 데모 전용 DB 계정과 JWT 키를 사용하며 `backend/.env`를 읽지 않습니다. 배포에 재사용하지 마세요.
- 사진 업로드만 AWS S3 설정이 필요합니다. 설정이 없으면 업로드 시 안내 메시지가 표시되고 나머지 기능은 그대로 동작합니다.
- 테스트: `cd backend && pip install -r requirements-dev.txt && pytest`
- 종료: `docker compose down` (데모 데이터까지 지우려면 `-v`)

</details>

## 회고

- **범위를 줄여 끝까지 완성** — 리뷰 크롤링·추천 모델·CI/CD를 제외하고 기획 → 개발 → 배포를 혼자 끝냈습니다.
- **코드 밖의 문제가 더 자주 막았다** — 설정 파일 경로, 컨테이너 포트, 머신마다 다른 DB 상태처럼 배포·환경 문제가 실제 시간을 가장 많이 썼습니다.
- **개발 방식** — AI 코딩 에이전트에게 개념 설명과 리뷰를 받고 기능 코드는 직접 작성했습니다. 서버 종료 후 데모 정리 작업은 에이전트의 도움을 받았습니다.

**다음에 한다면** API 통합 테스트(권한 격리) · Alembic 마이그레이션 · 도메인과 HTTPS

날짜별 개발 과정은 [DEVLOG.md](docs/DEVLOG.md)에 있습니다.
