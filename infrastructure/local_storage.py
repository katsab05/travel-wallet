import os
from fastapi import UploadFile
from infrastructure.file_storage import FileStorage

UPLOAD_DIR = "uploaded_docs"

class LocalFileStorage(FileStorage):
    async def upload(self, file: UploadFile, filename: str) -> str:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        return file_path
