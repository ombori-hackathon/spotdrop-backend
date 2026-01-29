import uuid
from io import BytesIO

from minio import Minio
from minio.error import S3Error

from src.core.config import settings


class StorageService:
    def __init__(self) -> None:
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self.bucket = settings.MINIO_BUCKET

    def _ensure_bucket(self) -> None:
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def upload_image(self, file_data: bytes, content_type: str) -> tuple[str, str]:
        """Upload an image and return (object_name, url)."""
        self._ensure_bucket()

        extension = content_type.split("/")[-1]
        if extension == "jpeg":
            extension = "jpg"

        object_name = f"spots/{uuid.uuid4()}.{extension}"

        self.client.put_object(
            self.bucket,
            object_name,
            BytesIO(file_data),
            length=len(file_data),
            content_type=content_type,
        )

        url = f"http://{settings.MINIO_ENDPOINT}/{self.bucket}/{object_name}"
        return object_name, url

    def delete_image(self, object_name: str) -> bool:
        """Delete an image by object name."""
        try:
            self.client.remove_object(self.bucket, object_name)
            return True
        except S3Error:
            return False


storage_service = StorageService()
