#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sender import Sender

# from bonafide config
ENDPOINT = "ipc:///tmp/bonafide.sock"


class CoreProxy():

    def __init__(self):
        self._sender = Sender()
        self._sender.start()

    def stop(self):
        self._sender.stop()

    def user_login(self, username, password):
        self._sender.send([b'user',
                           b'authenticate',
                           username.encode('utf-8'),
                           password.encode('utf-8')])
