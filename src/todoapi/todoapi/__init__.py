from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .apis import blueprint


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.register_blueprint(blueprint, url_prefix="/api/v1")

    return app
