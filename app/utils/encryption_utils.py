# app/utils/encryption_utils.py

from cryptography.fernet import Fernet

# Generate a key for encryption
# In a real application, store this key securely and retrieve it from an environment variable or a secure vault
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_data(data: str) -> str:
    """Encrypt the data using Fernet encryption."""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt the data using Fernet decryption."""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()
