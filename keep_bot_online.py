from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "Currently Up"

def run():
    app.run(host='0.0.0.0', port=8000)

def keep_bot_online():
    t = Thread(target=run)
    t.start()