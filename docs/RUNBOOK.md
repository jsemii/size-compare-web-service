# 운영 Runbook

## 2단계 — AWS 기반 세팅 (S3 이미지 저장)

### S3 버킷
- 이름: size-compare-garments-jsemii
- 리전: ap-northeast-2 (서울)
- 퍼블릭 액세스: 전체 차단
- 암호화: SSE-S3 (기본)

### IAM
- 사용자: size-compare-service (콘솔 접근 없음, 프로그래밍 전용)
- 정책: size-compare-s3-policy (최소권한)
  - 객체(버킷/*): GetObject, PutObject, DeleteObject
  - 버킷: ListBucket
- 자격증명: 액세스 키 → .env (git 무시)

### 설계 근거
- 루트 키 대신 최소권한 IAM 사용자: 키 유출 시 피해 범위를 이 버킷으로 한정
- 퍼블릭 차단 + presigned URL: 사진 무단 노출 방지 (고정 공개 URL 없음)