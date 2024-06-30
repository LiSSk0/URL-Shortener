import random
import string
from db.orm_funcs import get_tokens, insert_to_db

all_tokens = []


# gets all tokens from DB, so they can be used for other funcs
def receive_all_tokens(engine):
    global all_tokens
    all_tokens = get_tokens(engine)


# generates unique token
def generate_token():
    characters = string.ascii_letters + string.digits

    token = ''.join(random.choices(characters, k=6))
    while token in all_tokens:
        token = ''.join(random.choices(characters, k=6))

    return token


# creates short url for long url
def create_short_url(engine, long_url):
    token = generate_token()
    all_tokens.append(token)
    insert_to_db(engine, long_url, token)

    # нужно будет вернуть готовую ссылку, а не просто токен:
    return token
