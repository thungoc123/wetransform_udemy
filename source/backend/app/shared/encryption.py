from cryptography.fernet import Fernet

from app.config import settings


class DataEncryptor:
    def __init__(self):
        # Fernet requires a 32-byte url-safe base64-encoded key.
        # We load it from settings.ENCRYPTION_KEY
        self.cipher = Fernet(settings.ENCRYPTION_KEY.encode("utf-8"))

    def encrypt(self, plain_text: str) -> str:
        """Encrypts a plain text string and returns the base64 encoded encrypted string."""
        if not plain_text:
            return ""
        return self.cipher.encrypt(plain_text.encode("utf-8")).decode("utf-8")

    def decrypt(self, encrypted_text: str) -> str:
        """Decrypts a base64 encoded encrypted string and returns the plain text."""
        if not encrypted_text:
            return ""
        return self.cipher.decrypt(encrypted_text.encode("utf-8")).decode("utf-8")


# Global encryptor instance
encryptor = DataEncryptor()
