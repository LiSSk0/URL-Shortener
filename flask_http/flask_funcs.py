from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def get_long_url():
    return "дай ссылку"

@app.route('/get_url', methods=['GET', 'POST'])
def send_long_url():
    return "держи ссылку"

if __name__ == '__main__':
    app.run()