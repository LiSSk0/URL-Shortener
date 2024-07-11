from db.orm_funcs import DataBase
from flask_http.flask_funcs import app, process, input_long_url, send_db
import sys
from db.credentials_funcs import get_credentials, check_credentials

DB_NAME = "db_url"
DATA = postgre_login, postgre_pass = get_credentials(".env")

if __name__ == '__main__':
    if not check_credentials(*DATA):
        print("!ERROR bad credentials. Closing the program.")
        sys.exit()

    db = DataBase(DB_NAME, DATA)
    send_db(db)

    app.run(debug=True)
