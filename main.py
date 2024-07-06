from db.orm_funcs import create_db, connect_to_db , get_token_from_db, print_table
from flask_http.flask_funcs import app, process, input_long_url
# from url_convert.url_funcs import create_token, receive_all_tokens
import sys
from db.credentials_funcs import get_credentials, check_credentials

DB_NAME = "db_url"
DATA = postgre_login, postgre_pass = get_credentials(".env")

if __name__ == '__main__':
    app.run()

    if not check_credentials(*DATA):
        print("!ERROR bad credentials. Closing the program.")
        sys.exit()

    create_db(DB_NAME, DATA)  # creating db if not
    engine = connect_to_db(DB_NAME, DATA)  # creating engine to manage db
    # receive_all_tokens(engine)  # url_funcs.py needs engine to receive all tokens from db
    print_table(engine)

    # long_url = get_long_url()  # flask_http
    #
    # url_short_token = get_token_from_db(engine, long_url)  # db
    # if url_short_token is None:
    #     url_short_token = create_token(engine, long_url)  # url
    #
    # send_long_url()  # flask_http / console print
