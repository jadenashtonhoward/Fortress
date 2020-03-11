from random import choice

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

    print(password)


createPassword()