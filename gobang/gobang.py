#!/usr/bin/python
# coding=utf-8
import pygame 
import draw 


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
screen_info=[(800, 610), (10, 10), 2, 40, 14, 14, 'gobang']
pygame.init()
draw = draw.draw(screen_info)

end = False
while end == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: end = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            point = pygame.mouse.get_pos()
            pos = draw.getpos(point)
            print "get (%d, %d)" %(pos[0], pos[1])
        else:
            print "no event"

pygame.quit()


