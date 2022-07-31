import hashlib
import database as db

from sys import exit
from generator import generate
from auth import signup, signin

pass_hash = hashlib.sha3_256("Password".encode("utf-8")).hexdigest() # code to hash passwords

def menu(message: str, *options: str) -> str:
    while True:    
        print(message)
        print("Here are your options:")
        for i in range(0, len(options)):
            print(f"    {options[i]}")
            
        option = input("Please select an operation. >> ")
        
        if option in options:
            return option
        
        print("Please select a valid operation! Capitalization matters.\n")
    
    
def main():

    print("""
    d88888b  .d88b.  d8888b. d888888b d8888b. d88888b .d8888. .d8888. 
    88'     .8P  Y8. 88  `8D `~~88~~' 88  `8D 88'     88'  YP 88'  YP 
    88ooo   88    88 88oobY'    88    88oobY' 88ooooo `8bo.   `8bo.   
    88~~~   88    88 88`8b      88    88`8b   88~~~~~   `Y8b.   `Y8b. 
    88      `8b  d8' 88 `88.    88    88 `88. 88.     db   8D db   8D 
    YP       `Y88P'  88   YD    YP    88   YD Y88888P `8888Y' `8888Y' 
          """)
    
    print("")

    option = menu("Welcome to Fortress!", "Sign In", "Sign Up")
    
    if option == "Sign In":
        signin()
    elif option == "Sign Up":
        signup()
        
    option = menu("Welcome to your fort!", "Fetch", "Add", "Update", "Delete")
    
    # TODO: add arguments and capture return values
    if option == "Fetch":
        db.get_credentials()
    elif option == "Add":
        db.add_credentials()
    elif option == "Update":
        db.update_credentials()
    elif option == "Delete":
        db.delete_credentials()

if __name__ == "__main__":
    main()