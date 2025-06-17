# infrastructure/local_storage.py
from __future__ import annotations
from pathlib import Path
import aiofiles
from fastapi import UploadFile

_UPLOAD_DIR = Path("uploads")
_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class LocalFileStorage:
    """
    Minimal async local-disk storage backend used when USE_S3 == false.
    """

    async def upload(self, file: UploadFile, filename: str) -> str:
        """
        Saves <file> under uploads/<filename>.  Returns relative path as str.
        """
        dest = _UPLOAD_DIR / filename
        async with aiofiles.open(dest, "wb") as out:
            while chunk := await file.read(1024 * 1024):  # stream in 1 MB chunks
                await out.write(chunk)
        await file.close()
        return str(dest)
