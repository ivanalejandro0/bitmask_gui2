#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import uuid

import zmq


class Sender():
    """
    Message sender running in a thread, it sends messages to the bitmask
    daemon.

    NOTE: right now this is not very well thought, just the basics to get a
    simple zmq non twistedy message sender.
    """
    POLL_TIMEOUT = 1000  # ms

    # this is defined on bonafide config
    ENDPOINT = "ipc:///tmp/bonafide.sock"

    def __init__(self):
        """
        Initialize the ZMQ socket to talk to the signaling server.
        """
        self._requests = {}

        # when this Event is set, the receiver will cycle, check for messages.
        # We unset this to stop the thread.
        self._do_work = threading.Event()

        self._receiver_thread = threading.Thread(target=self._receiver)

        context = zmq.Context.instance()
        self._socket = context.socket(zmq.DEALER)
        self._socket.setsockopt(zmq.IDENTITY, b'SENDER')
        self._socket.connect(self.ENDPOINT)

    def _disconnect(self):
        """ Disconnect socket. """
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.close()

    def send(self, cmd):
        """
        Send command to the Core.

        :param cmd: the command and arguments to send.
        :type cmd: list[bytes, bytes, ...]

        :return: unique identifier for the command sent
        :rtype: bytes
        """
        print("Sender: sending: {0}".format(cmd))
        uid = uuid.uuid4().bytes
        request = [uid]
        request.extend(cmd)
        self._socket.send_multipart(request)
        self._requests[uid] = {
            'request': cmd,
            'response': None,
        }
        print("Sender: command id: {0}".format(uid))
        return uid

    def start(self):
        self._do_work.set()
        self._receiver_thread.start()

    def stop(self):
        self._do_work.clear()

    def _receiver(self):
        print("Receiver thread started")
        context = zmq.Context.instance()
        client = context.socket(zmq.DEALER)
        client.setsockopt(zmq.IDENTITY, b'RECEIVER')
        client.connect(self.ENDPOINT)
        # client.send_multipart([b'no-uid', b'hello'])

        poll = zmq.Poller()
        poll.register(client, zmq.POLLIN)

        while self._do_work.is_set():
            socks = dict(poll.poll(self.POLL_TIMEOUT))
            if socks.get(client) == zmq.POLLIN:
                reply = client.recv_multipart(zmq.NOBLOCK)
                print("Received:", reply)
                ruid = reply[0]
                self._requests[ruid]['response'] = reply[1]

    def get_response(self, uid):
        req = self._requests.get(uid)
        if req is not None:
            return req[uid].get('response')
