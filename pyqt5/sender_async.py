#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is implemented using ROUTER/DEALER zmq sockets, they can communicate
# asynchronously and many requests can be sent as well as receive many
# responses at any time.
# We are keeping track of received responses to be checked at any time the user
# wants to.

import queue
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
    POLL_TIMEOUT = 100  # ms
    QUEUE_TIMEOUT = 0.1  # sec

    # this is defined on bonafide config
    ENDPOINT = "ipc:///tmp/bonafide.sock"

    def __init__(self):
        """
        Initialize the ZMQ socket to talk to the signaling server.
        """
        # TODO, put a limit to this, we keep track of everything right now
        self._requests = {}

        self._queue = queue.Queue()
        # when this Event is set, the worker will cycle, send and check for
        # messages.
        # We unset this to stop the thread.
        self._do_work = threading.Event()

        self._worker_thread = threading.Thread(target=self._worker)

        context = zmq.Context.instance()
        self._socket = context.socket(zmq.DEALER)
        # self._socket.setsockopt(zmq.IDENTITY, b'SENDER')
        self._socket.connect(self.ENDPOINT)

    def _disconnect(self):
        """ Disconnect socket. """
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.close()

    def _send_request(self, uid):
        """
        Send command to the Core.

        :param uid: the uid of the command to send
        :type uid: bytes
        """
        request = self._requests[uid]['request']
        print("Sender: sending: {0!r}".format(request))
        self._socket.send_multipart(request)

    def send(self, cmd):
        """
        Queue the command to send asap.
        In case of 'shutdown' command send it right away.
        """
        print("Sender: queuing: {0!r}".format(cmd))

        # uid = str(uuid.uuid4()).encode()  # nicer looking uuid for print
        uid = uuid.uuid4().bytes
        request = [uid, b'']  # message format used by txzmq on the core
        request.extend(cmd)

        self._requests[uid] = {
            'request': request,
            'response': None,
        }

        if cmd == b'shutdown':
            # don't wait for shutdown
            self._send_request(request)

        self._queue.put(uid)
        return uid

    def start(self):
        """
        Start the sender thread.
        """
        self._do_work.set()
        self._worker_thread.start()

    def stop(self):
        """
        Stop the sender thread.
        """
        self._do_work.clear()

    def _process_queue(self):
        """
        Process the queue and trigger the send for one request (if any).
        """
        try:
            uid = self._queue.get(timeout=self.QUEUE_TIMEOUT)
            self._send_request(uid)
        except queue.Empty:
            pass

    def _receive_response(self, poll):
        """
        Poll the socket for new responses from the core.

        :param poll: the poller to use
        :type poll: zmq.Poller
        """
        client = self._socket
        socks = dict(poll.poll(self.POLL_TIMEOUT))
        if socks.get(client) == zmq.POLLIN:
            reply = client.recv_multipart(zmq.NOBLOCK)
            print("Received:", reply)
            ruid = reply[0]
            self._requests[ruid]['response'] = reply[2]

    def _worker(self):
        """
        Worker method meant to be run in a thread.
        This switches constantly between sending and receiving.
        Each send/receive blocks for a fraction of a second and it should be
        responsive messaging.
        """
        print("Worker thread started")
        client = self._socket

        poll = zmq.Poller()
        poll.register(client, zmq.POLLIN)

        while self._do_work.is_set():
            self._process_queue()
            self._receive_response(poll)

        self._disconnect()

    def get_response(self, uid):
        """
        Return the response for the specified uid.
        Return None if no response is arrived yet.

        :raise KeyError: if the specified uid does not exist.

        :param uid: the uid for the request to get the response from.
        :type uid: bytes
        """
        # this raises KeyError if we don't have such uid
        req = self._requests[uid]
        return req.get('response')
