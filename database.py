# TODO: encrypt passwords

import sqlalchemy as sa

engine = sa.create_engine("sqlite+pysqlite:///:memory", echo=True, future=True)

metadata_obj = sa.MetaData()

user_table = sa.Table(
    "user_account",
    metadata_obj,
    sa.Column('name', sa.String(30), primary_key=True),
    sa.Column('pass_hash', sa.String)
)

credentials_table = sa.Table(
    "credentials",
    metadata_obj,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String),
    sa.Column("username", sa.String),
    sa.Column("password", sa.String),
    sa.Column("fortress_name", sa.ForeignKey(
        "user_account.name"), nullable=False)
)

metadata_obj.create_all(engine)


def add_user(name: str, pass_hash: str):
    with engine.connect() as conn:
        result = conn.execute(
            sa.insert(user_table),
            [
                {"name": name, "pass_hash": pass_hash}
            ]
        )
        conn.commit()


def get_user_hash(name: str):
    with engine.connect() as conn:
        return conn.execute(sa.select(user_table.c.pass_hash).
                            where(user_table.c.name == name))


def add_credentials(name: str, username: str, password: str, fortress_name: str):
    with engine.connect() as conn:
        result = conn.execute(
            sa.insert(credentials_table),
            [
                {
                    "name": name,
                    "username": username,
                    "password": password,
                    "fortress_name": fortress_name
                }
            ]
        )
        conn.commit()


def get_credentials(name: str):
    with engine.connect() as conn:
        return conn.execute(sa.select(credentials_table).
                            where(credentials_table.c.fortress_name == name))


def update_credentials(fortress_name: str, new_password: str):
    with engine.connect() as conn:
        conn.execute(
            sa.update(credentials_table).where(user_table.c.fortress_name == fortress_name).
            values(password=new_password)
        )
        conn.commit()


def delete_credentials(name: str):
    with engine.connect() as conn:
        conn.execute(
            sa.delete(credentials_table).
            where(credentials_table.c.name == name)
        )
        conn.commit()
