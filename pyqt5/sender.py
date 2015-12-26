#!/usr/bin/env python
# -*- coding: utf-8 -*-
import queue
import threading
import time

import zmq
from zmq.sugar.constants import NOBLOCK, SNDMORE


class Sender():
    """
    Message sender running in a thread, it sends messages to the bitmask
    daemon.
    """

    # this is defined on bonafide config
    ENDPOINT = "ipc:///tmp/bonafide.sock"

    def __init__(self):
        """
        Initialize the ZMQ socket to talk to the signaling server.
        """
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect(self.ENDPOINT)

        self._queue = queue.Queue()

        self._do_work = threading.Event()  # used to stop the worker thread.
        self._worker_thread = threading.Thread(target=self._worker)

    def _worker(self):
        """
        Worker loop that processes the Queue of pending requests to do.
        """
        while self._do_work.is_set():
            try:
                request = self._queue.get(block=False)
                self._send_request(request)
            except queue.Empty:
                pass
            time.sleep(0.01)

        print("Sender: thread stopped.")

    def start(self):
        """
        Start the Signaler worker.
        """
        self._do_work.set()
        self._worker_thread.start()

    def stop(self):
        """
        Stop the Signaler worker.
        """
        self._do_work.clear()

    def send(self, cmd):
        """
        Queue the command to send asap.
        """
        self._queue.put(cmd)

    def _send_request(self, command):
        """
        Rudimentary zmq (non twistedy) multipart message sender.
        borrowed from:
        http://txzmq.readthedocs.org/en/latest/_modules/txzmq/connection.html#ZmqConnection.send

        :type command: list
        """
        for part in command[:-1]:
            self._socket.send(part, NOBLOCK | SNDMORE)
        self._socket.send(command[-1], NOBLOCK)
