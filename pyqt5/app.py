#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget

from dispatcher import CommandDispatcher
from ui_main import Ui_Main

# TODO: implement timeouts for calls
# if we send a command and don't have a response on X time, we can assume that
# the the core is not alive (or not reachable)


class Main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.connect_ui()
        self.show()

        self._dispatcher = CommandDispatcher()

        self._who_to_call = {}

        self._response_poller = QTimer(self)
        self._response_poller.timeout.connect(self._check_core_responses)
        self._response_poller.start(100)  # milliseconds

    def closeEvent(self, event):
        print("[UI] closeEvent")
        self._dispatcher.stop()
        QWidget.closeEvent(self, event)

    def connect_ui(self):
        self.ui.pbLogin.clicked.connect(self.user_login)
        self.ui.pbLogout.clicked.connect(self.user_logout)

        self.ui.pbEIPStart.clicked.connect(self.eip_start)
        self.ui.pbEIPStop.clicked.connect(self.eip_stop)
        # self.ui.pbEIPStatus.clicked.connect(self.eip_status)

        self.ui.pbMailStart.clicked.connect(self.mail_start)
        self.ui.pbMailStop.clicked.connect(self.mail_stop)
        self.ui.pbMailStatus.clicked.connect(self.mail_status)

        self.ui.pbCoreStatus.clicked.connect(self.core_status)

    def _on(self, uid, callme):
        """
        On given `uid` ready, call `callme`
        """
        print("Scheduled uid, callable: {0!r}".format((uid, callme)))
        self._who_to_call[uid] = callme

    def _check_core_responses(self):
        """
        Check if the core has responses for us and call the specified callable
        if it has.
        """
        try:
            uid, callme = self._who_to_call.popitem()
        except KeyError:  # dict empty
            return
        except Exception as e:
            print("Unexpected error: {0!r}".format(e))

        try:
            r = self._dispatcher.get_response(uid)
        except KeyError:  # no such uid
            return

        if r is not None:
            callme(r)
        else:
            # there is no response yet, add it again
            self._who_to_call[uid] = callme

    def user_login(self):
        print("[UI] User: login")
        username = self.ui.leUsername.text()
        password = self.ui.lePassword.text()
        ruid = self._dispatcher.user_login(username, password)
        self._on(ruid, self._update_login_status)

    def _update_login_status(self, data):
        print("[UI] login status: {0!r}".format(data))
        self.ui.lblLoginStatus.setText(data.decode('utf-8'))

    def user_logout(self):
        print("[UI] User: logout")
        username = self.ui.leUsername.text()
        password = self.ui.lePassword.text()
        self._dispatcher.user_logout(username, password)

    def eip_start(self):
        print("[UI] EIP: start")
        self._dispatcher.eip_start()

    # def eip_status(self):
    #     print("[UI] EIP: status")
    #     self._dispatcher.eip_status()

    def eip_stop(self):
        print("[UI] EIP: stop")
        self._dispatcher.eip_stop()

    def mail_start(self):
        print("[UI] Mail: start")
        # self._dispatcher.mail_start()

    def mail_stop(self):
        print("[UI] Mail: stop")
        # self._dispatcher.mail_stop()

    def mail_status(self):
        print("[UI] Mail: status")
        ruid = self._dispatcher.mail_status()
        self._on(ruid, self._update_mail_status)

    def _update_mail_status(self, data):
        print("[UI] mail status: {0!r}".format(data))
        self.ui.lblMailStatus.setText(data.decode('utf-8'))

    def core_start(self):
        # TODO: this should run a subprocess for the core
        print("[UI] Core: start - NOT IMPLEMENTED")
        # self._dispatcher.core_start()

    def core_status(self):
        print("[UI] Core: status")
        ruid = self._dispatcher.core_get_status()
        self._on(ruid, self._update_core_status)

    def _update_core_status(self, data):
        print("[UI] core status: {0!r}".format(data))
        self.ui.lblCoreStatus.setText(data.decode('utf-8'))

    def core_stop(self):
        print("[UI] Core: stop")
        self._dispatcher.core_shutdown()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main()

    # Ensure that the application quits using CTRL-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec_())
