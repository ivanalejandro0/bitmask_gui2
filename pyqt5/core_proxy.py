#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sender import Sender


class CoreProxy():
    """
    This is a remote interface to interact with the bitmask core daemon.
    """

    def __init__(self):
        self._sender = Sender()
        self._sender.start()

    def stop(self):
        self._sender.stop()

    def core_get_version(self):
        pass

    def core_get_status(self):
        pass

    def core_get_stats(self):
        pass

    def core_shutdown(self):
        pass

    def user_register(self, username, password):
        self._sender.send([b'user',
                           b'signup',
                           username.encode('utf-8'),
                           password.encode('utf-8')])

    def user_login(self, username, password):
        self._sender.send([b'user',
                           b'authenticate',
                           username.encode('utf-8'),
                           password.encode('utf-8')])

    def user_logout(self, username, password):
        self._sender.send([b'user',
                           b'logout',
                           username.encode('utf-8'),
                           password.encode('utf-8')])

    # def mail_start(self):
    #     pass
    #
    # def mail_stop(self):
    #     pass

    def mail_status(self):
        self._sender.send([b'mail', b'status'])

    def mail_get_imap_token(self):
        self._sender.send([b'mail', b'get_imap_token'])

    def mail_get_smtp_token(self):
        self._sender.send([b'mail', b'get_smtp_token'])

    def mail_get_smtp_certificate(self):
        self._sender.send([b'mail', b'get_smtp_certificate'])

    def eip_start(self):
        self._sender.send([b'eip', b'start'])

    def eip_stop(self):
        self._sender.send([b'eip', b'stop'])
