#!/usr/bin/env python
# encoding: utf-8

from flask import Flask

import os

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/test')

app = Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR,
            static_url_path='')


@app.route('/')
def root():
    # return render_template('index.html')
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
