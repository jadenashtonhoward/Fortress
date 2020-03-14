from random import choice
from os.path import isfile

def createPassword():
    password = ""
    words = open("words.txt", "r").readlines()
    words = [word.replace("\n", "_")for word in words]

    for i in range(0,6):
        usable = False
        while usable != True:
            word = choice(words)
            if len(word) < 5:
                usable = False
                words.remove(word)
            else:
                usable = True
        password += word
        words.remove(word)

    password = password[:-1]

    return(password)


def createCredentials():
    site = input("What site do you need a password for? ")
    sitePassword = createPassword()
    if isfile(site.lower() + "File.txt"):
        print(f"You already have credentials for {site}")
    else:
        siteFile = open(site.lower() + "File.txt", "w+")
        siteFile.write(f"Website/Application: \n{site} \nPassword: \n{sitePassword}")
        siteFile.close()


def getCredentials():
    site = input("Which site do you need credentials for? ")
    if isfile(site.lower() + "File.txt"):
        siteFile = open(site + "File.txt", "r")
    else:
        print(f"You don't have any credentials stored for {site}")


def useApp():
    userInput = input("Would you like to MAKE or GET credentials? ")
    if userInput.upper() == "MAKE":
        createCredentials()
    elif userInput.upper() == "GET":
        getCredentials()
    else:
        print("Please input either MAKE or GET")
