from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def input_long_url():
    if request.method == 'GET':
        return render_template("input_long_url.html")
    else:
        long_url = request.form.get('longurl')
        if long_url != '':
            print(long_url)
            token = int(long_url)+5
            return redirect(url_for('output_short_url', token=token))
        else:
            return render_template("error_long_url_is_None.html")


@app.route('/short_url', methods=['GET', 'POST'])
def output_short_url():
    token = request.args.get('token', None)
    return render_template("output_short_url.html", token=token)


if __name__ == '__main__':
    app.run(debug=True)