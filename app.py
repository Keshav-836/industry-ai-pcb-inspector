import os
from flask import Flask

from config import Config


def create_app():
    # app factory pattern - baad me testing aur blueprints easy ho jayenge
    app = Flask(__name__)
    app.config.from_object(Config)

    # data folder pehli baar run pe khud ban jaye
    os.makedirs(app.config["BOARDS_DIR"], exist_ok=True)

    # abhi ke liye ek simple route, bas check karne ke liye ki server chal raha hai
    @app.route("/")
    def home():
        return "PCB Inspector chal raha hai"

    return app


if __name__ == "__main__":
    app = create_app()
    # 127.0.0.1 matlab sirf apne laptop pe, bilkul offline
    app.run(host="127.0.0.1", port=5000, debug=True)
    