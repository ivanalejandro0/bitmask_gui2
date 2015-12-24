#!/usr/bin/env python
# -*- coding: utf-8 -*-
# bitmask_cli
# Copyright (C) 2015 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Bitmask Command Line interface: zmq client.
"""
import getpass

# from txzmq import ZmqEndpoint, ZmqFactory, ZmqREQConnection
import zmq

from sender import BackendProxy

# from bonafide config
ENDPOINT = "ipc:///tmp/bonafide.sock"


class CoreProxy():

    def __init__(self):
        self._sender = BackendProxy()
        self._sender.run()

    def user_login(self, username, password):
        self._sender.user('authenticate', username, password)
        pass

    def get_zmq_connection():
        zf = ZmqFactory()
        e = ZmqEndpoint('connect', ENDPOINT)
        return ZmqREQConnection(zf, e)

    def send_command(self, cli):

        args = cli.args
        subargs = cli.subargs

        cmd = args.command

        if cmd == 'version':
            print(['bitmask_cli: 0.0.1'])
            data = ("version",)

        elif cmd == 'status':
            data = ("status",)

        elif cmd == 'shutdown':
            data = ("shutdown",)

        elif cmd == 'debug':
            data = ("stats",)

        elif cmd == 'user':
            username = subargs.username
            if '@' not in username:
                print("ERROR: Username must be in the form <user@example.org>")
                return

            # TODO check that ONLY ONE FLAG is True
            # TODO check that AT LEAST ONE FLAG is True

            passwd = getpass.getpass()

            if subargs.create:
                data = ("user", "signup", username, passwd)
            if subargs.authenticate:
                data = ("user", "authenticate", username, passwd)
            if subargs.logout:
                data = ("user", "logout", username, passwd)

        elif cmd == 'mail':
            if subargs.status:
                data = ("mail", "status")

            if subargs.get_imap_token:
                data = ("mail", "get_imap_token")

            if subargs.get_smtp_token:
                data = ("mail", "get_smtp_token")

            if subargs.get_smtp_certificate:
                data = ("mail", "get_smtp_certificate")

        s = self.get_zmq_connection()
        try:
            # d = s.sendMsg(*data)
            s.sendMsg(*data)
        except zmq.error.Again:
            print("[ERROR] Server is down")
        # d.addCallback(cb)
        # d.addCallback(lambda x: reactor.stop())


def main():
    pass

if __name__ == "__main__":
    main()
