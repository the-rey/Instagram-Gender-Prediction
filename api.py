#!/usr/bin/env python
import flask
import naive_baiyes 
from svm import svm

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>API </p>"

@app.route('/svm', methods=['GET'])
def svm():
    return "<h1>SVM</p>"

@app.route('/train_nb', methods=['GET'])
def train_nb():

    naive_baiyes.main("")
    naive_baiyes.nb_classify("test")

@app.route('/train_nb', methods=['GET'])
def train_nb():

    naive_baiyes.main("")
    naive_baiyes.nb_classify("test")

@app.route('/classify_nb', methods=['POST'])
def classify_nb():

    naive_baiyes.main("")
    naive_baiyes.nb_classify("test")



app.run()