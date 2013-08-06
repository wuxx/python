#!/usr/bin/python
# coding=utf-8

import sys 
import random
from PyQt4 import QtGui,QtCore

class Jigsaw(QtGui.QMainWindow):
    Width = 4
    Height = 4

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle('JigSaw Game')
        self.setFixedSize(400, 400)
        #self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.statusbar = self.statusBar()
        self.connect(self, QtCore.SIGNAL("messageToStatusbar(QString)"), self.statusbar, QtCore.SLOT("showMessage(QString)"))
        self.label_num = []     # [1, 2, ... 15, -1] -> [random, ...]
        self.label = []
        self.isFinished = False
        self.count = 0
        self.initGame()

    def initGame(self):
        self.layout = QtGui.QGridLayout()
        self.widget = QtGui.QWidget(self)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setRandom()
        self.setWindow()

    def setRandom(self):
        tmp_array = [x for x in range(1, Jigsaw.Width * Jigsaw.Height)]
        for i in range(Jigsaw.Width*Jigsaw.Height-1):
            j = random.randint(0, len(tmp_array)-1)
            self.label_num.append(tmp_array[j])
            tmp_array.pop(j)

        self.label_num.append(-1)

    def setWindow(self):
        for i in range(Jigsaw.Height):
            for j  in range(Jigsaw.Width):
                label = QtGui.QLabel()                      
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setStyleSheet(
                'background-color: rgb(255, 255, 127);'
                'color: rgb(0, 170, 255);'
                'font: 75 18pt "Axure Handwriting";'
                )    
                label.setText(str(self.label_num[i*Jigsaw.Height + j]))
                self.label.append(label)
                self.layout.addWidget(label, i, j)

        self.label[-1].setText("")
        self.label[-1].setStyleSheet('')
        self.free_label_index = len(self.label)-1
    
    def keyPressEvent(self, event):

        if self.isFinished == True:
            return 
        key = event.key()
        if not self.isShiftable(key):
            return 

        if key == QtCore.Qt.Key_Up:
            self.swapLabel(self.free_label_index, self.free_label_index + Jigsaw.Width)
            self.free_label_index = self.free_label_index + Jigsaw.Width
        elif key == QtCore.Qt.Key_Down:
            self.swapLabel(self.free_label_index, self.free_label_index - Jigsaw.Width)
            self.free_label_index = self.free_label_index - Jigsaw.Width
        elif key == QtCore.Qt.Key_Left:
            self.swapLabel(self.free_label_index, self.free_label_index + 1)
            self.free_label_index = self.free_label_index + 1
        elif key == QtCore.Qt.Key_Right:
            self.swapLabel(self.free_label_index, self.free_label_index - 1)
            self.free_label_index = self.free_label_index - 1

        self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), str(self.count))

        if self.isFinish() == True:
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "Finished")


        
    
    def isShiftable(self, key):
        if key == QtCore.Qt.Key_Up:
            if self.free_label_index + Jigsaw.Width >= Jigsaw.Width * Jigsaw.Height:
                return False
        elif key == QtCore.Qt.Key_Down:
            if self.free_label_index - Jigsaw.Width < 0:
                return False
        elif key == QtCore.Qt.Key_Left:
            if (self.free_label_index + 1) % Jigsaw.Width == 0:
                return False
        elif key == QtCore.Qt.Key_Right:
            if self.free_label_index % Jigsaw.Width == 0:
                return False

        return True

    
    def swapLabel(self, indexA, indexB):

        tmpb = self.label[indexB]
        self.label[indexA].setText(tmpb.text())
        self.label[indexA].setStyleSheet(tmpb.styleSheet())

        self.label[indexB].setText("")
        self.label[indexB].setStyleSheet("")

        tmp = self.label_num[indexB]
        self.label_num[indexB] = self.label_num[indexA]
        self.label_num[indexA] = tmp
        self.count += 1
        """print "swap %d %d" %(indexA, indexB)
        tmpa = self.label[indexA]
        tmpb = self.label[indexB]

        print "tmpa[%d]: text(%s); style(%s)" %(indexA, tmpa.text(), tmpa.styleSheet())
        print "tmpb[%d]: text(%s); style(%s)" %(indexB, tmpb.text(), tmpb.styleSheet())

        self.label[indexA].setText(tmpb.text())
        self.label[indexA].setStyleSheet(tmpb.styleSheet())

        self.label[indexB].setText(tmpa.text())
        self.label[indexB].setStyleSheet(tmpa.styleSheet())

        print "label[%d]: text(%s); style(%s)" %(indexA, self.label[indexA].text(), self.label[indexA].styleSheet())
        print "label[%d]: text(%s); style(%s)" %(indexB, self.label[indexB].text(), self.label[indexB].styleSheet())
        """
        
    def isFinish(self):
        for i in range(len(self.label_num) - 1):
            if self.label_num[i] != i+1:
                return False
        self.isFinished = True
        return True
        

def startGame():
    app = QtGui.QApplication(sys.argv)
    game = Jigsaw()
    game.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    startGame()
