from flask import Flask, render_template, request, redirect, url_for, abort
#from db.orm_funcs import get_token_from_db, is_in_db

app = Flask(__name__)


def is_token_in_db(token):
    return True


def get_longurl_from_db(token):
    return "https://proglib.io/p/samouchitel-po-python-dlya-nachinayushchih-chast-23-osnovy-veb-razrabotki-na-flask-2023-06-27"


def create_short_url(url):
    return url + "1"


def is_in_db(long_url):
    return False


def get_token_from_db(long_url):
    return long_url + "2"


@app.route('/', methods=['GET', 'POST'])
def input_long_url():
    if request.method == 'GET':
        return render_template("input_long_url.html")
    else:
        long_url = request.form.get('longurl')
        if long_url != '':
            print(long_url)
            if(is_in_db(long_url)):
                token = get_token_from_db(long_url)
            else:
                token = create_short_url(long_url)
            return redirect(url_for('output_short_url', token=token))
        else:
            return render_template("error_long_url_is_None.html")


@app.route('/short_url', methods=['GET', 'POST'])
def output_short_url():
    token = request.args.get('token', None)
    return render_template("output_short_url.html", token=token)


@app.route('/<token>', methods=['GET', 'POST'])
def process(token):
    if is_token_in_db(token):
        long_url = get_longurl_from_db(token)
        return redirect(long_url)
    else:
        return abort(404)


if __name__ == '__main__':
    app.run(debug=True)