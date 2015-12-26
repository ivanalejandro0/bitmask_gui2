#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import sys

from PyQt5.QtWidgets import QApplication, QWidget

from core_proxy import CoreProxy
from ui_main import Ui_Main


class Main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.connect_ui()
        self.show()

        self._core_proxy = CoreProxy()

    def connect_ui(self):
        self.ui.pbLogin.clicked.connect(self.user_login)
        self.ui.pbLogout.clicked.connect(self.user_logout)

        self.ui.pbEIPStart.clicked.connect(self.eip_start)
        self.ui.pbEIPStop.clicked.connect(self.eip_stop)
        self.ui.pbEIPStatus.clicked.connect(self.eip_status)

        self.ui.pbMailStart.clicked.connect(self.mail_start)
        self.ui.pbMailStop.clicked.connect(self.mail_stop)
        self.ui.pbMailStatus.clicked.connect(self.mail_status)

    def user_login(self):
        print("[UI] User: login")
        username = self.ui.leUsername.text()
        password = self.ui.lePassword.text()
        self._core_proxy.user_login(username, password)

    def user_logout(self):
        print("[UI] User: logout")
        username = self.ui.leUsername.text()
        password = self.ui.lePassword.text()
        self._core_proxy.user_logout(username, password)

    def eip_start(self):
        print("[UI] EIP: start")
        # self._core_proxy.eip_start()

    def eip_status(self):
        print("[UI] EIP: status")
        # self._core_proxy.eip_status()

    def eip_stop(self):
        print("[UI] EIP: stop")
        # self._core_proxy.eip_stop()

    def mail_start(self):
        print("[UI] Mail: start")
        # self._core_proxy.mail_start()

    def mail_status(self):
        print("[UI] Mail: status")
        # self._core_proxy.mail_status()

    def mail_stop(self):
        print("[UI] Mail: stop")
        # self._core_proxy.mail_stop()

    def closeEvent(self, event):
        print("[UI] closeEvent")
        self._core_proxy.stop()
        # event.accept()
        QWidget.closeEvent(self, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main()

    # Ensure that the application quits using CTRL-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec_())
