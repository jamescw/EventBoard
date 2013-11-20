# -*- coding: utf-8 -*-

"""
Event Server
===========

This simple application uses WebSockets to
publish events to browser based clients.
"""

import gevent
from flask import (
    Flask,
    render_template,
    request,
    Response
)
from flask_sockets import Sockets
from flask_jsonschema import (
    JsonSchema,
    validate,
    ValidationError
)

from backends import EventBackend

app = Flask(__name__)
app.config.from_pyfile('settings.py')
jsonschema = JsonSchema(app)
sockets = Sockets(app)
redis_url = app.config['REDIS_URL']
redis_channel = app.config['REDIS_CHANNEL']

events = EventBackend(redis_url, redis_channel)
events.start()


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
@validate('event')
def inbox():
    """
    Receives incoming events and insert them into Redis.
    """
    event = request.data
    events.publish(event)
    return Response(status=201)

@sockets.route('/receive')
def outbox(ws):
    """
    Sends outgoing chat messages, via `EventBackend`.
    """
    events.register(ws)

    while ws.socket is not None:
        # Context switch while `EventBackend.start`
        # is running in the background.
        gevent.sleep()

@app.errorhandler(ValidationError)
def on_validation_error(e):
    #TODO: Handle errors properly!
    return "error"

