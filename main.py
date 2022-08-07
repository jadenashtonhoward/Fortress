import database as db

from sys import exit
from typing import Tuple, List


def ensure_credentials(owner: str) -> Tuple[bool, List[str]]:
    """Ensures that the user has credentials before trying to work on them
    """

    credentials = db.get_all_credentials(owner)

    if len(credentials) == 0:
        return False, credentials
    else:
        return True, credentials


def display_credentials(owner: str) -> bool:
    """If the user has credentials, displays them

    Args:
        owner (str): the username of the User
    """

    has_credentials, credentials = ensure_credentials(owner)

    if has_credentials:
        for i in range(0, len(credentials)):
            if i % 3 == 0:
                print()
            print(credentials[i].name, end=" ")

        print()

        return True
    else:
        print("You don't have any credentials!")
        return False


def main():

    print("""
        d88888b  .d88b.  d8888b. d888888b d8888b. d88888b .d8888. .d8888. 
        88'     .8P  Y8. 88  `8D `~~88~~' 88  `8D 88'     88'  YP 88'  YP 
        88ooo   88    88 88oobY'    88    88oobY' 88ooooo `8bo.   `8bo.   
        88~~~   88    88 88`8b      88    88`8b   88~~~~~   `Y8b.   `Y8b. 
        88      `8b  d8' 88 `88.    88    88 `88. 88.     db   8D db   8D 
        YP       `Y88P'  88   YD    YP    88   YD Y88888P `8888Y' `8888Y' 
    """)

    print("\nWelcome to Fortress!")

    owner = ""
    owner_password = ""

    authenticated = False

    while not authenticated:
        option = ""

        while option not in ("signin", "signup"):
            option = input("Would you like to SignIn or SignUp? >> ").lower()

        owner = input("Username >> ")
        owner_password = input("Password >> ")

        if option == "signin":
            authenticated = db.compare_hash(owner, owner_password)
        elif option == "signup":
            authenticated = db.add_user(owner, owner_password)

            if not authenticated:
                print("An account with that username already exists!")

        print()

    print("Welcome to your Fort!")
    print()

    while True:
        option = ""

        while True:
            option = input(
                "Would you like to Add, Get, Update, Delete, or Exit? >> ").lower()

            if option in ("add", "get", "update", "delete", "exit"):
                break
            else:
                print("Invalid option, try again!")

        print()

        if option == "add":
            name = input("What will this credential be called? >> ")
            username = input("What is your username for this credential? >> ")

            print(
                f"Your password for {name} is {db.add_credential(name, username, owner, owner_password)}")

        elif option == "get":
            if not display_credentials(owner):
                continue

            name = input("Which credential would you like to view? >> ")

            print(db.get_credential(name, owner, owner_password))

        elif option == "update":
            if not display_credentials(owner):
                continue

            name = input("What credential should be updated? >> ")

            db.update_credential(name, owner, owner_password)

        elif option == "delete":
            if not display_credentials(owner):
                continue

            name = input("Which credential should be deleted? >> ")

            db.delete_credential(name, owner)

        elif option == "exit":
            exit()

        print()


if __name__ == "__main__":
    main()
