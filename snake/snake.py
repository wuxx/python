#!/usr/bin/python
# coding=utf-8

import sys
from PyQt4 import QtCore, QtGui
import random

class Game(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setGeometry(300, 300, 380, 180)
        self.setWindowTitle('snake')
        self.center()


        self.board = Board(self)
        self.board.start()
        self.setCentralWidget(self.board)

        self.statusbar = self.statusBar()
        self.connect(self.board, QtCore.SIGNAL("messageToStatusbar(QString)"), self.statusbar, QtCore.SLOT("showMessage(QString)")) 
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

class Board(QtGui.QFrame):
    BoardWidth = 22
    BoardHeight = 10
    Speed = 110

    Free = 0
    Userd = 1

    Up = 0
    Down = 1
    Left = 2
    Right = 3

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)  # 不添加此语句则不会响应按键
        self.timer = QtCore.QBasicTimer()
        self.snake_body = []
        self.isStarted = False
        self.isPaused = False

    def start(self):
        self.isStarted = True
        self.isDie = False
        self.isPaused = False
        self.snake_body = [(0, 0), (1, 0), (2, 0)]              # (x, y) 左上角为(0, 0) (0 ~ BoardWidth-1, 0 ~ BoardHeight-1) 第一个元素表示尾巴
        self.generateFood()
        self.direction = Board.Right
        self.timer.start(Board.Speed, self)

    def keyPressEvent(self, event):
        if self.isDie == True:
            return 
        key = event.key()      

        if key == QtCore.Qt.Key_Up:
            self.direction = Board.Up
        elif key == QtCore.Qt.Key_Down:
            self.direction = Board.Down
        elif key == QtCore.Qt.Key_Left:
            self.direction = Board.Left
        elif key == QtCore.Qt.Key_Right:
            self.direction = Board.Right

        elif key == QtCore.Qt.Key_P:
            self.pause()
        elif key == QtCore.Qt.Key_Space:
            self.move()

        else:
            QtGui.QWidget.keyPressEvent(self, event)

    def pause(self):
        if self.isPaused == False:
            self.isPaused = True
            self.timer.stop()
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "Paused")
        else:
            self.isPaused = False
            self.timer.start(Board.Speed, self)

    def timerEvent(self, event):
        self.move()
        if not self.isDie:
            self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), str(len(self.snake_body)))
    
    def generateFood(self):
        self.foodX = random.randint(0, Board.BoardWidth-1)
        self.foodY = random.randint(0, Board.BoardHeight-1)
        while (self.foodX, self.foodY) in self.snake_body:
            self.foodX = random.randint(0, Board.BoardWidth-1)
            self.foodY = random.randint(0, Board.BoardHeight-1)
 
        self.foodColor = QtGui.QColor(random.randint(0, 0xFFFFFF))
            
    def move(self):
        """ 根据self.direction更新self.snake_body，并重新画图
        """
        if self.isDie == True:
            return 
        if self.isPaused == True:
            return 
        head = self.snake_body[-1]  # 蛇头

        if self.direction == Board.Up:
            if head[1]-1 == -1 or (head[0], head[1]-1) in self.snake_body:
                self.die()
            else:
                self.snake_body.append((head[0], head[1]-1))

                if head[0] != self.foodX or head[1]-1 != self.foodY:
                    self.snake_body.pop(0)      # 蛇尾
                else:
                    self.generateFood()
        elif self.direction == Board.Down:
            if head[1]+1 == Board.BoardHeight or (head[0], head[1]+1) in self.snake_body:
                self.die()
            else:
                self.snake_body.append((head[0], head[1]+1))
                if head[0] != self.foodX or head[1]+1 != self.foodY:
                    self.snake_body.pop(0)
                else:
                    self.generateFood()
        elif self.direction == Board.Left:
            if head[0]-1  == -1 or (head[0]-1, head[1]) in self.snake_body:
                self.die()
            else:
                self.snake_body.append((head[0]-1, head[1]))
                if head[0]-1 != self.foodX or head[1] != self.foodY:
                    self.snake_body.pop(0)
                else:
                    self.generateFood()
        elif self.direction == Board.Right:
            if head[0]+1 == Board.BoardWidth or (head[0]+1, head[1]) in self.snake_body:
                self.die()
            else:
                self.snake_body.append((head[0]+1, head[1]))
                if head[0]+1 != self.foodX or head[1] != self.foodY:
                    self.snake_body.pop(0)
                else:
                    self.generateFood()
        self.update()
        
    def die(self):
        self.isDie = True
        self.snake_body.pop(0)
        self.update()
        self.timer.stop()
        self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "Game Over") 

    def paintEvent(self, event):
        """ 0. 画边框
            1. 画蛇身
            2. 画食物
        """ 
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()

        boardTop = (rect.bottom() - Board.BoardHeight * self.squareHeight()) / 2
        boardLeft = (rect.right() - Board.BoardWidth * self.squareWidth() ) / 2
        self.drawEdge(painter, boardLeft, boardTop, Board.BoardWidth * self.squareWidth(), Board.BoardHeight * self.squareHeight())
        for coord in self.snake_body:
            self.drawSquare(painter, boardLeft + coord[0] * self.squareWidth(), boardTop + coord[1] * self.squareHeight(), QtGui.QColor(0x1E90FF))

        self.drawSquare(painter, boardLeft + self.foodX * self.squareWidth(), boardTop + self.foodY * self.squareHeight(), self.foodColor)
        
        

    def squareWidth(self):
        """ 每个小方块占的像素宽
        """
        return self.contentsRect().width() / Board.BoardWidth

    def squareHeight(self):
        """ 每个小方块占的像素高
        """
        return self.contentsRect().height() / Board.BoardHeight

    def drawEdge(self, painter, x0, y0, x1, y1):
        """ 画边框
        """
        color = QtGui.QColor(0xFFFFFF)
        painter.fillRect(x0, y0, x1, y1, color)

    def drawSquare(self, painter, x, y, color):
        """ 在(x, y)处画一个方块，左上角为(0, 0)
        """
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, self.squareHeight() - 2, color)
        # 以下的画线是为了增加立体感,使方块更加好看
        painter.setPen(color.light())           # 画左上角的两根线,淡色
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)  # 画线，(x0, y0, x1, y1); (x0, y0) -> (x1, y1)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.dark())            # 画右下角的两根线,深色
        painter.drawLine(x + 1, y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)

def start():
    app = QtGui.QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()
