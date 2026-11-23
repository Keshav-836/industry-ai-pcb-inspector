from routes.api import api
from routes.pages import pages


def register_routes(app):
    # saare blueprints yahin register honge - app.py saaf rahega
    app.register_blueprint(pages)
    app.register_blueprint(api)