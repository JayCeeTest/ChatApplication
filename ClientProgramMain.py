__author__ = 'jarethmoyo'

import socket
import threading
import time
from PyQt4 import QtGui
from PyQt4 import QtCore
from sys import argv


class ClientProgram(object):
    def __init__(self, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = port
        # connect on the port that the server is serving on
        self.client_socket.connect((self.host, self.port))

    def respond(self, msg):
        self.client_socket.send(msg)

    def start_listening(self,tb):
        thread=threading.Thread(target=lambda: self.listen(textbox=tb))
        thread.daemon=True # End thread when program is closed
        thread.start()

    def listen(self, textbox):
        while 1:
            self.msg, self.server_address=self.client_socket.recvfrom(1024)
            textbox.append(self.msg)


class ClientInterface(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        QtGui.QWidget.setGeometry (self, 400, 400, 400, 400)
        app = QtGui.QApplication.instance()
        app.setStyleSheet('QLabel{color: black; font-size:15px}')
        self.setWindowTitle("Client")
        layout = QtGui.QGridLayout(self)

        self.top_label = QtGui.QLabel()
        self.top_label.setText("CHAT HISTORY")

        self.msg_label = QtGui.QLabel()
        self.msg_label.setText("MESSAGE")

        clear = QtGui.QPushButton()
        clear.setText("Clear History")
        clear.clicked.connect(self.clear_history)
        send = QtGui.QPushButton()
        send.setText("Send")
        send.clicked.connect(self.send_message)

        self.textbox = QtGui.QTextEdit()
        self.line_box = QtGui.QLineEdit()
        layout.addWidget(self.top_label,1,1)
        layout.addWidget(self.textbox,2,1,1,2)
        layout.addWidget(self.msg_label,3,1)
        layout.addWidget(self.line_box,4,1,1,2)
        layout.addWidget(clear,5,1)
        layout.addWidget(send,5,2)
        self.connected = False  # not connected to server
        # define client
        self.initiate_conn()

    def initiate_conn(self):
        try:
            self.client = ClientProgram(9090)
            self.client.start_listening(self.textbox)
            self.connected = True
        except socket.error:
            print "No Server to connect to"

    def clear_history(self):
        self.textbox.clear()

    def send_message(self):
        msg = self.line_box.text()
        msg = str(msg)
        client_name = self.client.client_socket.getsockname()
        full_msg = str((client_name)) + ": " + msg
        self.client.respond(full_msg) # send message to server
        self.line_box.clear()
        self.textbox.append(full_msg)


if __name__ == "__main__":
    a=QtGui.QApplication(argv)
    li=ClientInterface()
    li.show()
    li.raise_()
    exit(a.exec_())

#c = ClientProgram(9090)
#c.respond()

