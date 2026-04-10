import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # Step 1: SHA256 (no length limit)
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()

    # Step 2: bcrypt
    return pwd_context.hash(sha256_hash)

def verify_password(plain: str, hashed: str):
    sha256_hash = hashlib.sha256(plain.encode()).hexdigest()
    return pwd_context.verify(sha256_hash, hashed)