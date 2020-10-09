from random import choice
from os.path import isfile

def createPassword():

    # initializes the password and creates a list of words from all of the words in words.txt
    password = ""
    words = open("words.txt", "r").readlines()
    words = [word.replace("\n", "_") for word in words]

    for i in range(0, 6):

        usable = False

        while not usable:

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

    site = input("Site/Application Name: ").upper()

    if isfile(site + "_File.txt"):
        print(f"You already have credentials for {site}, GET them instead")

    else:
        sitePassword = createPassword()
        siteFile = open(site + "_File.txt", "w+")
        siteFile.write(f"{site} \n{sitePassword}")
        siteFile.close()
        print(f"The password that was created is {sitePassword}")


def getCredentials():

    site = input("Site/Application Name: ").upper()

    if isfile(site + "_File.txt"):
        siteFile = open(site + "_File.txt", "r")
        siteFile = [item.replace("\n", "") for item in siteFile]
        password = siteFile[1]
        siteFile.close()
        print(f"Site/Application: {site} \nPassword: {password}")

    else:
        print(f"You don't have any credentials stored for {site}, CREATE some instead")

def useApp():

    using = True

    while using:

        task = input("CREATE, GET, or CLOSE? ").upper()

        if task == "CREATE":
            createCredentials()
        elif task == "GET":
            getCredentials()
        elif task == "CLOSE":
            using = False
        else:
            print("That operation is not supported by this application, please use either GET, CREATE, or CLOSE")


useApp()
