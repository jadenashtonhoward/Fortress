import security
import sqlalchemy as sa
import sqlalchemy.orm as orm

from os import urandom
from typing import List
from generator import generate

engine = sa.create_engine("sqlite+pysqlite:///database.db", future=True)

Session = orm.sessionmaker(engine, future=True)

Base = orm.declarative_base()

# region CLASSES


class User(Base):
    __tablename__ = "user_account"

    username = sa.Column(sa.String(32), primary_key=True)
    hash = sa.Column(sa.String)
    salt = sa.Column(sa.String)

    credentials = orm.relationship(
        "Credential",
        back_populates="user",
        order_by="Credential.name",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, hash={self.hash!r}, salt={self.salt!r})"


class Credential(Base):
    __tablename__ = "credential"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(32))
    username = sa.Column(sa.String(32))
    password = sa.Column(sa.String)
    owner = sa.Column(sa.String, sa.ForeignKey("user_account.username"))

    user = orm.relationship("User", back_populates="credentials")

    def __repr__(self) -> str:
        return f"Credential(name={self.name!r}, username={self.username!r}, password={self.password!r})"


Base.metadata.create_all(engine)

# endregion

# region USER FUNCTIONS


def add_user(username: str, password: str) -> bool:
    """Adds a user to the database

    Args:
        username (str): the user's username
        password (str): the user's password

    Returns:
        bool: True if user was added, False if not
    """

    user = User(username=username, hash=security.create_hash(
        password), salt=urandom(16))

    try:
        with Session.begin() as session:
            session.add(user)

        return True
    except:
        return False


def delete_user(username: str) -> None:
    """Deletes a user from the database

    Args:
        username (str): the username of the User that will be deleted
    """

    with Session.begin() as session:
        user = session.get(User, username)

        session.delete(user)


def get_user_hash(username: str) -> str:
    """Retreives a user's password hash from the database

    Args:
        username (str): the user's username

    Returns:
        str: the hash of the user's password
    """

    with Session() as session:
        hash = session.scalars(
            sa.select(User.hash).where(User.username == username)
        ).one()

    return hash


def compare_hash(username: str, password: str) -> bool:
    """Compares a password's hash to a user's stored hash

    Args:
        username (str): the User's username
        password (str): the password entered by the User

    Returns:
        bool: True if the password matches the stored hash, False if not
    """

    if security.create_hash(password) == get_user_hash(username):
        return True
    else:
        return False


def get_user_salt(username: str) -> bytes:
    """Retreives a user's salt from the database

    Args:
        username (str): the user's username

    Returns:
        str: the user's salt
    """

    salt = ""

    with Session() as session:
        salt = session.scalars(
            sa.select(User.salt).where(User.username == username)
        ).one()

    return salt


# endregion

# region CREDENTIAL FUNCTIONS

def add_credential(name: str, username: str, owner: str, owner_password: str) -> str:
    """Adds a credential to the database

    Args:
        name (str): the credential's name
        username (str): the username to be stored
        owner (str): the username of the User that owns the credential
        owner_password (str): the password of the User that owns the credential

    Returns:
        str: the password stored in the credential
    """

    password = generate()

    with Session.begin() as session:
        try:
            password = session.scalars(
                sa.select(Credential.password).where(Credential.name ==
                                                     name and Credential.owner == owner)
            ).one()

            return f"{password}, but that credential already existed! If you would like to change it, try using Update."
        except:
            pass

        user = session.scalars(
            sa.select(User).where(User.username == owner)
        ).one()

        user.credentials.append(
            Credential(
                name=name,
                username=username,
                password=security.encrypt(
                    password, owner_password, get_user_salt(owner)
                ),
                owner=owner
            )
        )

    return password


def get_all_credentials(owner: str) -> List[str]:
    """Retrieves all of a user's credential names

    Args:
        owner (str): the username of the credential's owner

    Returns:
        List[str]: a list of credential names
    """

    with Session() as session:
        credentials = session.scalars(sa.select(Credential).join(
            Credential.user).where(User.username == owner)).all()

    return credentials


def get_credentials_size(owner: str) -> int:
    """Retreives the amount of credentials a User has

    Args:
        owner (str): the username of the User being checked

    Returns:
        int: the amount of credentials belonging to the User
    """

    return len(get_all_credentials(owner))


def get_credential(name: str, owner: str, owner_password: str) -> str:
    """Retrieves a user's credential by its name

    Args:
        name (str): the name of the credential
        owner (str): the username of the User that owns the credential

    Returns:
        str: a string containing the credential name, username, and password
    """

    with Session() as session:
        username = session.scalars(sa.select(Credential.username).where(
            Credential.name == name and Credential.owner == owner)).one()

        password = session.scalars(sa.select(Credential.password).where(
            Credential.name == name and Credential.owner == owner)).one()

    password = security.decrypt(
        password,
        owner_password,
        get_user_salt(owner)
    )

    return f"Your username for {name} is {username} and your password is {password}"


def delete_credential(name: str, owner: str) -> None:
    """Selects a credential by its name and owner and deletes it

    Args:
        name (str): the name of the credential
        owner (str): the username of the User that owns the credential
    """

    with Session.begin() as session:
        user = session.get(User, owner)

        user.credentials.remove(
            session.scalars(sa.select(Credential).where(
                Credential.name == name).where(Credential.owner == owner)).one()
        )


def update_credential(name: str, owner: str, owner_password: str) -> str:
    """Selects a credential by its name and owner and generates a new password for it

    Args:
        name (str): the name of the credential
        owner (str): the username of the User that owns the credential
        owner_password (str): the password of the User that owns the credential

    Returns:
        str: the new password stored in the credential
    """

    with Session() as session:
        username = session.scalars(
            sa.select(Credential.username).where(
                Credential.name == name).where(Credential.owner == owner)
        ).one()

    delete_credential(name, owner)
    return add_credential(name, username, owner, owner_password)

# endregion

# region TESTING FUNCTIONS


def run_tests() -> str:
    print(f"{security.create_hash('test')=}")
    add_user("test", "test")
    print(f"{get_user_hash('test')=}")
    print(f"{get_user_salt('test')=}")

    print(f"{add_credential('test', 'test', 'test', 'test')=}")
    print(f"{add_credential('test1', 'test', 'test', 'test')=}")
    print(f"{add_credential('test2', 'test', 'test', 'test')=}")

    print(f"{get_all_credentials('test')=}")
    print(f"{get_credential('test', 'test', 'test')=}")
    print(f"{get_credential('test1', 'test', 'test')=}")
    print(f"{get_credential('test2', 'test', 'test')=}")

    delete_credential('test2', 'test')

    print(f"{update_credential('test1', 'test', 'test')=}")
    print(f"{get_credential('test1', 'test', 'test')=}")

    delete_user("test")


# endregion

if __name__ == "__main__":
    print(run_tests())
