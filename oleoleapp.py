#!/bin/env python
import os
from app import create_app, db, socketio
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell

app = create_app(debug=True)

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    socketio.run(app)
