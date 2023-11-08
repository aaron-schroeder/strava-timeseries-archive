from flask import Flask, redirect, url_for

from flask_app.authorization import bp as authorization_blueprint
from flask_app.proxy import bp as proxy_blueprint


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def main():
        return redirect(url_for('authorization.redirect_to_strava'))

    app.register_blueprint(authorization_blueprint, url_prefix='/auth')
    app.register_blueprint(proxy_blueprint, url_prefix='/proxy')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()