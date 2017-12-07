from flask import Blueprint

main = Blueprint('main', __name__)

def create_app(config_name):
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    #app.config.from_object('config')
    return app

from . import routes, events, models
