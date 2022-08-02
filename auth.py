import hashlib

from database import add_user, get_user_hash


def signin() -> tuple:
    username = input("Please enter your username. >> ")
    pass_hash = hashlib.sha3_256(input("Please enter your password. >> ").encode("utf-8")).hexdigest()
    
    if pass_hash == get_user_hash(username):
        return True, username
    else:
        return False, None


def signup()-> tuple:
    username = input("What would you like your username to be? >> ")
    password_set = False
    password = ""
    
    while not password_set:
        password = input("What would you like your password to be? >> ")
        pass_confirmation = input("Please confirm your password. >> ")

        if password == pass_confirmation:
            password_set = True
        
        print("Your passwords do not match!")
    
    
    pass_hash = hashlib.sha3_256(f"{password}".encode("utf-8")).hexdigest()
    
    add_user(username, pass_hash)
    
    return True, username
    
    

if __name__ == "__main__":
    print("This program is not meant to be run on its own!")