from flask import Flask, render_template, request, redirect, abort
from db.orm_funcs import DataBase
from url_convert.url_funcs import create_short_url, check_long_url
import qrcode

app = Flask(__name__)

db = DataBase


def send_db(database):
    global db
    db = database


def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr


@app.route('/', methods=['GET', 'POST'])
def input_long_url():
    if request.method == 'GET':
        db.delete_expired_urls()
        return render_template("input_long_url.html")
    else:
        long_url = request.form.get('longurl')
        if long_url != '':
            if check_long_url(long_url):
                if db.is_long_url_in_db(long_url):
                    token = str(db.get_token_from_db(long_url)[0])
                else:
                    token = str(create_short_url(db, long_url))
                short_url = 'http://127.0.0.1:5000/'+token
                qr_code = generate_qr_code(short_url)
                img = qr_code.make_image(fill_color="black", back_color="white")
                img.save(f"flask_http/static/{token}.png")
                return render_template("output_short_url.html", short_url=short_url, token=token)
            else:
                return render_template("error_long_url_is_not_url.html")
        else:
            return render_template("error_long_url_is_None.html")


@app.route('/check', methods=['GET','POST'])
def check_url():
    if request.method == 'GET':
        return render_template("check_url.html")
    else:
        shorturl = request.form.get('shorturl')
        if shorturl != '':
             token = shorturl[-6:]
             print(token)
             if db.is_token_in_db(token):
                counter = db.get_clicks_count(token)
                return render_template("check_url_counter.html", counter=counter )
             else:
                return render_template("no_url.html")
        else:
            return render_template("error_short_url_is_None.html")


@app.route('/<string:token>', methods=['GET'])
def process(token):
    if request.method == 'GET':
        if db.is_token_in_db(token):
            long_url = db.get_long_url_from_db(token)
            db.increase_clicks_count(token)
            return redirect(long_url)
        else:
            return abort(404)


