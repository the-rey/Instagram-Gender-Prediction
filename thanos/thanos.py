#!/usr/bin/env python

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
import naive_bayes as nb
import collector
from InstagramAPI import InstagramAPI

client_threads = {}
app = Flask("Thanos Classifier API")
socketio = SocketIO(app)

class ClientThread(Thread):
    def __init__(self, client_id):
        self._client_id = client_id

        super().__init__()

    def setData(self, algorithm, username, follower_limit, media_per_follower_limit, comments_per_media_limit):
        self._algorithm = algorithm
        self._username = username
        self._follower_limit = follower_limit
        self._media_per_follower_limit = media_per_follower_limit
        self._comments_per_media_limit = comments_per_media_limit

    def send_status(self, done, type, header="", body=""):
        payload = {'done': done, 'type': type, 'header': header, 'body': body}
        socketio.emit(self._client_id, payload, namespace='/classify')

    def run(self):
        if not (self._algorithm or self._username):
            return

        self.send_status("false", "message", "Getting list of followers")
        follower_id_list = collector.get_followers_id_list(ig_client, self._username, self._follower_limit)
        total_follower = len(follower_id_list)

        self.send_status("false", "data", "Total follower(s)", str(total_follower))

        all_follower_comments = []
        for follower_idx, follower in enumerate(follower_id_list):
            follower_comments = []

            all_media_id = collector.get_all_media_id(ig_client, follower, self._media_per_follower_limit)
            total_media = len(all_media_id)
            for media_idx, media_id in enumerate(all_media_id):
                self.send_status("false", "message", "Gathering comments from all followers",
                    str(follower_idx / total_follower * 100) + " follower(s) / " + str(media_idx / total_media * 100) + " media(s)")
                media_comments = collector.get_media_comments(ig_client, media_id, self._comments_per_media_limit)
                follower_comments.extend(media_comments)

            all_follower_comments.append(follower_comments)

        self.send_status("false", "data", "Total comment(s) data", str(len(all_follower_comments)))
        random.shuffle(all_follower_comments)
        self.send_status("false", "message", "Running " + self._algorithm + " algorithm")

@socketio.on('connect', namespace="/classify")
def classify():
    global client_threads
    client_id = request.args.get("clientID")
    client_threads[client_id] = ClientThread(client_id)

    print("New client_id: " + client_id)

    return client_id

@socketio.on('compute', namespace='/classify')
def compute(client_id, algorithm, username, follower_limit,
    media_per_follower_limit, comments_per_media_limit):
    global client_threads
    print("New compute request about '" + username + "' using: " +
        algorithm + " algorithm, from " + client_id)

    client_threads[client_id].setData(algorithm, username, follower_limit,
        media_per_follower_limit, comments_per_media_limit)
    client_threads[client_id].start()

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

def main(args):
    global ig_client
    ig_username = os.getenv("IG_USERNAME")
    ig_password = os.getenv("IG_PASSWORD")
    if not (ig_username or ig_password):
        print("Please set IG_USERNAME and IG_PASSWORD env variable")

    print("Logging into instragram account: " + ig_username)
    ig_client = InstagramAPI(ig_username, ig_password)
    if not ig_client.login():
        print("Instagram login failed!")
        sys.exit(1)

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
        help="Specifies the session secret key")

    args = parser.parse_args()

    app.config["ENV"] = args.env
    app.config["DEBUG"] = args.debug
    if args.secret == "":
        app.config["SECRET_KEY"] = b64encode(os.urandom(16)).decode('utf-8')
    else:
        app.config["SECRET_KEY"] = args.secret
    print("Generated secret key:", app.config["SECRET_KEY"])

    main(args)
