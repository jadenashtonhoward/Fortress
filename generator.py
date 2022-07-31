from secrets import choice
from string import ascii_letters, digits, punctuation


CHAR_TYPES = (ascii_letters, digits, punctuation)

def generate(length: int = 12):
    """Generates a passowrd with ASCII letters, digits, and punctuation characters

    Args:
        length (int, optional): The length of the returned password. 
            Defaults to 12.

    Returns:
        str: the generated password
    """
    
    password = ""
    for i in range(0, length):
        password = password + choice(choice(CHAR_TYPES))
        
    return password


if __name__ == "__main__":
    print("This program is not meant to be run!")