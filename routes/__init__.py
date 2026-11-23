from routes.api import api


def register_routes(app):
    # saare blueprints yahin register honge - app.py saaf rahega
    app.register_blueprint(api)