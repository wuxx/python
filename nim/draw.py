# coding=utf-8
import pygame
from pygame import *
import math


black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
darkgreen = (0, 100,  0)
blue = (0, 0, 255)
grey = (169, 169, 169)
orange = (255, 165, 0)
purple = (160, 32, 240)
background = (100, 100, 100)
violet = (238, 130, 238)

dark_color = darkgreen
light_color = green


NONE= 0
SELECTED = 1
REMOVED = 2

class draw:
    """ @screen_info[0][0]: 屏幕像素宽
        @screen_info[0][1]: 屏幕像素高
        @screen_info[1][0]: 棋盘起始点x
        @screen_info[1][1]: 棋盘起始点y
        @screen_info[2]:    长方框之间的距离
        @screen_info[3]:    长方框的高度
        @screen_info[4]:    棋子的半径
        @screen_info[5]:    棋子列表如[1, 2, 3, 4, 5]
        @screen_info[6]:    标题
    """
    def __init__(self, screen_info):
        pygame.init()
        size = screen_info[0]
        self.startx = screen_info[1][0]
        self.starty = screen_info[1][1]
        self.margin = screen_info[2]
        self.rect_height = screen_info[3]
        self.radius = screen_info[4]
        self.piece_list = screen_info[5]
        title = screen_info[6]

        self.map = [[NONE for x in range(y)] for y in self.piece_list]    # self.map[y][x]
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(grey)
        pygame.display.update()

        self.drawboard()
        pygame.display.set_caption(title)

    def drawboard(self):
        boardWidth = 2 * self.margin + self.rect_height * max(self.piece_list)
        boardHeight = self.margin + (self.margin + self.rect_height) * len(self.piece_list)
        pygame.draw.rect(self.screen, black, [self.startx, self.starty, boardWidth, boardHeight])
        for i in range(len(self.piece_list)):
            pygame.draw.rect(self.screen, white, [self.startx + self.margin, self.starty + self.margin + i * (self.margin + self.rect_height), boardWidth - 2*self.margin, self.rect_height])
        
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                self.drawcircle((x, y), light_color)
        pygame.display.update([self.startx, self.starty, boardWidth, boardHeight])

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
        x = (pos[0] - self.startx - self.margin) // (self.rect_height)
        y = (pos[1] - self.starty - self.margin) // (self.rect_height + self.margin)
        if y >= 0 and y < len(self.map):
            if x >= 0 and x < len(self.map[y]):
                if math.hypot(self.startx + self.margin + x*self.rect_height + self.rect_height/2 - pos[0], self.starty + self.margin + y*self.rect_height + self.rect_height/2 - pos[1]) <= self.radius:
                    return (x, y)
        return (-1, -1)
        #if x < 0 or x >= self.gridX or y < 0 or y >= self.gridY:
            #return (-1, -1)
        #else:
            #return (x, y)

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
        if pos != (-1, -1) and self.map[pos[1]][pos[0]] == NONE:
            return True
        else:
            return False

    def set(self, pos):
        self.map[pos[1]][pos[0]] = SELECTED
        self.drawcircle(pos, dark_color)
    
    def unset(self, pos):
        if self.map[pos[1]][pos[0]] == SELECTED:
            self.map[pos[1]][pos[0]] = NONE
            self.drawcircle(pos, light_color)

    def remove(self, rlist = []):
        if rlist == []:
            remove_list = []
            for y in range(len(self.map)):
                for x in range(len(self.map[y])):
                    if self.map[y][x] == SELECTED:
                        remove_list.append((x, y))
            if remove_list != []:
                for r in remove_list:
                    if r[1] != remove_list[0][1]:
                        return False
                for r in remove_list:
                    self.map[r[1]][r[0]] = REMOVED
                    self.drawcircle((r[0], r[1]), white) 
                return True
            else:
                return False    # 没有棋子消除
        else:
            print "rlist: ", rlist
            for r in rlist:
                print "remove:", r
                self.map[r[1]][r[0]] = REMOVED
                self.drawcircle((r[0], r[1]), white) 

    def setai(self, pos):
        if self.isfree(pos) == True:
            self.map[pos[0]][pos[1]] = AI

    def setplayer(self, pos):
        if self.isfree(pos) == True:
            self.map[pos[0]][pos[1]] = PLAYER

    def drawcircle(self, pos, color, width = 0):
        px = self.startx + self.margin + self.rect_height * pos[0]  
        py = self.starty + self.margin + (self.rect_height + self.margin) * pos[1]
        pygame.draw.circle(self.screen, color, (px + self.rect_height/2, py + self.rect_height/2), self.radius, width)
        pygame.display.update(px, py, px + self.rect_height, py+ self.rect_height)

    def drawX(self, pos, color, width):
        px = self.startx + self.margin + (self.margin + self.width) * pos[0]
        py = self.starty + self.margin + (self.margin + self.width) * pos[1]
        pointlist = [(px+16, py+16), (px+self.width-16, py+self.width-16)]
        pygame.draw.lines(self.screen, color, True, pointlist, width)
        pointlist = [(px+self.width-16, py+16), (px+16, py+self.width-16)]
        pygame.draw.lines(self.screen, color, True, pointlist, width)
        pygame.display.update(px, py, self.width, self.width)
        
    def reset(self):
        self.map = [[NONE for x in range(y)] for y in self.piece_list]    # self.map[y][x]
        self.drawboard()

    def getmap(self):
        return self.map

    def isover(self):
        for x in self.map:
            if NONE in x:
                return False
        return True
