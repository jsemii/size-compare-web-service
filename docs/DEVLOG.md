# 개발 로그

프로젝트 진행 과정을 날짜별로 기록합니다.

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

### 7/28
- 옷 등록 화면 작성 — 토큰을 Authorization 헤더에 실어 인증 요청
- 빈 치수 칸은 전송에서 제외해 카테고리별 부분 입력 지원 (서버에 null 저장)
- 로그인 성공/실패 분기 (response.ok) — 실패 시 안내, 성공 시 옷 등록 화면 이동
- 위시 등록 화면 작성 (쇼핑몰명 필드 추가) — 옷 등록과 동일 구조
- 로그인 → 옷 등록 → 위시 등록으로 이어지는 사용 흐름 완성

### 8/5
- 로그인 후 메인화면(main.html, main.js) 추가
- 메인 → 옷장 등록/위시 등록 페이지 이동 연결 (addEventListener + window.location.href)
- 로그인 성공 목적지 garments.html → main.html 변경

### 8/6
- 메인 화면 비교 기능 완성 — 드롭다운 선택 → 비교 → 표 표시 (한국어 항목명, null 숨김)
- 입력 단위 변환 추가 — inch 선택 시 cm로 자동 변환 후 저장
- 전체 공통 CSS 작성 — 무신사 컨셉 미니멀 (각진 모서리, 흑백 버튼, hover 반전)
- 화면 5개 통일 디자인 + 메인 레이아웃 정리 (비교 위, 등록 버튼 아래)

### 8/7
- Nginx 컨테이너 추가 (docker-compose): "/" 정적 프론트 서빙, "/api" 백엔드 리버스 프록시
- 프론트 fetch 주소를 절대경로(127.0.0.1:8000) → 상대경로(/api)로 변경
- 출처 통일로 CORSMiddleware 제거
- 로그인 폼에 Enter 키 제출 기능 추가

### 8/12
- LG 노트북(부트캠프 지급)에 병행 개발 환경 구축
- WSL2(Ubuntu) + Docker Desktop(WSL2 backend) + pyenv 3.12.13 설치
- Swagger(/docs) 접속 확인, 맥·LG 노트북 양쪽에서 병행 개발 가능한 상태 확보

### 8/14
- garment photo_url → photo_key 컬럼명 변경 (S3 object key 저장 목적)
- DB 테이블 재생성으로 스키마 동기화 (init_db는 backend/에서 실행)
- boto3 도입, S3 업로드 함수(upload_image) 작성
- wishlist 사진 전환은 garment 흐름 완성 후로 보류

### 8/16
- AWS 계정 활성화 + S3 버킷 생성 (ap-northeast-2, 퍼블릭 차단, SSE-S3)
- IAM 최소권한 사용자·정책 생성, .env에 자격증명 등록
- 맥북 환경 동기화 (git pull, boto3, DB 재생성)

### 8/28
- .env 경로를 절대경로(BASE_DIR)로 고정, 흩어진 .env를 backend/.env 하나로 통합
- S3 사진 업로드 백엔드 완성: upload_image(S3 저장 + Content-Type), get_image_url(presigned URL)
- 사진 업로드 엔드포인트 추가 (POST /garments/{id}/photo), Swagger로 실제 업로드 검증
- 프로젝트 범위 조정: 운영·CI/CD·모니터링·배치 제외, 사진 업로드 + 프론트 연결 + EC2 배포로 축소

### 8/30
- 조회 응답에 presigned URL(photo_url) 포함: photo_key를 임시 링크로 변환해 응답, to_response 헬퍼로 분리 (service=DB / router=응답 포맷 계층 분리)
- 프론트 사진 업로드 연동: garment 등록 시 FormData로 사진 함께 전송 (등록 → id 받기 → 사진 업로드 2단계)
- 비교 화면 에러 처리: response.ok 체크 후 실패 시 detail 메시지 표시 (카테고리 불일치 등)
- 로컬 전체 흐름 검증: Docker Compose(Nginx+백엔드+MySQL)로 회원가입~옷/위시 등록~사진 업로드~비교까지 실제 동작 확인

### 8/31
- 프론트에 회원가입 화면 추가 (index.html + app.js)
- AWS EC2(t3.small, Ubuntu) 배포: Docker/Compose 설치 → 코드 clone → 컨테이너 기동
- Elastic IP 할당·연결로 고정 주소 확보 (13.124.223.245)
- 퍼블릭 IP 접속으로 회원가입~비교~사진 업로드 실제 동작 검증