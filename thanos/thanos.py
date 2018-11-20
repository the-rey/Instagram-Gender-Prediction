#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import argparse
from base64 import b64encode
import time
import random
import json

from flask_socketio import SocketIO, emit
from threading import Thread, Event
from time import sleep
from flask import (Flask, render_template, flash, redirect,
    url_for, request, copy_current_request_context)

import svm
import naive_bayes

app = Flask("Thanos Classifier API")
socketio = SocketIO(app)

client_threads = {}

class ClientThread(Thread):
    def __init__(self, client_id):
        self._client_id = client_id
        self.progress = 1
        super().__init__()

    def run(self):
        for _ in range(0, 100):
            socketio.emit(self._client_id, {'progress': self.progress}, namespace='/classify')

            self.progress += 1
            sleep(0.05)

@socketio.on('connect', namespace="/classify")
def classify():
    global client_threads
    client_id = request.args.get("clientID")
    client_threads[client_id] = ClientThread(client_id)

    print("New client_id: " + client_id)

    return client_id

@socketio.on('compute', namespace='/classify')
def compute(client_id, algorithm):
    global client_threads
    print("New compute request using: " + algorithm + " algorithm, from " + client_id)

    client_threads[client_id].start()

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

def main(args):
    app.run(host=args.host, port=args.port)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--port",
        action="store",
        dest="port",
        default="5001",
        help="Specifies the port to listen on")

    parser.add_argument(
        "-o",
        "--host",
        action="store",
        dest="host",
        default="127.0.0.1",
        help="Specifies the interface address to listen on")

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="debug",
        default=False,
        help="Specifies the debug mode")

    parser.add_argument(
        "-e",
        "--env",
        action="store",
        dest="env",
        default="development",
        help="Specifies the env for flask to run")

    parser.add_argument(
        "-s",
        "--secret",
        action="store",
        dest="secret",
        default="",
        help="Specifies the env for flask to run")

    args = parser.parse_args()

    app.config["ENV"] = args.env
    app.config["DEBUG"] = args.debug
    if args.secret == "":
        app.config["SECRET_KEY"] = b64encode(os.urandom(16)).decode('utf-8')
    else:
        app.config["SECRET_KEY"] = args.secret
    print("Generated secret key:", app.config["SECRET_KEY"])

    main(args)
