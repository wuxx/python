#!/usr/bin/python
# coding=utf-8
# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu

import pygame

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
darkgreen = (0, 100,  0)

WHITE = 0
GREEN = 1
DARKGREEN = 2
# This sets the width and height of each grid location
width=20
height=20

grid_width = 7
grid_height = 7

# This sets the margin between each cell
margin=2

ignore = [(0,0), (1, 0), (0, 1), (1, 1), (5, 0), (6, 0), (5, 1), (6, 1), (0, 5), (1, 5), (0, 6), (1, 6), (5, 5), (6, 5), (5, 6), (6, 6)]
last_clicked = (-1, -1)
last_color = -1

# Create a 2 dimensional array. A two dimesional
# array is simply a list of lists.
grid=[]
for row in range(grid_height):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(grid_width):
        if (row, column) in ignore:
            grid[row].append(-1) 
        else:
            grid[row].append(1)

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
grid[3][3] = 0

# Initialize pygame
pygame.init()
 
# Set the height and width of the screen
size=[156,156]
screen=pygame.display.set_mode(size)

# Set title of screen
pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done=False

# Used to manage how fast the screen updates
clock=pygame.time.Clock()

# -------- Main Program Loop -----------
while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column=pos[0] // (width+margin)
            row=pos[1] // (height+margin)
            
            if (row, column) not in ignore:
                if grid[row][column] == WHITE: # 点击的是白子
                    if grid[last_clicked[0]][last_clicked[1]] == DARKGREEN:  #上次点击的是棋子
                        if row == last_clicked[0]:  # 同一行
                            if column == last_clicked[1] + 2 and grid[row][last_clicked[1]+1] == GREEN: # 有效
                                grid[row][column] = GREEN
                                grid[last_clicked[0]][last_clicked[1]] = WHITE 
                                grid[row][last_clicked[1]+1] = WHITE
                                last_clicked = (row, column)
                                last_color = GREEN
    
                            elif column == last_clicked[1] - 2 and grid[row][last_clicked[1]-1] == GREEN:
                                grid[row][column] = GREEN
                                grid[last_clicked[0]][last_clicked[1]] = WHITE
                                grid[last_clicked[0]][last_clicked[1]-1] = WHITE
                                last_clicked = (row, column)
                                last_color = GREEN
        
                        elif column == last_clicked[1]:  # 同一列
                            if row == last_clicked[0] + 2 and grid[last_clicked[0]+1][column] == GREEN:
                                grid[row][column] = GREEN
                                grid[last_clicked[0]][last_clicked[1]] = WHITE
                                grid[last_clicked[0]+1][last_clicked[1]] = WHITE
                                last_clicked = (row, column)
                                last_color = GREEN
    
                            elif row == last_clicked[0] - 2 and grid[last_clicked[0]-1][column] == GREEN:
                                grid[row][column] = GREEN
                                grid[last_clicked[0]][last_clicked[1]] = WHITE
                                grid[last_clicked[0]-1][last_clicked[1]] = WHITE
                                last_clicked = (row, column)
                                last_color = GREEN
                else:

                    if last_clicked != (-1, -1):
                        grid[last_clicked[0]][last_clicked[1]] = last_color

                    last_color = grid[row][column]
                    last_clicked = (row, column)
                    if grid[row][column] != WHITE:
                        grid[row][column] = DARKGREEN


            print("Click ",pos,"Grid coordinates: ",row,column)

    # Set the screen background
    screen.fill(black)

    # Draw the grid
    for row in range(grid_height):
        for column in range(grid_width):
            if grid[row][column] == WHITE:
                color = white
            elif grid[row][column] == GREEN:
                color = green
            elif grid[row][column] == DARKGREEN:
                color = darkgreen

            if (row, column) not in ignore:
                #pygame.draw.rect(screen,color,[(margin+width)*column+margin,(margin+height)*row+margin,width,height])
                pygame.draw.circle(screen,color,((margin+width)*column+margin+width/2,(margin+height)*row+margin+height/2) ,width/2, 0)
    
    # Limit to 20 frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()

