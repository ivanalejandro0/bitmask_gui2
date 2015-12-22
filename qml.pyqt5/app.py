#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import signal

from PyQt5 import QtCore
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication


class Controller(QtCore.QObject):
    """
    A basic controller class that helps to interact between qml and python.
    """
    def __init__(self):
        QtCore.QObject.__init__(self)

    @QtCore.pyqtSlot(QtCore.QObject)
    def itemSelected(self, wrapper):
        print('User clicked on:'.format(wrapper))

    @QtCore.pyqtSlot(str, str, QtCore.QObject)
    def login(self, user, password, widget):
        print('Login - u: {0} - p: {1}'.format(user, password))
        widget.setProperty('loggedIn', 'true')

    @QtCore.pyqtSlot(str, str)
    def set_user_to(self, jid, b_jid):
        print('set_user_to - jid: {0} - b_jid: {1}'.format(jid, b_jid))
        # widget.setProperty('loggedIn', 'true')

    @QtCore.pyqtSlot(QtCore.QObject)
    def send_message(self, message):
        text = message.property('text')
        print('Send message: {0}'.format(message))
        print('Send message.text: {0}'.format(text))


class MainWindow(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

        self._controller = Controller()

        self.view = QQuickView()

        full_path = os.path.realpath(__file__)
        folder = os.path.dirname(full_path)
        qml_file = os.path.join(folder, 'qml', 'App.qml')
        qml_qurl = QtCore.QUrl.fromLocalFile(qml_file)

        self.view.setSource(qml_qurl)

        # Add context properties to use this objects from qml
        rc = self.view.rootContext()
        rc.setContextProperty('controller', self._controller)

    def show(self):
        self.view.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    # Ensure that the application quits using CTRL-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    sys.exit(app.exec_())
