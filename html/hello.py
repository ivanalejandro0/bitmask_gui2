#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World! This is powered by Python backend."

if __name__ == "__main__":
    print('oh hello')
    app.run(host='127.0.0.1', port=5000)
