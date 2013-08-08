#!/usr/bin/python
# coding=utf-8

import sys
import random
from PyQt4 import QtGui,QtCore
from math import *

class GameWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle('24 point game')
        self.resize(400, 250)
        self.widget = QtGui.QWidget(self)
        self.setWindow()

    def setWindow(self):
        self.num = []
        self.num_bak = []
        self.expression = []
        self.label = []
        hbox0 = QtGui.QHBoxLayout()
        for i in range(0, 4):
            label = QtGui.QLabel()
            label.setAlignment(QtCore.Qt.AlignCenter)
            num = random.randint(1, 10) #[1, 10]
            self.num.append(num)
            self.num_bak.append(num)
            self.expression.append(str(num))
            label.setText(str(num))
            label.setStyleSheet(
                'background-color: rgb(47, 130, 208);'
                'color: rgb(246, 253, 251);'
                'font: 75 18pt "Axure Handwriting";'
            )
            hbox0.addWidget(label)
            self.label.append(label)

        self.expressionWid = QtGui.QLineEdit()
        self.submitWid = QtGui.QPushButton('submit', self)
        self.no_solutionWid = QtGui.QPushButton('no solution', self)
        self.answerWid = QtGui.QPushButton('see answer', self)
        self.nextWid = QtGui.QPushButton('next puzzle', self)

        self.statusbarWid = self.statusBar()
        self.connect(self, QtCore.SIGNAL("messageToStatusbar(QString)"), self.statusbarWid, QtCore.SLOT("showMessage(QString)"))

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.submitWid)
        hbox1.addWidget(self.no_solutionWid)
        hbox1.addWidget(self.answerWid)
        hbox1.addWidget(self.nextWid)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox0)
        vbox.addWidget(self.expressionWid)
        vbox.addLayout(hbox1)

        self.widget.setLayout(vbox)
        self.setCentralWidget(self.widget)

        self.connect(self.submitWid, QtCore.SIGNAL('clicked()'), self.checkExpression)
        self.connect(self.no_solutionWid, QtCore.SIGNAL('clicked()'), self.checkNoSolution)
        self.connect(self.answerWid, QtCore.SIGNAL('clicked()'), self.getAnswer)
        self.connect(self.nextWid, QtCore.SIGNAL('clicked()'), self.nextPuzzle)

    def nextPuzzle(self):
        self.num = []
        self.num_bak = []
        self.expression = []
        for i in range(0, 4): 
            label = self.label[i]
            num = random.randint(1, 10) 
            self.num.append(num)
            self.num_bak.append(num)
            self.expression.append(str(num))
            label.setText(str(num))
        self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), " ")
        self.expressionWid.clear()

    def checkNoSolution(self):
        """ 检查是否无解
        """
        self.num = []
        self.expression = []
        for i in range(len(self.num_bak)):
            self.num.append(self.num_bak[i])
            self.expression.append(str(self.num_bak[i]))

        rt = self.caculate(4);

        self.num = []
        for i in range(len(self.num_bak)):
            self.num.append(self.num_bak[i])

        if rt == True:
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "WRONG, please try again!")
        else:
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "RIGHT, you have done a great job!")

    def checkExpression(self):
        """ 计算输入的表达式结果
        """
        tmp_expression = str(self.expressionWid.text())
        try:
            self.exp_string = unicode(tmp_expression)
            result = eval(self.exp_string)
        except:
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "expression invalid")
            return

        if result == 24 and self.expressionLegal():
            self.success()
        else:
            self.failure()


    def expressionLegal(self):  
        """ 检查表达式是否合法
        """
        self.tmp_num = []

        length = len(self.exp_string)
        i = 0
        while i < length:
            if self.exp_string[i].isdigit() == True:
                self.tmp_num.append(int(self.exp_string[i]))
                if self.exp_string[i] == '1' and (i+1) < length :
                    if self.exp_string[i+1] == '0':
                        self.tmp_num[-1] = 10
                        i += 1
            i += 1


        if len(self.tmp_num) != 4:
            return False

        self.num.sort()
        self.tmp_num.sort()

        for i in range(4):
            if self.tmp_num[i] != self.num[i]:
                return False

        return True

    def success(self):
        self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "SUCCESS, congratulations!")

    def failure(self):
        self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "FAILURE, check each number and the sum")

    def getAnswer(self):

            self.num = []
            self.expression = []
            for i in range(len(self.num_bak)):
                self.num.append(self.num_bak[i])
                self.expression.append(str(self.num_bak[i]))

            rt = self.caculate(4);

            self.num = []
            for i in range(len(self.num_bak)):
                self.num.append(self.num_bak[i])

            self.num = []
            for i in range(len(self.num_bak)):
                self.num.append(self.num_bak[i])

            if rt == True:
                self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "answer is %s" %(self.expression[0]))
            else:
                self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "no solution")
            return rt

    def caculate(self, n = 4):
        """ 计算24点
        """
        if n == 1:
            if abs(self.num[0]- 24.0) < 1E-6:
                return True
            else:
                return False
    
        for i in range(0, n-1):
            for j in range(i+1, n):
    
                a = self.num[i]
                b = self.num[j]
                self.num[j] = self.num[n-1]
                
                expa = self.expression[i]
                expb = self.expression[j]
                self.expression[j] = self.expression[n-1]
    
                # a+b
                tmp = ['(', expa, '+', expb, ')']
                self.expression[i] = ''.join(tmp)
                self.num[i] = float(a)+float(b)
                if self.caculate(n-1) == True:
                    return True
    
                # a*b
                tmp = ['(', expa, '*', expb, ')']
                self.expression[i] = ''.join(tmp)
                self.num[i] = float(a)*float(b)
                if self.caculate(n-1) == True:
                    return True
    
                # a-b
                tmp = ['(', expa, '-', expb, ')']
                self.expression[i] = ''.join(tmp)
                self.num[i] = float(a)-float(b)
                if self.caculate(n-1) == True:
                    return True
    
                # b-a
                tmp = ['(', expb, '-', expa, ')']
                self.expression[i] = ''.join(tmp)
                self.num[i] = float(b)-float(a)
                if self.caculate(n-1) == True:
                    return True
    
                # a/b
                if b != 0:
                    tmp = ['(', expa, '/', expb, ')']
                    self.expression[i] = ''.join(tmp)
                    self.num[i] = float(a)/float(b)
                    if self.caculate(n-1) == True:
                        return True
    
                # b/a
                if a != 0:
                    tmp = ['(', expb, '/', expa, ')']
                    self.expression[i] = ''.join(tmp)
                    self.num[i] = float(b)/float(a)
                    if self.caculate(n-1) == True:
                        return True
    
                self.num[i] = a
                self.num[j] = b
                self.expression[i] = expa
                self.expression[j] = expb
        return False

def startGame():
    app = QtGui.QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    startGame()
