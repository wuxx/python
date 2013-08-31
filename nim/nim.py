#!/usr/bin/python
# coding=utf-8
import pygame 
import draw 
import core

green = (0, 255, 0)
yellow = (255, 255, 0)

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
screen_info=[(800, 560), (20, 20), 4, 100, 40, [1, 2, 3, 4, 5], 'nim']
pygame.init()
draw = draw.draw(screen_info)
core = core.core()


statusbar = [550, 400, 200, 40]
menu0 = [600, 80, 160, 40] 
menu1 = [600, 130, 160, 40] 
draw.drawtext(menu0, (605, 82), 30, 'GAMECUBEN.ttf',  green, 'i first')
draw.drawtext(menu1, (605, 132), 30, 'GAMECUBEN.ttf', green, 'ai first')

def setstatusbar(text):
    draw.drawtext(statusbar, (555, 402), 30, 'GAMECUBEN.ttf',  yellow, text)

def clearstatusbar():
    draw.drawtext(statusbar, (555, 402), 30, 'GAMECUBEN.ttf',  yellow, '')


clearstatusbar()
#draw.drawtext()

end = False
gameover = False
ai_first = False

while end == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: end = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            press_btn = pygame.mouse.get_pressed()
            if press_btn[0] == 1:   # 左键
                point = pygame.mouse.get_pos()
                if pygame.Rect(menu0).collidepoint(point):
                    draw.reset()
                    ai_first = False
                    gameover = False
                    clearstatusbar()
                    continue
                elif pygame.Rect(menu1).collidepoint(point):
                    draw.reset()
                    ai_first = True
                    gameover = False
                    clearstatusbar()
                    remove_list = core.caculate(draw.getmap())
                    draw.remove(remove_list)
                else:
                    pos = draw.getpos(point)
                    if pos != (-1, -1):
                        if draw.isfree(pos):
                            draw.set(pos)
                        else:
                            draw.unset(pos)
            elif press_btn[2] == 1: # 右键移除棋子
                if draw.remove() == True: #有棋子移除
                    if core.gameover(draw.getmap()) == True:
                        gameover = True
                        setstatusbar('you win!')
                    else:
                        remove_list = core.caculate(draw.getmap())
                        draw.remove(remove_list)
                        if core.gameover(draw.getmap()) == True:
                            gameover = True
                            setstatusbar('ai win!')

                            

pygame.quit()


