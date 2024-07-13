import random
import string
import re


# generates unique token
def generate_token(db):
    all_tokens = db.get_tokens()
    characters = string.ascii_letters + string.digits

    token = ''.join(random.choices(characters, k=6))
    while token in all_tokens:
        token = ''.join(random.choices(characters, k=6))

    return token


# creates token for long url
def create_short_url(db, long_url):
    token = generate_token(db)
    db.insert_to_db(long_url, token)
    return token


# checks if the url is correct
def check_long_url(url):
    pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$'
    if re.match(pattern, url):
        return True
    return False
