from db.orm_funcs import is_in_db, get_short_url_from_db
from flask_http.flask_funcs import get_long_url, send_long_url
from url_convert.url_funcs import create_short_url

if __name__ == '__main__':
    print("is working")

    url_long = get_long_url()  # flask_http file

    if is_in_db(url_long):  # db file
        url_short = get_short_url_from_db(url_long)  # db file
    else:
        url_short = create_short_url()  # work w/ url file

    send_long_url()  # flask_http file / console print

