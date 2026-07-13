from abc import ABC, abstractmethod

class StorageBackend(ABC):
    """Abstract base class for file storage operations."""
    
    @abstractmethod
    async def upload_file(self, file_path: str, content: bytes) -> str:
        """Upload a file and return its URL/Path."""
        pass

    @abstractmethod
    async def download_file(self, file_path: str) -> bytes:
        """Download a file's content."""
        pass

class LocalStorage(StorageBackend):
    """Local filesystem storage implementation."""
    
    async def upload_file(self, file_path: str, content: bytes) -> str:
        # Save locally in a /uploads directory
        return f"/local-uploads/{file_path}"
        
    async def download_file(self, file_path: str) -> bytes:
        return b""
        
class S3Storage(StorageBackend):
    """AWS S3 storage implementation."""
    
    async def upload_file(self, file_path: str, content: bytes) -> str:
        # Upload to S3 bucket using boto3/aioboto3
        return f"s3://my-bucket/{file_path}"
        
    async def download_file(self, file_path: str) -> bytes:
        return b""

def get_storage() -> StorageBackend:
    """Factory to get the configured storage backend."""
    # Logic to switch between Local and S3 based on config
    return LocalStorage()
