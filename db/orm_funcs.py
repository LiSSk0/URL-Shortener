import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Column, String, Date

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from datetime import date, timedelta

EXPIRATION_TIME = 30  # url retention time (days), after which it will be deleted

SqlAlchemyBase = sqlalchemy.orm.declarative_base()  # ??


class Url(SqlAlchemyBase):
    def __init__(self, long_url, token, expiration_date):
        self.token = token
        self.long_url = long_url
        self.expiration_date = expiration_date

    __tablename__ = 'urls'
    long_url = Column(String, primary_key=True)
    token = Column(String)
    expiration_date = Column(Date)


def create_db(db_name, data):
    # creating connection to postgres
    connection = psycopg2.connect(user=data[0], password=data[1])
    # except (psycopg2.OperationalError, sqlalchemy.exc.OperationalError):
    #    print("!ERROR bad credentials: db/orm_funcs.py - create_db.")
    #    return False

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


def connect_to_db(db_name, data):
    # dialect+driver://username:password@host:port/db_name
    # default parameters: echo=False, pool_size=5, max_overflow=10, encoding='UTF-8'
    connection_link = "postgresql+psycopg2://" + data[0] + ":" + data[1] + "@localhost/" + db_name

    # engine creating and connecting
    engine = create_engine(connection_link)
    engine.connect()  # print(engine)
    metadata = MetaData()

    # creating the main table
    table = Table('urls', metadata,
                  Column('long_url', String, primary_key=True),
                  Column('token', String),
                  Column('expiration_date', Date))

    # init the table (if it doesn't exist)
    metadata.create_all(bind=engine)
    # SqlAlchemyBase.metadata.create_all(engine)  # хз в чем отличие, но не работает

    return engine


def is_long_url_in_db(engine, long_url):
    with Session(engine) as session:
        if session.query(Url).filter(Url.long_url == long_url).first():
            return True
        return False


def is_token_in_db(engine, token):
    with Session(engine) as session:
        if session.query(Url).filter(Url.token == token).first():
            return True
        return False


def insert_to_db(engine, long_url, token):
    current_date = date.today()  # .strftime("%d.%m.%Y")
    expiration_date = current_date + timedelta(days=EXPIRATION_TIME)  # "yyyy-mm-dd"

    # можно глобально прописать
    # session = sessionmaker(bind=engine)
    # и потом просто юзать session = Session()
    # но мне не хочется глобальные делать
    result = is_long_url_in_db(engine, long_url)  # объявление тут, чтобы не было двойного открытия сессии ниже
    with Session(engine) as session:
        if not result:
            session.add(Url(long_url, token, expiration_date))
            session.commit()
        else:
            print("!ERROR inserting: db/orm_funcs.py - insert_to_db: url '" + long_url + "' is already in db.")


def get_table(engine):
    table = []
    with Session(engine) as session:
        all_urls = session.query(Url).all()
        for url in all_urls:
            table.append((url.long_url, url.token, url.expiration_date))
    return table


def print_table(engine):
    table = get_table(engine)
    for url in table:
        print(*url)


def get_long_url_from_db(engine, token):
    if not is_token_in_db(engine, token):
        return None
    with Session(engine) as session:
        return session.query(Url.token).filter(Url.token == token).first()


def get_token_from_db(engine, long_url):
    if not is_long_url_in_db(engine, long_url):
        return None
    with Session(engine) as session:
        return session.query(Url.token).filter(Url.long_url == long_url).first()


def get_tokens(engine):
    with Session(engine) as session:
        return session.query(Url.token).all()


def deleting_expired_urls(engine):
    current_date = date.today()
    # current_date = date(2024, 10, 28)
    with Session(engine) as session:
        expired_urls = session.query(Url).filter(Url.expiration_date <= current_date)
        for url_obj in expired_urls:
            session.delete(url_obj)
            print(url_obj.long_url, "has been deleted. Expiration date was", url_obj.expiration_date)
        session.commit()
