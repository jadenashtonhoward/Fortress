import sqlalchemy as sa

engine = sa.create_engine("sqlite+pysqlite:///:memory", future=True)

Base = sa.orm.declarative_base()


class User(Base):
    __tablename__ = "user_account"

    username = sa.Column(sa.String, primary_key=True)
    hash = sa.Column(sa.String)

    credentials = sa.orm.relationship("Credential", back_populates="user")

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, hash={self.hash!r})"


class Credential(Base):
    __tablename__ = "credential"

    name = sa.Column(sa.String, primary_key=True)
    username = sa.Column(sa.String)
    password = sa.Column(sa.String)
    owner = sa.Column(sa.String, sa.ForeignKey("user_account.username"))

    user = sa.orm.relationship("User", back_populates="credentials")

    def __repr__(self) -> str:
        return f"Credential(name={self.name!r}, username={self.username!r}, password={self.password!r}, owner={self.owner!r})"


Base.metadata.create_all(engine)

def add_user(username, pass_hash):
    user = User(username=username, hash=pass_hash)
    
    with sa.Session(engine) as session:
        session.add(user) # TODO: prevent repeat usernames
        session.commit()
    

def get_user_hash(username) -> str:
    hash = ""
    
    with sa.Session(engine) as session:
        for row in session.execute(sa.select(User.hash).where(User.username == username)):
            hash = row.hash # TODO: test!!!
            
    return hash


def add_credentials(fortress_user: str, name: str, username: str, password: str):
    pass


def get_credentials(name: str):
    pass


def update_credentials(fortress_user: str, new_password: str): 
    pass


def delete_credentials(fortress_user: str, name: str):
    pass


if __name__ == "__main__":
    print("This program is not meant to be run on its own!")