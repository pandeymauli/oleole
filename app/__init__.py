from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

socketio = SocketIO()
db = SQLAlchemy()

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gotta-make-this-one-complicated-thing!'
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/chatdb4"
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    return app
