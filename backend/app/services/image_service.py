from app.core.config import settings
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

def upload_image(file):
    # ① 파일 확장자 뽑기 "photo.jpg" -> "jpg"
    extension = file.filename.split(".")[-1]

    # ② 고유 key 만들기: "garments/무작위값.jpg"
    key = f"garments/{uuid.uuid4()}.{extension}"

    # ③ boto3로 S3에 업로드
    s3_client.upload_fileobj(file.file, BUCKET_NAME, key)

    # ④ key 리턴
    return key