from app.core.config import settings
from fastapi import HTTPException, status
import uuid
import boto3

# S3 리모컨 하나 (region은 서울 고정)
s3_client = boto3.client(
    "s3",
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)
BUCKET_NAME = settings.s3_bucket_name


def require_s3_configuration():
    if not all((settings.aws_access_key_id, settings.aws_secret_access_key, BUCKET_NAME)):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="사진 업로드를 사용하려면 AWS S3 설정이 필요합니다.",
        )

def upload_image(file):
    require_s3_configuration()
    # ① 파일 확장자 뽑기 "photo.jpg" -> "jpg"
    extension = file.filename.split(".")[-1]

    # ② 고유 key 만들기: "garments/무작위값.jpg"
    key = f"garments/{uuid.uuid4()}.{extension}"

    # ③ boto3로 S3에 업로드
    s3_client.upload_fileobj(
        file.file,
        BUCKET_NAME,
        key,
        ExtraArgs={"ContentType": file.content_type},
    )

    # ④ key 리턴
    return key

def get_image_url(key):
    # boto3한테 presigned URL 만들어달라고 요청
    url = s3_client.generate_presigned_url(
        "get_object",                                    # "이 객체를 가져오는" 링크
        Params={"Bucket": BUCKET_NAME, "Key": key},      # 어느 버킷의 어느 key인지
        ExpiresIn=600,                                    # 유효시간(초). 600초 = 10분
    )
    return url
