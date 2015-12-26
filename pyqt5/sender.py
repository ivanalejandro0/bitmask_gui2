#!/usr/bin/env python
# -*- coding: utf-8 -*-
import queue
import threading
import time

import zmq
from zmq.sugar.constants import NOBLOCK


class Sender():
    """
    Message sender running in a thread, it sends messages to the bitmask
    daemon.

    NOTE: right now this is not very well thought, just the basics to get a
    simple zmq non twistedy message sender.
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

        :type command: list
        """
        self._socket.send_multipart(command, NOBLOCK)
