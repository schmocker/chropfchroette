import time

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    # server template
    return render_template('index.html')