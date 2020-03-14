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
    site = input("What site do you need a password for? ").lower()
    sitePassword = createPassword()
    if isfile(site + "File.txt"):
        print(f"You already have credentials for {site}")
    else:
        siteFile = open(site + "File.txt", "w+")
        siteFile.write(f"{site} \n{sitePassword}")
        siteFile.close()


def getCredentials():
    site = input("Which site/application do you need credentials for? ").lower()
    if isfile(site + "File.txt"):
        siteFile = open(site + "File.txt", "r")
        siteFile = [item.replace("\n", "")for item in siteFile]
        password = siteFile[1]
        print(f"Site/Application: {site} \nPassword: {password}")
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


useApp()
