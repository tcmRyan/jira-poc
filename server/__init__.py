import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rq import Queue
from worker.worker import conn

app = Flask(__name__, static_url_path='/static')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
q = Queue(connection=conn)

import server.views
import server.lifecycle
import server.webhooks.callbacks
