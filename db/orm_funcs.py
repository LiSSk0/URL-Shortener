import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy import create_engine, MetaData, Table, Column, String

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

POSTGRE_USERNAME = "postgres"
POSTGRE_PASS = "2409"


def create_db():
    # creating connection to postgres
    connection = psycopg2.connect(user=POSTGRE_USERNAME, password=POSTGRE_PASS)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # при использовании уровня изоляции транзакции
                                                                # ISOLATION_LEVEL_AUTOCOMMIT каждая операция INSERT,
                                                                # UPDATE, DELETE или т.д. будет автоматически
                                                                # фиксирована в базе данных без необходимости явного
                                                                # вызова команды COMMIT.

    cursor = connection.cursor()
    cursor.execute('create database db_url')
    cursor.close()
    connection.close()

    # dialect+driver://username:password@host:port/db_name
    # default parameters: echo=False, pool_size=5, max_overflow=10, encoding='UTF-8'
    connection_link = "postgresql+psycopg2://" + POSTGRE_USERNAME + ":" + POSTGRE_PASS + "@localhost/db_url"
    engine = create_engine(connection_link)
    engine.connect()
    metadata = MetaData()

    # print(engine)

    table = Table(
        'urls',
        metadata,
        Column('token', String, primary_key=True),
        Column('long_url', String),
        Column('creation_date', String)
    )

    # creating the table (if it doesn't exist)
    metadata.create_all(bind=engine)

    return engine, table


def insert_to_db(engine, table):
    insert_query = table.insert().values(token='', long_url='', creation_date='')
    with engine.connect() as connection:
        connection.execute(insert_query)


def print_db(engine, table):
    select_query = table.select()
    with engine.connect() as connection:
        result = connection.execute(select_query)
        for row in result:
            print(row)


def is_in_db(url_long):
    return True


def get_short_url_from_db(url_long):
    return "https://short.url"
