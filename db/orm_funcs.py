import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Column, String

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from datetime import date

DB_NAME = "db_url"
POSTGRE_USERNAME = "postgres"
POSTGRE_PASS = "2409"

SqlAlchemyBase = sqlalchemy.orm.declarative_base()  # ??


class Url(SqlAlchemyBase):
    def __init__(self, long_url, token, creation_date):
        self.token = token
        self.long_url = long_url
        self.creation_date = creation_date

    __tablename__ = 'urls'
    long_url = Column(String, primary_key=True)
    token = Column(String)
    creation_date = Column(String)


def create_db(db_name):
    # creating connection to postgres
    connection = psycopg2.connect(user=POSTGRE_USERNAME, password=POSTGRE_PASS)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # при использовании уровня изоляции транзакции
                                                                # ISOLATION_LEVEL_AUTOCOMMIT каждая операция INSERT,
                                                                # UPDATE, DELETE и т.д. будет автоматически
                                                                # фиксирована в базе данных без необходимости явного
                                                                # вызова команды COMMIT.

    # creating db if not
    cursor = connection.cursor()
    try:
        cursor.execute('create database ' + db_name)
    except psycopg2.errors.DuplicateDatabase:  # db has been already created
        pass
    cursor.close()
    connection.close()

    # cursor = connection.cursor()
    # is_created = cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    # print("val = ", is_created)
    # if not is_created:
    #     cursor.execute('create database ' + db_name)
    # else:
    #     print("already created")
    # cursor.close()
    # connection.close()


def connect_to_db(db_name):
    # dialect+driver://username:password@host:port/db_name
    # default parameters: echo=False, pool_size=5, max_overflow=10, encoding='UTF-8'
    connection_link = "postgresql+psycopg2://" + POSTGRE_USERNAME + ":" + POSTGRE_PASS + "@localhost/" + db_name

    # engine creating and connecting
    engine = create_engine(connection_link)
    engine.connect()  # print(engine)
    metadata = MetaData()

    # creating the main table
    table = Table('urls', metadata,
                  Column('long_url', String, primary_key=True),
                  Column('token', String),
                  Column('creation_date', String))

    # init the table (if it doesn't exist)
    metadata.create_all(bind=engine)
    # SqlAlchemyBase.metadata.create_all(engine)  # хз в чем отличие, но не работает

    return engine


def is_in_db(engine, long_url):
    with Session(engine) as session:
        if session.query(Url).filter(Url.long_url == long_url).first():
            return True
        return False


def insert_to_db(engine, long_url, token):
    current_date = date.today().strftime("%d.%m.%Y")

    # можно глобально прописать
    # session = sessionmaker(bind=engine)
    # и потом просто юзать session = Session()
    # но мне не хочется глобальные делать
    result = is_in_db(engine, long_url)  # объявление тут, чтобы не было двойного открытия сессии ниже
    with Session(engine) as session:
        if not result:
            session.add(Url(long_url, token, current_date))
            session.commit()
        else:
            print("!ERROR inserting: db/orm_funcs.py - insert_to_db: url '" + long_url + "' is already in db.")


def get_table(engine):
    table = []
    with Session(engine) as session:
        all_urls = session.query(Url).all()
        for url in all_urls:
            table.append((url.long_url, url.token, url.creation_date))
    return table


def print_db(engine):
    table = get_table(engine)
    for url in table:
        print(*url)


def get_token_from_db(engine, long_url):
    if not is_in_db(engine, long_url):
        return None
    with Session(engine) as session:
        return session.query(Url.token).filter(Url.long_url == long_url).first()[0]


create_db(DB_NAME)  # only when init, once
engine = connect_to_db(DB_NAME)
print_db(engine)
insert_to_db(engine, "https://test2.url/", "TEST2")
print(get_token_from_db(engine, "https://test.url/"))
print(get_token_from_db(engine, "https://test.url1/"))
# print_db(engine)
