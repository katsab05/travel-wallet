import boto3
from fastapi import UploadFile
from infrastructure.file_storage import FileStorage
from core.config import get_settings

settings = get_settings()

class S3FileStorage(FileStorage):
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    async def upload(self, file: UploadFile, filename: str) -> str:
        content = await file.read()
        self.s3.upload_fileobj(
            Fileobj=UploadFileToBytesIO(content),
            Bucket=settings.AWS_BUCKET_NAME,
            Key=filename,
            ExtraArgs={"ACL": "public-read"},
        )
        return f"https://{settings.AWS_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"


# Helper to convert UploadFile to BytesIO
from io import BytesIO
def UploadFileToBytesIO(content: bytes) -> BytesIO:
    return BytesIO(content)
