# coding=utf-8
import pygame
from pygame import *


black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (169, 169, 169)
background = (100, 100, 100)

NONE= 0
AI = 1
PLAYER = -1
class draw:
    """ @screen_info[0][0]: 屏幕像素宽
        @screen_info[0][1]: 屏幕像素高
        @screen_info[1][0]: 棋盘起始点x
        @screen_info[1][1]: 棋盘起始点y
        @screen_info[2]:    棋盘边框像素
        @screen_info[3]:    每个棋盘格子的边的像素(棋盘格子都是正方形)
        @screen_info[4]:    棋盘格子数(横)
        @screen_info[5]:    棋盘格子数(纵)
        @screen_info[6]:    标题
    """
    def __init__(self, screen_info):
        pygame.init()
        size = screen_info[0]
        self.startx = screen_info[1][0]
        self.starty = screen_info[1][1]
        self.margin = screen_info[2]
        self.width = screen_info[3]
        self.gridX = screen_info[4]
        self.gridY = screen_info[5]
        title = screen_info[6]

        self.map = []
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(grey)
        pygame.display.update()

        self.map = [[NONE for y in range(self.gridY)] for x in range(self.gridX)]
        self.drawboard()
        pygame.display.set_caption(title)

    def drawboard(self):
        boardWidth = self.margin + (self.margin+self.width) * self.gridX
        boardHeight = self.margin + (self.margin+self.width) * self.gridY
        pygame.draw.rect(self.screen, black, [self.startx, self.starty, boardWidth, boardHeight])
        pygame.display.update([self.startx, self.starty, boardWidth, boardHeight])
        
        for j in range(self.gridY):
            for i in range(self.gridX):
                self.drawsquare(i, j)

    def drawsquare(self, x, y):
        """在坐标position(x, y)处画正方形, 边像素为self.margin
        """
        px = self.startx + self.margin + (self.margin + self.width) * x
        py = self.starty + self.margin + (self.margin + self.width) * y
        pygame.draw.rect(self.screen, white, [px, py, self.width, self.width])
        pygame.display.update([px, py, self.width, self.width])

    def getpos(self, pos):
        """未点击在棋盘内返回(-1, -1)
        """
        x = (pos[0] - self.startx - self.margin) // (self.width + self.margin)
        y = (pos[1] - self.starty - self.margin) // (self.width + self.margin)
        if x < 0 or x >= self.gridX or y < 0 or y >= self.gridY:
            return (-1, -1)
        else:
            return (x, y)

    def drawtext(self, area, fontpos,  fontsize, fontname, fontcolor, text):
        """在(area[0], area[1], area[2], area[3])这块区域画文字
        """
        pygame.draw.rect(self.screen, [80, 80, 80], area)
        font = pygame.font.Font(fontname, fontsize)
        tt = font.render(text, 0, fontcolor)
        self.screen.blit(tt, fontpos)   # 让文字右移一点
        pygame.display.update()

    def isfree(self, pos):
        """pos合法而且是空位
        """
        if pos != (-1, -1) and self.map[pos[0]][pos[1]] == NONE:
            return True
        else:
            return False

    def setai(self, pos):
        if self.isfree(pos) == True:
            self.map[pos[0]][pos[1]] = AI

    def setplayer(self, pos):
        if self.isfree(pos) == True:
            self.map[pos[0]][pos[1]] = PLAYER

    def drawcircle(self, pos, color, radius = -1, width = 0):
        if radius == -1:
            radius = self.width/2 - 8
        px = self.startx + self.margin + (self.margin + self.width) * pos[0]
        py = self.starty + self.margin + (self.margin + self.width) * pos[1]
        pygame.draw.circle(self.screen, color, (px + self.width/2, py + self.width/2), radius, width)
        pygame.display.update(px, py, self.width, self.width)

    def drawX(self, pos, color, width):
        px = self.startx + self.margin + (self.margin + self.width) * pos[0]
        py = self.starty + self.margin + (self.margin + self.width) * pos[1]
        pointlist = [(px+16, py+16), (px+self.width-16, py+self.width-16)]
        pygame.draw.lines(self.screen, color, True, pointlist, width)
        pointlist = [(px+self.width-16, py+16), (px+16, py+self.width-16)]
        pygame.draw.lines(self.screen, color, True, pointlist, width)
        pygame.display.update(px, py, self.width, self.width)
        
    def reset(self):
        self.map = [[NONE for y in range(self.gridY)] for x in range(self.gridX)]
        self.drawboard()

    def getmap(self):
        return self.map

    def isover(self):
        for x in self.map:
            if NONE in x:
                return False
        return True
