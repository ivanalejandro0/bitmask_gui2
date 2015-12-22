#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from ui_main import Ui_Main


class Main(QWidget):
    def __init__(self):
        # super(Main, self).__init__(self)
        QWidget.__init__(self)
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main()
    sys.exit(app.exec_())
