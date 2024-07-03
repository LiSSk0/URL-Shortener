from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_long_url():
    return render_template("input_long_url.html")

@app.route('/get_url', methods=['GET', 'POST'])
def send_long_url():
    return render_template("output_short_url.html")

if __name__ == '__main__':
    app.run()