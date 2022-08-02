import database as db

from sys import exit
from generator import generate
from auth import signup, signin


def menu(message: str, *options: str) -> str:
    while True:    
        print(message)
        print("Here are your options:")
        
        for i in range(0, len(options)):
            print(f"    {options[i]}")
        
        print("     Exit")
            
        option = input("Please select an operation. >> ")
        
        if option == "Exit":
            exit()
        elif option in options:
            print()
            return option
        
        print("Please select a valid operation! Capitalization matters.\n")
    
    
def main():
    authenticated = False
    user = ""

    print("""
    d88888b  .d88b.  d8888b. d888888b d8888b. d88888b .d8888. .d8888. 
    88'     .8P  Y8. 88  `8D `~~88~~' 88  `8D 88'     88'  YP 88'  YP 
    88ooo   88    88 88oobY'    88    88oobY' 88ooooo `8bo.   `8bo.   
    88~~~   88    88 88`8b      88    88`8b   88~~~~~   `Y8b.   `Y8b. 
    88      `8b  d8' 88 `88.    88    88 `88. 88.     db   8D db   8D 
    YP       `Y88P'  88   YD    YP    88   YD Y88888P `8888Y' `8888Y' 
          """)
    
    print("")
    
    while not authenticated:
        option = menu("Welcome to Fortress!", "Sign In", "Sign Up")
        
        if option == "Sign In":
            authenticated, user = signin()
        elif option == "Sign Up":
            authenticated, user = signup()
        
    option = menu("Welcome to your fort!", "Add", "Fetch", "Update", "Delete")
    
    # TODO: add arguments and capture return values
    if option == "Add":
        cred_name = input("What is this credential for? >> ")
        cred_username = input("What is your username for this credential? >> ")
        password_length = int(input("How long would you like your password to be? >> ")) # TODO: error checking
        cred_password = generate(password_length)
        print(f"Your generated password: {cred_password}")
        db.add_credentials(user, cred_name, cred_username, cred_password) # TODO: encrypt password
    elif option == "Fetch":
        print(db.get_credentials(user))
    elif option == "Update":
        db.update_credentials(user, str)
    elif option == "Delete":
        db.delete_credentials(user, str)

if __name__ == "__main__":
    main()