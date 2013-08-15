#!/usr/bin/python
# coding=utf-8
import pygame 
import draw 
import core

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
grey = (169, 169, 169)

statusbar = [320, 250, 200, 40]
def setstatusbar(text):
    draw.drawtext(statusbar, (330, 255), 30, 'Unocide.ttf',  yellow, text)

def clearstatusbar():
    draw.drawtext(statusbar, (330, 255), 30, 'Unocide.ttf',  yellow, '')

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
screen_info=[(500, 350), (10, 10), 2, 100, 3, 3, 'tic-tac-toe']
pygame.init()
draw = draw.draw(screen_info)
core = core.core()

menu0 = [360, 80, 120, 40]
menu1 = [360, 130, 120, 40]
draw.drawtext(menu0, (370, 85), 30, 'Unocide.ttf',  green, 'I First')
draw.drawtext(menu1, (370, 135), 30, 'Unocide.ttf', green, 'AI First')
clearstatusbar()

end = False
gameover = False

ai_first = False

while end == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: end = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            point = pygame.mouse.get_pos()
            if pygame.Rect(menu0).collidepoint(point):
                draw.reset()
                ai_first = False
                gameover = False
                clearstatusbar()
            elif pygame.Rect(menu1).collidepoint(point):
                draw.reset()
                clearstatusbar()
                ai_first = True
                gameover = False
                (x, y) = core.caculate(draw.getmap())
                draw.setai((x, y))
                draw.drawX((x, y), red, 4)

            else:

                if ai_first == False:           # player first
                    pos = draw.getpos(point)
                    #print "get (%d, %d)" %(pos[0], pos[1])
                    if draw.isfree(pos) == True and gameover == False:
                        draw.setplayer(pos)
                        draw.drawcircle(pos, green, -1, 4)
                        #print "setplayer"
                        if core.iswin(draw.getmap(), pos[0], pos[1]):
                            #print "player win!"
                            gameover = True
                            setstatusbar('Player Win')
                            continue
                        if draw.isover() == True:
                            gameover = True
                            #print "game over, draw game"
                            setstatusbar('Draw Game')
                            continue
                        (x, y) = core.caculate(draw.getmap())
                        #print "ai (%d, %d)" %(x, y)
                        draw.setai((x, y))
                        draw.drawX((x, y), red, 4)
                        if core.iswin(draw.getmap(), x, y):
                            #print "ai win"
                            setstatusbar('AI Win')
                            gameover = True
                            continue
                else:   # ai first
                    pos = draw.getpos(point)
                    if draw.isfree(pos) == True and gameover == False:
                        draw.setplayer(pos)
                        draw.drawcircle(pos, green, -1, 4)
                        if core.iswin(draw.getmap(), pos[0], pos[1]):
                            setstatusbar('Player Win')
                            gameover = True
                            continue
                        (x, y) = core.caculate(draw.getmap())
                        draw.setai((x, y))
                        draw.drawX((x, y), red, 4)
                        if core.iswin(draw.getmap(), x, y):
                            #print "ai win"
                            setstatusbar('AI Win')
                            gameover = True
                            continue
                        if draw.isover() == True:
                            setstatusbar('Draw Game')
                            gameover = True
                            continue
                    
                    

pygame.quit()


