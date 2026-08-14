import os
import uuid
import boto3

# S3 리모컨 하나 (region은 서울 고정)
s3_client = boto3.client("s3", region_name="ap-northeast-2")

# 버킷 이름은 .env에서 읽어옴(아직 버킷 없으니 지금 빈 값일 수 있음)
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def upload_image(file):
    # ① 파일 확장자 뽑기 "photo.jpg" -> "jpg"
    extension = file.filename.split(".")[-1]

    # ② 고유 key 만들기: "garments/무작위값.jpg"
    key = f"garments/{uuid.uuid4()}.{extension}"

    # ③ boto3로 S3에 업로드
    s3_client.upload_fileobj(file.file, BUCKET_NAME, key)

    # ④ key 리턴
    return key