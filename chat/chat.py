#!/usr/bin/python
# coding=utf-8

import sys
import socket
import thread
from PyQt4 import QtGui,QtCore
from math import *

NONE = 0
SERVER = 1
CLIENT = 2

DISCONNECTED = 1
CONNECTED = 2

PORT = 8001

SEND_LIMIT = 1024
RECV_LIMIT = 1024
class ChatWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle('web chat')
        #self.resize(800, 500)
        self.resize(400, 250)
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)
        self.setWindow()
        self.initChat()

    def initChat(self):
        self.state = DISCONNECTED
        self.mode = NONE
        self.state = DISCONNECTED
        self.port = PORT
        self.sendbuf = ''

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setWindow(self):
        self.textwindow = QtGui.QTextEdit()
        self.textwindow.setReadOnly(True)
        self.connect(self, QtCore.SIGNAL("messageAppendToTextWindow(QString)"), self.textwindow, QtCore.SLOT("append(QString)"))

        self.sendtext = QtGui.QTextEdit()

        self.sendbtn = QtGui.QPushButton('send', self)
        self.sendbtn.setDefault(True)
        self.connect(self.sendbtn, QtCore.SIGNAL('clicked()'), self.send)

        self.statusbar = self.statusBar()
        self.connect(self, QtCore.SIGNAL("messageToStatusbar(QString)"), self.statusbar, QtCore.SLOT("showMessage(QString)"))

        self.serveract = QtGui.QAction(QtGui.QIcon(''), 'Server', self)
        self.serveract.setStatusTip('Server Mode')
        self.connect(self.serveract, QtCore.SIGNAL('triggered()'), self.server)

        self.clientact = QtGui.QAction(QtGui.QIcon(''), 'Client', self)
        self.clientact.setStatusTip('Client Mode')
        self.connect(self.clientact, QtCore.SIGNAL('triggered()'), self.client)

        self.resetact = QtGui.QAction(QtGui.QIcon(''), 'Reset', self)
        self.resetact.setStatusTip('Reset Connection')
        self.connect(self.resetact, QtCore.SIGNAL('triggered()'), self.reset)

        self.menubar = self.menuBar()
        menu = self.menubar.addMenu('&Menu')
        menu.addAction(self.serveract)
        menu.addAction(self.clientact)
        menu.addAction(self.resetact)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.sendbtn)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.textwindow)
        vbox.addWidget(self.sendtext)
        vbox.addLayout(hbox)

        self.widget.setLayout(vbox)

    def server(self):
        print "server selected"
        #self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "Waiting for client ...")
        print "emit"

        self.mode = SERVER
        self.clientact.setDisabled(True)
        self.serveract.setDisabled(True)

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', self.port))
        self.sock.listen(5)

        thread.start_new_thread(self.thread, ('server_thread', self.mode))

    def thread(self, string, mode):
        print "%s %s running..." %(string, mode)
        if mode == SERVER:
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "waiting for client...")
            self.connection, self.remoteaddress = self.sock.accept()
            self.state = CONNECTED
            while self.state == CONNECTED:
                print "server running..."
                try:
                    self.connection.settimeout(5)  
                    buf = self.connection.recv(RECV_LIMIT)  
                    if len(buf) != 0:
                        print "receive %s" %(buf)
                        text = ''.join([self.remoteaddress[0], ':', str(self.remoteaddress[1]), '>', buf])
                        print "text: %s" %(text)
                        #self.textwindow.append(text)   # 线程中不能使用GUI对象, 只能发射信号
                        self.emit(QtCore.SIGNAL("messageAppendToTextWindow(QString)"), text)
                        self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "chatting")
                    else:
                        self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "session closed")
                        self.connection.close() 
                        #self.sock.close()
                        self.reset()
                except socket.timeout:  
                    print 'except: time out'  
                    self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "session closed")
                    self.connection.close() 
                    #self.sock.close()
                    self.reset()
                except socket.error, msg:
                    print "except: other except" %(msg)
                    self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "session closed")
                    self.connection.close() 
                    #self.sock.close()
                    self.reset()

        elif mode == CLIENT:
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "connecting to server...")
            print "client thread running..."

            try:
                self.sock.connect((self.serverip, self.port))
                self.sock.setblocking(0)
                self.state = CONNECTED
                print "connect successed"
                while self.state == CONNECTED:
                    if len(self.sendbuf) != 0:
                        print "sendbuf: %s" %(self.sendbuf)
                        self.sock.send(self.sendbuf)
                        self.sendbuf = ''
                    print "recv..."
                    buf = ''
                    try:
                        buf = self.sock.recv(RECV_LIMIT)
                    except socket.error, e:
                        if e.errno == 11: # Resource temporarily unavailable
                            print "except: %s" %(e)
                        else:
                            print "other except: %s" %(e)
                    print "recv buf: %s" %(buf)
                    if len(buf) != 0:
                        text = ''.join([str(self.serverip), ':', str(self.port), '>', buf])
                        self.emit(QtCore.SIGNAL("messageAppendToTextWindow(QString)"), text)
            except socket.error, e:
                print "except: %s" %(e)
                if e.errno == 111:       # Connection refused
                    self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "connection refused")
                elif e.errno == 11:    # Resource temporarily unavailable
                    print "except: %s" %(e)
                else:
                    self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "connection failed, session closed")
                    self.reset()
                
            print "client mode"

        else:
            print "exiting thread .. "
            thread.exit_thread()

        thread.exit_thread()



    def client(self):
        print "client selected"
        self.mode = CLIENT
        self.serveract.setDisabled(True)
        self.clientact.setDisabled(True)

        text, ok = QtGui.QInputDialog.getText(self, 'SERVER IP', 'Enter The Server IP:')
        if ok == True:
            self.serverip = text
            print "servserip is %s" %(self.serverip)
            thread.start_new_thread(self.thread, ('client_thread', self.mode))

    def reset(self):
        print "connection reset"
        self.serveract.setEnabled(True)
        self.clientact.setEnabled(True)
        self.mode = NONE
        self.state = DISCONNECTED
        self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "session closed1")


    def send(self):
        print "now send the text %s" %(self.sendtext.toPlainText())
        sendtext = self.sendtext.toPlainText()
        self.sendbuf = sendtext
        if len(sendtext) != 0 and self.state == CONNECTED:
            self.emit(QtCore.SIGNAL("messageAppendToTextWindow(QString)"), ''.join(['you:', text]))
        else:
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "session not started")

def startChat():
    app = QtGui.QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    startChat()
