from tkinter import *
from random import choice
from os.path import isfile

# Setup for the GUI
root = Tk()
root.title("Password Manager")
root.geometry("1000x500")

class Application(Frame):
    # An interactive password manager
    def __init__(self, master):
        # Initialize the app's frame
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    # Creates the buttons
    def create_widgets(self):
        self.getCredentialsBtn = Button(self, text = "Get Credentials")
        self.getCredentialsBtn.grid()
        self.createCredentialsBtn = Button(self, text = "Create Credentials")
        self.createCredentialsBtn.grid()
        self.websiteLabel = Label(self)
        self.websiteLabel.grid()
        self.passwordLabel = Label(self)


app = Application(root)

def createPassword():
    password = ""
    words = open("words.txt", "r").readlines()
    words = [word.replace("\n", "_")for word in words]

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
    site = input("What site is this for? ").lower()
    sitePassword = createPassword()
    if isfile(site + "File.txt"):
        print(f"You already have credentials for {site}")
    else:
        siteFile = open(site + "File.txt", "w+")
        siteFile.write(f"{site} \n{sitePassword}")
        siteFile.close()


def getCredentials():
    site = input("Which application do you need credentials for? ").lower()
    if isfile(site + "File.txt"):
        siteFile = open(site + "File.txt", "r")
        siteFile = [item.replace("\n", "")for item in siteFile]
        password = siteFile[1]
        print(f"Site/Application: {site} \nPassword: {password}")
    else:
        print(f"You don't have any credentials stored for {site}")


root.mainloop()
