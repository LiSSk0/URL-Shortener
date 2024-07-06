from flask import Flask, render_template, request, redirect, abort
from db.orm_funcs import DataBase
from url_convert.url_funcs import create_short_url

app = Flask(__name__)

db = None


def send_db(database):
    global db
    db = database


@app.route('/', methods=['GET', 'POST'])
def input_long_url():
    if request.method == 'GET':
        return render_template("input_long_url.html")
    else:
        long_url = request.form.get('longurl')
        if long_url != '':
            print(long_url)
            if db.is_long_url_in_db(long_url):
                token = 'http://127.0.0.1:5000/' + db.get_token_from_db(long_url)
            else:
                token = 'http://127.0.0.1:5000/' + create_short_url(db, long_url)
            return render_template("output_short_url.html", token=token)
        else:
            return render_template("error_long_url_is_None.html")


@app.route('/<token>', methods=['GET', 'POST'])
def process(token):
    if db.is_token_in_db(token):
        long_url = db.get_long_url_from_db(token)
        return redirect(long_url)
    else:
        return abort(404)
