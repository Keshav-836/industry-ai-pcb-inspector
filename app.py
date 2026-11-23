import os
from flask import Flask

from config import Config
from routes import register_routes


def create_app():
    # app factory pattern - testing aur blueprints dono easy ho jate hain
    app = Flask(__name__)
    app.config.from_object(Config)

    # data folder pehli baar run pe khud ban jaye
    os.makedirs(app.config["BOARDS_DIR"], exist_ok=True)

    # pages (HTML) aur api (data) dono routes yahan judte hain
    register_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    # 127.0.0.1 matlab sirf apne laptop pe, bilkul offline
    app.run(host="127.0.0.1", port=5000, debug=True)