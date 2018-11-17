#! /usr/bin/python3
# -*- coding: utf-8 -*-
 
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

class MixerWindow(QWidget):
    def __init__(self, parent=None):
        super(MixerWindow, self).__init__(parent)
        self.init_layout()

    def init_layout(self):
        textbox = QPlainTextEdit()
        button = QPushButton()
        button.setText('button_label')
        button.clicked.connect(self.on_clicked)
        button.pressed.connect(self.on_pressed)
        button.released.connect(self.on_released)

        layout = QVBoxLayout()
        layout.addWidget(textbox)
        layout.addWidget(button)

        self.setLayout(layout)

    def on_clicked(self):
        print('click')

    def on_pressed(self):
        print('press')

    def on_released(self):
        print('released')

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MixerWindow()
    window.show()
    sys.exit(app.exec_())
