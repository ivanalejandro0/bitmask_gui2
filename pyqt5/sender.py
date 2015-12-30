#!/usr/bin/env python
# -*- coding: utf-8 -*-
import queue
import threading
import time

import zmq


class Sender():
    """
    Message sender running in a thread, it sends messages to the bitmask
    daemon.

    NOTE: right now this is not very well thought, just the basics to get a
    simple zmq non twistedy message sender.
    """
    # Total wait time == POLL_TIMEOUT * POLL_TRIES (ms)
    POLL_TRIES = 5
    POLL_TIMEOUT = 2000  # ms

    # this is defined on bonafide config
    ENDPOINT = "ipc:///tmp/bonafide.sock"

    def __init__(self):
        """
        Initialize the ZMQ socket to talk to the signaling server.
        """
        self._queue = queue.Queue()
        self._do_work = threading.Event()  # used to stop the worker thread.
        self._worker_thread = threading.Thread(target=self._worker)
        self._socket = None
        self._connect()

    def _connect(self, reconnect=False):
        """
        Connect to the core, create a new socket and reconnect if specified.
        """
        if self._socket is not None and reconnect:
            self._socket.setsockopt(zmq.LINGER, 0)
            self._socket.close()

        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect(self.ENDPOINT)

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

    def _send_request(self, request):
        """
        Send the given request to the server.
        This is used from a thread safe loop in order to avoid sending a
        request without receiving a response from a previous one.

        :param request: the request to send.
        :type request: list of bytes
        """
        print("Sender: sending: {0}".format(request))
        time_a = time.perf_counter()  # time before sending
        self._socket.send_multipart(request)

        poll = zmq.Poller()
        poll.register(self._socket, zmq.POLLIN)

        reply = None
        tries = 0

        while True:
            socks = dict(poll.poll(self.POLL_TIMEOUT))
            if socks.get(self._socket) == zmq.POLLIN:
                reply = self._socket.recv()
                break

            tries += 1
            if tries < self.POLL_TRIES:
                print('Retrying receive... {0}/{1}'.format(
                    tries, self.POLL_TRIES))
            else:
                break

        time_b = time.perf_counter()  # time after sending

        if reply is None:
            print("Sender: timeout error contacting backend")
            self._connect(reconnect=True)  # reconnect to cleanup socket
        else:
            print("Sender: received reply for '{0}' -> '{1}'".format(
                request, reply))

        print("Sender: elapsed time: {0}".format(time_b - time_a))
