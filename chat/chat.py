#!/usr/bin/python
# coding=utf-8

import sys
import socket
import thread
import select
from PyQt4 import QtGui,QtCore
from math import *

reload(sys)
sys.setdefaultencoding('utf-8')
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
        self.server_sock_inited = False
        self.state = DISCONNECTED

    def initChat(self, mode):
        self.state = DISCONNECTED
        self.mode = mode
        self.port = PORT
        self.sendbuf = ''


        self.sendbuflock = thread.allocate_lock() 
        if mode == SERVER:
            if self.server_sock_inited == False:
                self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server_sock.bind(('0.0.0.0', self.port))
                self.server_sock.listen(5)
                self.server_sock_inited = True
        elif mode == CLIENT:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def setWindow(self):
        self.textwindow = QtGui.QTextEdit()
        self.textwindow.setReadOnly(True)
        self.connect(self, QtCore.SIGNAL("messageAppendToTextWindow(QString)"), self.textwindow, QtCore.SLOT("append(QString)"))

        self.sendtext = QtGui.QTextEdit()

        self.sendbtn = QtGui.QPushButton('send', self)
        self.sendbtn.setDefault(True)
        self.sendbtn.setShortcut('Ctrl+S')
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

        gbox = QtGui.QGridLayout()
        gbox.addWidget(self.textwindow, 0, 0)
        gbox.addWidget(self.sendtext, 1, 0)
        gbox.addLayout(hbox, 2, 0)

        gbox.setRowStretch(0, 30)
        gbox.setRowStretch(1, 10)
        self.widget.setLayout(gbox)

    def server(self):
        print "server selected"
        self.initChat(SERVER)
        self.clientact.setDisabled(True)
        self.serveract.setDisabled(True)


        thread.start_new_thread(self.thread, ('server_thread', self.mode))

    def thread(self, string, mode):
        print "%s %s running..." %(string, mode)
        if mode == SERVER:
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "waiting for client...")
            self.connection, self.remoteaddress = self.server_sock.accept()
            self.connection.setblocking(0)
            self.state = CONNECTED
            idle = 0
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "client connected")
            while self.state == CONNECTED:
                print "server running..."
                try:
                    self.sendbuflock.acquire()
                    if len(self.sendbuf) != 0:
                        if len(self.sendbuf) > SEND_LIMIT:
                            self.sendbuf = self.sendbuf[0:SEND_LIMIT]
                        self.connection.send(str(self.sendbuf))
                        idle = 0
                        self.sendbuf = ''
                    self.sendbuflock.release()

                    buf = ''
                    rlist, wlist, elist = select.select([self.connection], [], [], 0.5)
                    if len(rlist) != 0:
                        buf = self.connection.recv(RECV_LIMIT)  
                        if len(buf) != 0:
                            print "receive %s" %(buf)
                            print "len(buf): %d" %(len(buf))
                            text = ''.join([str(self.remoteaddress[0]), ':', str(self.remoteaddress[1]), '>', str(buf)])
                            if text[-1] == '\n':
                                text = text[0:-1]
                            print "text: %s" %(text)
                            print "len(text): %d" %(len(text))
                            #self.textwindow.append(text)   # 线程中不能使用GUI对象, 只能发射信号
                            self.emit(QtCore.SIGNAL("messageAppendToTextWindow(QString)"), text)
                            #test = "吴xx"
                            #test.encode('utf-8')
                            #self.emit(QtCore.SIGNAL("messageAppendToTextWindow(QString)"), test)
                            #self.emit(QtCore.SIGNAL("messageAppendToTextWindow(QString)"), QtCore.QString(u'测试')) # success
                            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "chatting")
                            idle = 0
                        else:
                            idle += 1
                            print "idle: %d" %(idle)
                            if idle == 240:
                                print "idle timeout0" 
                                self.connection.close()
                                self.reset()
                                thread.exit_thread()
                    else:
                        idle += 1
                        print "idle: %d" %(idle)
                        if idle == 240:
                            print "idle timeout" 
                            self.connection.close()
                            self.reset()
                            thread.exit_thread()
                except socket.error, e:
                    print "except: other except.. %s" %(e)
                    self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "session closed")
                    self.connection.close() 
                    self.reset()
                    thread.exit_thread()

        elif mode == CLIENT:
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "connecting to server...")
            print "client thread running..."
            idle = 0

            try:
                self.client_sock.connect((self.serverip, self.port))
                self.client_sock.setblocking(0)    # 此语句要在self.sock.connect之后
                self.state = CONNECTED
                self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "connecting to server... success")
                print "connect successed"
                while self.state == CONNECTED:
                    self.sendbuflock.acquire()
                    if len(self.sendbuf) != 0:
                        print "now send the text... sendbuf: %s" %(self.sendbuf)
                        if len(self.sendbuf) > SEND_LIMIT:
                            self.sendbuf = self.sendbuf[0:SEND_LIMIT]
                        self.client_sock.send(str(self.sendbuf))   # 这里必须要用str转换, self.sendbuf是QString类型
                        idle = 0
                        print "send the text.... idle: %d" %(idle)
                        self.sendbuf = ''
                    self.sendbuflock.release()
                    print "recv..."
                    buf = ''
                    rlist, wlist, elist = select.select([self.client_sock], [], [], 0.5)
                    print "after select..."
                    print "len(rlist): %d" %(len(rlist))
                    if len(rlist) != 0:
                        buf = self.client_sock.recv(RECV_LIMIT)
                        print "len(buf): %d" %(len(buf))
                        if len(buf) != 0:
                            text = ''.join([str(self.serverip), ':', str(self.port), '>', buf])
                            if text[-1] == '\n':
                                text = text[0:-1]
                            print "text: %s" %(text)
                            self.emit(QtCore.SIGNAL("messageAppendToTextWindow(QString)"), text)
                            idle = 0
                        else:
                            idle += 1
                            print "idle: %d" %(idle)
                            if idle == 240:
                                print "timeout..."
                                self.client_sock.close()
                                self.reset()
                                thread.exit_thread()
                    else:
                        idle += 1
                        print "idle: %d" %(idle)
                        if self.state == DISCONNECTED:
                            self.client_sock.close()
                            thread.exit_thread()
                        if idle == 240:
                            print "timeout..."
                            self.client_sock.close()
                            self.reset()
                            thread.exit_thread()

                        
            except socket.error, e:
                print "except: %s" %(e)
                if e.errno == 111:       # Connection refused
                    self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "connection refused")
                elif e.errno == 10061:
                    self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "connection refused")
                else:
                    print "other except: %s" %(e)
                    self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "connection failed, session closed")

                self.client_sock.closed()
                self.reset()
                thread.exit_thread()
                
        else:
            print "unexcept mode: %d exiting thread .. " %(mode)
            thread.exit_thread()

        thread.exit_thread()



    def client(self):
        print "client selected"
        self.initChat(CLIENT)

        text, ok = QtGui.QInputDialog.getText(self, 'SERVER IP', 'Enter The Server IP:')
        if ok == True:
            if self.isvalid(text) == True:
                self.serverip = text
                print "servserip is %s" %(self.serverip)
                self.serveract.setDisabled(True)
                self.clientact.setDisabled(True)
                thread.start_new_thread(self.thread, ('client_thread', self.mode))
            else:
                self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "ip address invalid")

    def reset(self):
        print "connection reset"
        self.state = DISCONNECTED
        self.serveract.setEnabled(True)
        self.clientact.setEnabled(True)
        self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "session closed")


    def send(self):
        print "now send the text %s" %(self.sendtext.toPlainText())
        text = self.sendtext.toPlainText()
        if len(text) != 0 and self.state == CONNECTED:
            self.sendbuflock.acquire()
            self.sendbuf = text
            text = ''.join(['I>', str(self.sendbuf)])
            self.emit(QtCore.SIGNAL("messageAppendToTextWindow(QString)"), text)
            self.sendbuflock.release()
            self.sendtext.setPlainText('')
        else:
            print "no session existed"
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "session not started")

    def isvalid(self, ip):
        if len(ip) == 0:
            return False
        else:
            return len([i for i in ip.split('.') if (0<= int(i)<= 255)])== 4

def startChat():
    app = QtGui.QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    startChat()
