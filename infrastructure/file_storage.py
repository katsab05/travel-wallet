"""
Generic file uploader interface (Strategy Pattern)
"""

from fastapi import UploadFile
from abc import ABC, abstractmethod

class FileStorage(ABC):
    @abstractmethod
    async def upload(self, file: UploadFile, filename: str) -> str:
        """
        Upload a file and return its accessible URL or path.

        Args:
            file (UploadFile): The file object
            filename (str): Destination file name

        Returns:
            str: URL or path where the file was saved
        """
        pass
