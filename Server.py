__author__ = 'jarethmoyo'

from datetime import datetime
import socket
import threading
threading.Thread.daemon = True  # end thread when program is closed
import sys

all_client_threads = []


class ClientPrint(threading.Thread):
    def __init__(self, connection, text_box, list_box):
        # thread for each client initial phase
        threading.Thread.__init__(self)
        self.connection = connection[0]  # actual connection object
        self.addr = connection[1]  # address
        self.text_box = text_box
        self.list_box = list_box

    def run(self):
        try:
            date = str(datetime.now()).split(".")[0]
            init_text= "("+date + ") " + "Client %s, %s has connected" %(self.addr[0], self.addr[1])
            client = "Client %s" %str(self.addr)
            self.text_box.append(init_text)
            self.list_box.addItem(client)
            while 1:
                date = str(datetime.now()).split(".")[0]
                message = self.connection.recv(1024)
                full_msg = "("+date + ") "+"--> " + message
                self.text_box.append(full_msg)
                # broadcasting message to all clients
                for thread_obj in all_client_threads:
                    if thread_obj.addr == self.addr:
                        continue
                    thread_obj.connection.send(message)
        except socket.error, msg:
            print "A socket error occured: %s" %msg


class Server(object):
    def __init__(self, port, textbox,list_box):
        host = socket.gethostname()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.text_box = textbox
        self.list_box = list_box

        date = str(datetime.now()).split(".")[0]
        init_text= "("+date + ") " + "Server has started... Listening on port %s" %port
        self.text_box.append(init_text)
        # thread logic

    def start(self):
        # method to start the server
        while 1:
            conn = self.server_socket.accept()  # accept incoming connections
            new_client_thread = ClientPrint(conn, self.text_box, self.list_box)  # new thread for each client
            all_client_threads.append(new_client_thread)
            new_client_thread.start()

