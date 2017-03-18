from flask import Flask
import random

app = Flask(__name__)


@app.route('/')
def coin_flip():
    flips = ["heads", "tails"]
    return random.choice(flips)
