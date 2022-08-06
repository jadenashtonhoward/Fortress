import base64
import hashlib

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def create_hash(password: str) -> str:
    return hashlib.sha3_256(password.encode("utf-8")).hexdigest()


def create_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**15,
        r=8,
        p=1,
    )

    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def encrypt(password: str, owner_password: str, salt: bytes) -> str:
    f = Fernet(create_key(owner_password, salt))

    return f.encrypt(password.encode("utf-8"))


def decrypt(password: str, owner_password: str, salt: bytes) -> str:
    f = Fernet(create_key(owner_password, salt))

    return f.decrypt(password).decode("utf-8")
