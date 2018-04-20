__author__ = 'jarethmoyo'
from sys import argv

from PyQt4 import QtGui
from PyQt4 import QtCore
from QLED import *
from Server import *
import threading


class ServerInterface(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        QtGui.QWidget.setGeometry (self, 700, 400, 700, 400)
        app = QtGui.QApplication.instance()
        app.setStyleSheet('QLabel{color: black; font-size:15px}')
        self.setWindowTitle("SERVER")
        layout = QtGui.QGridLayout(self)

        self.status_label = QtGui.QLabel()
        self.status_label.setText("SERVER IS OFFLINE")

        self.connected_label = QtGui.QLabel()
        self.connected_label.setText("LOG")

        self.led = QLed(self, onColour=QLed.Green, shape=QLed.Circle)
        self.led.setFixedSize(30,30)
        self.textbox = QtGui.QTextEdit()

        self.list_box = QtGui.QListWidget()

        start = QtGui.QPushButton()
        start.setText("Start Server")
        start.clicked.connect(self.activate_serve)

        #stop = QtGui.QPushButton()
        #stop.setText("Stop Server")
        #stop.clicked.connect(self.stop_serve)

        layout.addWidget(self.connected_label,1,1)
        layout.addWidget(self.led,1,2)
        layout.addWidget(self.status_label,1,3)
        layout.addWidget(self.textbox,3,1)
        layout.addWidget(self.list_box,3,2,1,2)
        layout.addWidget(start,4,2,1,2)
        #layout.addWidget(stop,5,2,1,2)

        self.server_started = False

    def activate_serve(self):
        thread=threading.Thread(target=lambda: self.serve())
        thread.daemon=True # End thread when program is closed
        thread.start()

    def serve(self):
        if not self.server_started:
            self.led.toggleValue()
            self.status_label.setText("SERVER IS ONLINE")
            self.server_started = True
            s = Server(9090, self.textbox,self.list_box)
            s.start()

    def stop_serve(self):
        if self.server_started:
            self.led.toggleValue()
            self.status_label.setText("SERVER IS OFFLINE")
            self.server_started = False


if __name__ == "__main__":
    a=QtGui.QApplication(argv)
    li=ServerInterface()
    li.show()
    li.raise_()
    exit(a.exec_())
