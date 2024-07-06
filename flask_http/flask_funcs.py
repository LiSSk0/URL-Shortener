from flask import Flask, render_template, request, redirect, url_for, abort
from db.orm_funcs import get_token_from_db, is_long_url_in_db,is_token_in_db
from url_convert.url_funcs import create_short_url

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def input_long_url():
    if request.method == 'GET':
        return render_template("input_long_url.html")
    else:
        long_url = request.form.get('longurl')
        if long_url != '':
            print(long_url)
            if(is_long_url_in_db(long_url)):
                token = 'http://127.0.0.1:5000/' + get_token_from_db(long_url)
            else:
                token = 'http://127.0.0.1:5000/' + create_short_url(long_url)
            return render_template("output_short_url.html", token=token)
        else:
            return render_template("error_long_url_is_None.html")


@app.route('/<token>', methods=['GET', 'POST'])
def process(token):
    if is_token_in_db(token):
        long_url = "0" # get_longurl_from_db(token)
        return redirect(long_url)
    else:
        return abort(404)

