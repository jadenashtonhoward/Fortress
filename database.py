import sqlalchemy as sa
import sqlalchemy.orm as orm

engine = sa.create_engine("sqlite+pysqlite:///:memory", future=True)

Base = orm.declarative_base()


class User(Base):
    __tablename__ = "user_account"

    username = sa.Column(sa.String, primary_key=True)
    hash = sa.Column(sa.String)
    salt = sa.Column(sa.String)

    credentials = orm.relationship("Credential", back_populates="user")

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, hash={self.hash!r})"


class Credential(Base):
    __tablename__ = "credential"

    name = sa.Column(sa.String, primary_key=True)
    username = sa.Column(sa.String)
    password = sa.Column(sa.String)
    owner = sa.Column(sa.String, sa.ForeignKey("user_account.username"))

    user = orm.relationship("User", back_populates="credentials")

    def __repr__(self) -> str:
        return f"Credential(name={self.name!r}, username={self.username!r}, password={self.password!r}, owner={self.owner!r})"


Base.metadata.create_all(engine)

# database functions


def add_user(username, pass_hash) -> None:
    user = User(username=username, hash=pass_hash, salt=urandom(16))

    with orm.Session(engine) as session:
        session.add(user)
        session.commit()


def get_user_hash(username) -> str:
    hash = ""

    with orm.Session(engine) as session:
        for row in session.execute(sa.select(User.hash).where(User.username == username)):
            hash = row.hash

    return hash


def get_user_salt(username) -> bytes:
    salt = ""

    with orm.Session(engine) as session:
        for row in session.execute(sa.select(User.salt).where(User.username == username)):
            salt = row.salt

    return salt


def add_credentials(name: str, username: str, password: str, owner: str, owner_password: str) -> None:

    credential = Credential(name=name, username=username,
                            password=encrypt_password(password, owner, owner_password), owner=owner)

    with orm.Session(engine) as session:
        session.add(credential)
        session.commit()


def fetch_credentials_list(owner: str) -> list:
    creds = []

    with orm.Session(engine) as session:
        for row in session.execute(
            sa.select(Credential.name).where(Credential.owner == owner)
        ):
            creds.append(row)

    return creds


def fetch_credential(name: str, owner: str, owner_password: str) -> tuple:

    cred = ()

    with orm.Session(engine) as session:
        for row in session.execute(sa.select(Credential).
                                   where(Credential.name == name and
                                         Credential.owner == owner)):
            cred = row[0].name, decrypt_password(
                row[0].password, owner, owner_password)

    return cred


def update_credentials(name: str, new_password: str, owner: str, owner_password: str):

    with orm.Session(engine) as session:
        for row in session.execute(sa.select(Credential).
                                   where(Credential.name == name and
                                         Credential.owner == owner)):
            row[0].password = encrypt_password(
                new_password, owner, owner_password)

        session.commit()


def delete_credentials(name: str, owner: str, owner_password: str):
    from auth import hash_password

    if hash_password(owner_password) == get_user_hash(owner):
        with orm.Session(engine) as session:
            for row in session.execute(sa.select(Credential).where(
                    Credential.name == name and Credential.owner == owner)):

                session.delete(row[0])

            session.commit()


if __name__ == "__main__":
    print("This program is not meant to be run on its own!")
