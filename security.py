import hashlib
import base64

from database import add_user, get_user_hash

from os import urandom
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def hash_password(password: str):
    return hashlib.sha3_256(password.encode("utf-8")).hexdigest()


def sign_in() -> tuple:
    username = input("Please enter your username. >> ")
    password = input("Please enter your password. >> ")
    pass_hash = hash_password(password)

    if pass_hash == get_user_hash(username):
        return True, username, password
    else:
        return False, "", ""


def sign_up() -> tuple:
    username = input("What would you like your username to be? >> ")
    password_set = False
    password = ""

    while not password_set:
        password = input("What would you like your password to be? >> ")
        pass_confirmation = input("Please confirm your password. >> ")

        if password == pass_confirmation:
            password_set = True
        else:
            print("Your passwords do not match!")

    pass_hash = hash_password(password)

    add_user(username, pass_hash)

    return True, username, password


# encryption functions

def create_key(owner: str, owner_password: str) -> bytes:
    kdf = Scrypt(
        salt=get_user_salt(owner),
        length=32,
        n=2**20,
        r=8,
        p=1,
    )

    return base64.urlsafe_b64encode(kdf.derive(owner_password.encode("utf-8")))


def encrypt_password(password: str, owner: str, owner_password: str) -> str:
    key = create_key(owner, owner_password)

    f = Fernet(key)

    return str(f.encrypt(password.encode("utf-8")))


def decrypt_password(password: str, owner: str, owner_password: str) -> str:
    key = create_key(owner, owner_password)

    f = Fernet(key)

    return str(f.decrypt(password.encode("utf-8")))


if __name__ == "__main__":
    print("This program is not meant to be run on its own!")
