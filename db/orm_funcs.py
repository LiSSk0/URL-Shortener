import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Column, String, Date
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import psycopg2

from datetime import date, timedelta

EXPIRATION_TIME = 30  # url retention time (days), after which it will be deleted

SqlAlchemyBase = sqlalchemy.orm.declarative_base()


class UrlEntity(SqlAlchemyBase):
    def __init__(self, long_url, token, expiration_date):
        self.token = token
        self.long_url = long_url
        self.expiration_date = expiration_date

    __tablename__ = 'urls'
    long_url = Column(String, primary_key=True)
    token = Column(String)
    expiration_date = Column(Date)


class DataBase:
    def __init__(self, db_name, data):
        # creating connection to postgres
        connection = psycopg2.connect(user=data[0], password=data[1])
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # creating db if not
        cursor = connection.cursor()
        try:
            cursor.execute('create database ' + db_name)
        except psycopg2.errors.DuplicateDatabase:  # db has been already created
            pass

        cursor.close()
        connection.close()

        # dialect+driver://username:password@host:port/db_name
        # default parameters: echo=False, pool_size=5, max_overflow=10, encoding='UTF-8'
        connection_link = "postgresql+psycopg2://" + data[0] + ":" + data[1] + "@localhost/" + db_name

        # engine creating and connecting
        engine = create_engine(connection_link)
        engine.connect()
        metadata = MetaData()

        # creating the main table
        table = Table('urls', metadata,
                      Column('long_url', String, primary_key=True),
                      Column('token', String),
                      Column('expiration_date', Date))

        # init the table (if it doesn't exist)
        metadata.create_all(bind=engine)

        self.engine = engine

    def is_long_url_in_db(self, long_url):
        with Session(self.engine) as session:
            if session.query(UrlEntity).filter(UrlEntity.long_url == long_url).first():
                return True
            return False

    def is_token_in_db(self, token):
        with Session(self.engine) as session:
            if session.query(UrlEntity).filter(UrlEntity.token == token).first():
                return True
            return False

    def insert_to_db(self, long_url, token):
        current_date = date.today()  # .strftime("%d.%m.%Y")
        expiration_date = current_date + timedelta(days=EXPIRATION_TIME)  # "yyyy-mm-dd"

        result = self.is_long_url_in_db(long_url)  # объявление тут, чтобы не было двойного открытия сессии ниже
        with Session(self.engine) as session:
            if not result:
                session.add(UrlEntity(long_url, token, expiration_date))
                session.commit()
            else:
                print("!ERROR inserting: db/orm_funcs.py - insert_to_db: url '" + long_url + "' is already in db.")

    def get_table(self):
        table = []
        with Session(self.engine) as session:
            all_urls = session.query(UrlEntity).all()
            for url in all_urls:
                table.append((url.long_url, url.token, url.expiration_date))
        return table

    def print_table(self):
        table = self.get_table()
        for url in table:
            print(*url)

    def get_long_url_from_db(self, token):
        if not self.is_token_in_db(token):
            return None
        with Session(self.engine) as session:
            return session.query(UrlEntity.token).filter(UrlEntity.token == token).first()

    def get_token_from_db(self, long_url):
        if not self.is_long_url_in_db(long_url):
            return None
        with Session(self.engine) as session:
            return session.query(UrlEntity.token).filter(UrlEntity.long_url == long_url).first()

    def get_tokens(self):
        with Session(self.engine) as session:
            return session.query(UrlEntity.token).all()

    def delete_expired_urls(self):
        current_date = date.today()
        # current_date = date(2024, 10, 28)
        with Session(self.engine) as session:
            expired_urls = session.query(UrlEntity).filter(UrlEntity.expiration_date <= current_date)
            for url_obj in expired_urls:
                session.delete(url_obj)
                print(url_obj.long_url, "has been deleted. Expiration date was", url_obj.expiration_date)
            session.commit()
