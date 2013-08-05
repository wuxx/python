#!/usr/bin/python
# coding=utf-8

import sys
import time
from PyQt4 import QtGui
from PyQt4 import QtCore

class Timer(QtGui.QMainWindow):
    def __init__(self, app, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('timer')
        self.widget = QtGui.QWidget(self)
        self.app = app
        self.setWindow()
        self.setSignal()
        self.setTimer()

    def setWindow(self):
        self.label_hour = QtGui.QLabel('hour')
        self.label_hour.setAlignment(QtCore.Qt.AlignCenter)

        self.label_min = QtGui.QLabel('minute')
        self.label_min.setAlignment(QtCore.Qt.AlignCenter)

        self.label_sec = QtGui.QLabel('second')
        self.label_sec.setAlignment(QtCore.Qt.AlignCenter)

        self.spinbox_hour = QtGui.QSpinBox()
        self.spinbox_hour.setRange(0, 24)
        self.spinbox_hour.setValue(0)
        
        self.spinbox_min = QtGui.QSpinBox()
        self.spinbox_min.setRange(0, 59)
        self.spinbox_min.setValue(0)

        self.spinbox_sec = QtGui.QSpinBox()
        self.spinbox_sec.setRange(0, 59)
        self.spinbox_sec.setValue(0)

        self.button_start = QtGui.QPushButton('start') 
        self.button_reset = QtGui.QPushButton('reset') 
        self.button_exit = QtGui.QPushButton('exit') 

        #self.button_file = QtGui.QPushButton('choose a music file')
        self.layout = QtGui.QVBoxLayout()

        grid = QtGui.QGridLayout()
        grid.addWidget(self.label_hour, 0, 0)
        grid.addWidget(self.label_min, 0, 1)
        grid.addWidget(self.label_sec, 0, 2)

        grid.addWidget(self.spinbox_hour, 1, 0)
        grid.addWidget(self.spinbox_min, 1, 1)
        grid.addWidget(self.spinbox_sec, 1, 2)

        self.layout.addLayout(grid)
        self.layout.addWidget(self.button_start)
        self.layout.addWidget(self.button_reset)
        self.layout.addWidget(self.button_exit)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def setSignal(self):
        self.connect(self.button_start, QtCore.SIGNAL('clicked()'), self.startTimer)
        self.connect(self.button_reset, QtCore.SIGNAL('clicked()'), self.resetTimer)
        self.connect(self.button_exit, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))

    def setTimer(self):
        self.timer = QtCore.QBasicTimer()

    def startTimer(self):
        self.hour = self.spinbox_hour.value()
        self.min = self.spinbox_min.value()
        self.sec = self.spinbox_sec.value()

        self.total_second = 0

        if self.hour * 60 * 60 + self.min * 60 + self.sec == 0:
            return 

        self.button_start.setEnabled(False)
        self.timer.start(1000, self)

    def resetTimer(self):
        self.button_start.setEnabled(True)
        self.spinbox_hour.setValue(0)
        self.spinbox_min.setValue(0)
        self.spinbox_sec.setValue(0)
        self.timer.stop()
        self.total_second = 0

    def timerEvent(self, event):

        self.total_second += 1
        expired_second = self.hour * 60 * 60 + self.min * 60 + self.sec
        if self.total_second == expired_second:
            self.resetTimer()
            self.timerExpired()
            return 

        left_total_second = expired_second - self.total_second

        second_per_hour = 60 * 60
        second_per_min = 60
        left_hour = left_total_second / second_per_hour
        left_total_second = left_total_second - left_hour * second_per_hour
        left_min = left_total_second / second_per_min
        left_total_second = left_total_second - left_min * second_per_min
        left_sec = left_total_second

        self.spinbox_hour.setValue(left_hour)
        self.spinbox_min.setValue(left_min)
        self.spinbox_sec.setValue(left_sec)

    def timerExpired(self):

            self.trayIcon = QtGui.QSystemTrayIcon(self)
            #self.trayIcon.setVisible(False)
            self.trayIcon.setIcon(QtGui.QIcon("images/trash.svg"))
            self.trayIcon.show()
            self.trayIcon.showMessage("timer", "your timer is expired", QtGui.QSystemTrayIcon.MessageIcon(0), 15 * 1000)

            #self.msgbox = QtGui.QMessageBox.information(self, 'timer', "timer expired!")
            
            for i in range(50):
                time.sleep(0.1)
                self.app.beep()
                i += 1

def start():
    app = QtGui.QApplication(sys.argv)
    t = Timer(app)
    t.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()
