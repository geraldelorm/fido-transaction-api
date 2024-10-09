from cryptography.fernet import Fernet
from loguru import logger

from app.config.config import SECRET_KEY

# Ensure SECRET_KEY is a string
if isinstance(SECRET_KEY, bytes):
    ENCRYPTION_KEY = SECRET_KEY.decode()
else:
    ENCRYPTION_KEY = str(SECRET_KEY)

if not ENCRYPTION_KEY:
    # If the key is not found, generate a new one and log a warning
    logger.warning(
        "ENCRYPTION_KEY not found in environment variables. Generating a new key."
    )
    ENCRYPTION_KEY = Fernet.generate_key().decode()

cipher_suite = Fernet(ENCRYPTION_KEY.encode())


def encrypt_data(data: str) -> str:
    """Encrypt the data using Fernet encryption."""
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt the data using Fernet decryption."""
    logger.info(f"Decrypting data: {encrypted_data}")
    data = cipher_suite.decrypt(encrypted_data.encode()).decode()
    logger.info(f"Done decrypting data")
    return data
