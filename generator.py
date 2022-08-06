from secrets import choice
from string import ascii_letters, digits, punctuation


CHAR_TYPES = (ascii_letters, digits, punctuation)


def generate(length: int = 32):
    """Generates a password with ASCII letters, digits, and punctuation characters

    Args:
        length (int, optional): The length of the returned password 
            Defaults to 32.

    Returns:
        str: the generated password
    """

    password = ""
    for i in range(0, length):
        password = password + choice(choice(CHAR_TYPES))

    return password
