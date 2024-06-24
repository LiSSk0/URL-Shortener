import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Column, String

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from datetime import date

POSTGRE_USERNAME = "postgres"
POSTGRE_PASS = "2409"

SqlAlchemyBase = sqlalchemy.orm.declarative_base()  # ??


class Url(SqlAlchemyBase):
    def __init__(self, token, long_url, creation_date):
        self.token = token
        self.long_url = long_url
        self.creation_date = creation_date

    __tablename__ = 'urls'
    long_url = Column(String, primary_key=True)
    token = Column(String)
    creation_date = Column(String)


def create_db():
    # creating connection to postgres
    connection = psycopg2.connect(user=POSTGRE_USERNAME, password=POSTGRE_PASS)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # при использовании уровня изоляции транзакции
                                                                # ISOLATION_LEVEL_AUTOCOMMIT каждая операция INSERT,
                                                                # UPDATE, DELETE и т.д. будет автоматически
                                                                # фиксирована в базе данных без необходимости явного
                                                                # вызова команды COMMIT.

    # creating db
    cursor = connection.cursor()
    try:
        cursor.execute('create database db_url')
    except psycopg2.errors.DuplicateDatabase:  # db has been already created
        pass
    cursor.close()
    connection.close()

    # dialect+driver://username:password@host:port/db_name
    # default parameters: echo=False, pool_size=5, max_overflow=10, encoding='UTF-8'
    connection_link = "postgresql+psycopg2://" + POSTGRE_USERNAME + ":" + POSTGRE_PASS + "@localhost/db_url"

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
    # SqlAlchemyBase.metadata.create_all(engine)  # хз в чем отличие, но это не работает

    # cursor.execute("insert into db_url (token, long_url, creating_date) values ('TEST2', 'https', '24.02')")
    # cursor.close()
    # connection.close()

    return engine, table


def insert_to_db(engine, table, long_url, token):
    current_date = date.today().strftime("%d.%m.%Y")

    # можно глобально прописать
    # session = sessionmaker(bind=engine)
    # и потом просто юзать session = Session()
    # но мне понятнее каждый раз прописывать engine
    with Session(engine) as session:

        # url = Url()
        # url.token = token
        # url.long_url = long_url
        # url.current_date = current_date
        try:
            session.add(Url(long_url, token, current_date))
        except sqlalchemy.exc.IntegrityError:  # long_url is already in table
            pass
        except psycopg2.errors.UniqueViolation:  # long_url is already in table
            pass

        session.commit()  # print(session.new)


def print_db(engine, table):
    select_query = table.select()
    with engine.connect() as connection:
        result = connection.execute(select_query)
        for row in result:
            print(row)


def is_in_db(engine, table, long_url):
    select_query = table.select(where=long_url)
    with engine.connect() as connection:
        result = connection.execute(select_query)
    if result:
        return True
    return False


def get_short_url_from_db(url_long):
    return "https://short.url"


engine, table = create_db()
print_db(engine, table)
insert_to_db(engine, table, "https://test.url/", "TEST1")
print_db(engine, table)
