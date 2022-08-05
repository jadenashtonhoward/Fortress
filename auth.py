import hashlib

from database import add_user, get_user_hash


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


if __name__ == "__main__":
    print("This program is not meant to be run on its own!")
