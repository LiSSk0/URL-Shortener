import random
import string
from db.orm_funcs import get_tokens, insert_to_db


# generates unique token
def generate_token(engine):
    all_tokens = get_tokens(engine)
    characters = string.ascii_letters + string.digits

    token = ''.join(random.choices(characters, k=6))
    while token in all_tokens:
        token = ''.join(random.choices(characters, k=6))

    return token


# creates short url for long url
def create_short_url(engine, long_url):
    token = generate_token(engine)
    insert_to_db(engine, long_url, token)
    return token
