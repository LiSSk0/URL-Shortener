from db.orm_funcs import create_db, connect_to_db, is_in_db, get_token_from_db, print_table
from flask_http.flask_funcs import get_long_url, send_long_url
from url_convert.url_funcs import create_token, receive_all_tokens

DB_NAME = "db_url"

if __name__ == '__main__':

    create_db(DB_NAME)  # creating db if not
    engine = connect_to_db(DB_NAME)  # creating engine to manage db
    receive_all_tokens(engine)  # url_funcs.py needs engine to receive all tokens from db
    # print_table(engine)

    long_url = get_long_url()  # flask_http

    if is_in_db(engine, long_url):  # db
        url_short_token = get_token_from_db(engine, long_url)  # db
    else:
        url_short_token = create_token(engine, long_url)  # url

    send_long_url()  # flask_http / console print
