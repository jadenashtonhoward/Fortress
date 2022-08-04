import database as db

from sys import exit
from generator import generate
from auth import sign_up, sign_in


def menu(message: str, *options: str) -> str:
    while True:
        print(message)
        print("Here are your options:")

        for i in range(0, len(options)):
            print(f"\t{options[i]}")

        print("\tExit")

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
            authenticated, user = sign_in()
        elif option == "Sign Up":
            authenticated, user = sign_up()

    option = menu("Welcome to your fort!", "Add", "Fetch", "Update", "Delete")
    # TODO: display list (on multiple lines)
    db.fetch_credentials_list(username)

    if option == "Add":

        name = input("What is this credential for? >> ")
        username = input("What will your username be? >> ")
        # TODO: error checking
        length = int(input("How long do you want your password to be? >> "))

        password = generate(length)

        print(f"Your password for {name} is {password}")

        db.add_credentials(user, name, username, password)

    elif option == "Fetch":

        name = input("Which credential would you like to view? >> ")
        print(db.fetch_credential(name, username))

    elif option == "Update":

        name = input("Which credential would you like to update? >> ")
        length = int(input("How long do you want your password to be? >> "))
        password = generate(length)
        print(f"Your new password for {name} is {password}")
        db.update_credentials(name, password, username)

    elif option == "Delete":

        name = input("Which credential would you like to delete? >> ")
        print(f"You are attempting to delete your credential: {name}")
        password = input("Please input your Fortress password to confirm. >> ")

        db.delete_credentials(name, username, password)


if __name__ == "__main__":
    main()
