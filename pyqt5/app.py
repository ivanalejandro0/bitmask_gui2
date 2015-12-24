#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QWidget

from core_proxy import CoreProxy
from ui_main import Ui_Main


class Main(QWidget):
    def __init__(self):
        # super(Main, self).__init__(self)
        QWidget.__init__(self)
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.connect_ui()
        self.show()

        self._core_proxy = CoreProxy()

    def connect_ui(self):
        self.ui.pbLogin.clicked.connect(self.user_login)
        self.ui.pbEIPStart.clicked.connect(self.eip_start)

    def eip_start(self):
        print("EIP: start")
        # self._core_proxy.eip_start()

    def user_login(self):
        print("USER: login")
        username = self.ui.leUsername.text()
        password = self.ui.lePassword.text()
        self._core_proxy.user_login(username, password)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main()
    sys.exit(app.exec_())
