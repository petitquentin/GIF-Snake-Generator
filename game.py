# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 19:48:56 2018

@author: petit
"""

import math
import random
from tkinter import *
from variables import *
import numpy as np
from PIL  import Image, ImageDraw
from autogen import *

def play_game(PATH = "data/nopath"):
    def matBoardGen(food, snake = []):
        matboard = np.zeros((NBROW, NBCOLUMN))
        for a in snake:
            matboard[a[0]][a[1]] = 1
        matboard[food[0]][food[1]] = 2
        return matboard

    def displayRefresh(snake, food, moves):
        board.delete("all")
        matboard = matBoardGen(food, snake)
        image = Image.new("RGB", (NBPIXELS * NBROW, NBPIXELS * NBCOLUMN), COLORBACKGROUND)
        draw = ImageDraw.Draw(image)


        for i in range (NBROW):
            for j in range (NBCOLUMN):
                if(matboard[i][j] != 0):
                    if(matboard[i][j] == 1):
                        rgb = []
                        rgb.append(math.floor(COLORTAIL[0] + snake.index([i, j]) * ((COLORHEAD[0]-COLORTAIL[0])/len(snake))))
                        rgb.append(math.floor(COLORTAIL[1] + snake.index([i, j]) * ((COLORHEAD[1]-COLORTAIL[1])/len(snake))))
                        rgb.append(math.floor(COLORTAIL[2] + snake.index([i, j]) * ((COLORHEAD[2]-COLORTAIL[2])/len(snake))))
                        color = (rgb[0], rgb[1], rgb[2])
                        board.create_rectangle(NBPIXELS*j + NBDECAL, NBPIXELS*i + NBDECAL, NBPIXELS*j + NBPIXELS + NBDECAL, NBPIXELS*i + NBPIXELS + NBDECAL, width = 0, fill ="#%02x%02x%02x" % color)
                        draw.rectangle([NBPIXELS*j + NBDECAL, NBPIXELS*i + NBDECAL, NBPIXELS*j + NBPIXELS + NBDECAL, NBPIXELS*i + NBPIXELS + NBDECAL], color)
                    else:
                        board.create_rectangle(NBPIXELS * j + NBDECAL, NBPIXELS * i + NBDECAL, NBPIXELS * j + NBPIXELS + NBDECAL, NBPIXELS * i + NBPIXELS + NBDECAL,width=0, fill="#%02x%02x%02x" % COLORFOOD)
                        draw.rectangle([NBPIXELS * j + NBDECAL, NBPIXELS * i + NBDECAL, NBPIXELS * j + NBPIXELS + NBDECAL, NBPIXELS * i + NBPIXELS + NBDECAL], COLORFOOD)
        board.pack()
        filename = PATH + "/{0:08}".format(moves) + ".png"
        image.save(filename)
        win.update_idletasks()
        win.update()



    def newFood(snake = []):
        if(len(snake) >= NBROW * NBCOLUMN):
            win.destroy()
            return -1
        newFood = [-1, -1]
        snake.append(newFood)

        while(newFood in snake):
            newFood = []
            newFood.append(random.randint(0, NBROW - 1))
            newFood.append(random.randint(0, NBCOLUMN - 1))
        return newFood




    def gameUpdate(event):
        global snake, food
        switcher = {
            37: [0, -1],
            38: [-1, 0],
            39: [0, 1],
            40: [1, 0]
        }
        nextMove =  [snake[len(snake)-1][0] + switcher.get(event.keycode, "Invalid Key")[0], snake[len(snake)-1][1] + switcher.get(event.keycode, [0, 0])[1]]
        if(nextMove[0] < NBROW and nextMove[0] >= 0 and nextMove[1] < NBCOLUMN and nextMove[1] >= 0 and (nextMove in snake) == False):
            snakeSize = "Snake size : " + str(len(snake))
            myString.configure(text=snakeSize)
            global nb_moves
            nb_moves += 1
            snake.append(nextMove)
            if(nextMove[0] == food[0] and nextMove[1] == food[1]):
                food = newFood(snake.copy())
                if(food == -1):
                    return -1
            else:
                snake.pop(0)
            displayRefresh(snake, food, nb_moves)
            if(len(snake) >= NBCOLUMN*NBROW):
                win.destroy()
        else:
            myString.configure(text="This move is impossible")

    def playGame(event):
        global inProgress, snake, food
        if(inProgress):
            return 0
        else:
            while(1):
                inProgress = True
                snakeBody = snake.copy()
                snakeEnd = snakeBody.pop(0)
                snakeHead = snakeBody.pop(len(snakeBody)-1)
                board = matBoardGen(food, snakeBody)
                graph = graphInitialization(board, snakeBody, food)
                headFoodExist, headFoodList = pathfinding(graph, food, snakeHead)
                if(headFoodExist):
                    print("headFoodList")
                    print(headFoodList)

                    #nextMove = headFoodList.pop(len(headFoodList)-2)
                    for e in headFoodList:
                        board[e[0]][e[1]] = 1
                    board[snakeHead[0]][snakeHead[1]] = 1
                    graph = graphInitialization(board, snakeBody, food)
                    foodEndExist, foodEndList = pathfinding(graph, food, snakeEnd)
                    print('foodEndList')
                    print(foodEndList)
                else:
                    foodEndExist = False
                if(foodEndExist and headFoodExist and (len(foodEndList) != 1)):
                    if(len(headFoodList) > 1):
                        nextMove = headFoodList[1]
                    else:
                        nextMove = food
                else:
                    board = matBoardGen(food, snakeBody)
                    print("PATHFINDING3")
                    graph = graphInitialization(board, snakeBody, food)
                    headEndExist, headEndList = pathfinding2(graph, snakeHead, snakeEnd)
                    if(headEndExist):
                        if(headEndList[len(headEndList)-1] != snakeHead):
                            nextMove = headEndList[len(headEndList)-1]
                        else:
                            nextMove = headEndList[len(headEndList) - 2]
                        if(nextMove == food or nextMove == snakeEnd):
                            switcher = {
                                37: [0, -1],
                                38: [-1, 0],
                                39: [0, 1],
                                40: [1, 0]
                            }
                            rd = random.randint(37,40)
                            nextMove = [snake[len(snake) - 1][0] + switcher.get(rd)[0],snake[len(snake) - 1][1] + switcher.get(rd)[1]]

                    else:
                        print("No path found")
                        win.destroy()
                print("nextMove")
                print(nextMove)
                print("snakeHead")
                print(snakeHead)
                print('snakeEnd')
                print(snakeEnd)
                print('food')
                print(food )
                if (nextMove[0] < NBROW and nextMove[0] >= 0 and nextMove[1] < NBCOLUMN and nextMove[1] >= 0 and (nextMove in snake) == False):
                    snakeSize = "Snake size : " + str(len(snake))
                    myString.configure(text=snakeSize)
                    global nb_moves
                    nb_moves += 1
                    snake.append(nextMove)
                    if (nextMove[0] == food[0] and nextMove[1] == food[1]):
                        food = newFood(snake.copy())
                        if (food == -1):
                            return -1
                    else:
                        snake.pop(0)
                    displayRefresh(snake, food, nb_moves)
                    if (len(snake) >= NBCOLUMN * NBROW):
                        win.destroy()
                else:
                    myString.configure(text="This move is impossible")


    # We check if the board is big enough
    if(NBROW <= 3 or NBCOLUMN < 3):
        return -1
    # Else
    win = Tk()
    win.title('GIF Snake Generator')
    board = Canvas(win, width =NBROW*NBPIXELS, height =NBCOLUMN*NBPIXELS, bg="black")
    myString = Label(win)
    myString.pack()
    if(ISPLAYABLE):
        win.bind_all("<KeyPress-Up>", gameUpdate)
        win.bind_all("<KeyPress-Down>", gameUpdate)
        win.bind_all("<KeyPress-Left>", gameUpdate)
        win.bind_all("<KeyPress-Right>", gameUpdate)
    else:
        win.bind_all("<KeyPress-space>", playGame)
        global inProgress
        inProgress = False
    # board.bind_all("<Button-1>", pointeur)

    global nb_moves
    global snake
    global food
    nb_moves = 0

    # Initialization of the snake

    snake = []
    snake.append([math.floor(NBROW-1),math.floor(NBCOLUMN/2-1)])
    snake.append([math.floor(NBROW-2),math.floor(NBCOLUMN/2-1)])
    snake.append([math.floor(NBROW-3),math.floor(NBCOLUMN/2-1)])

    food = newFood(snake.copy())
    print(food)
    displayRefresh(snake, food, nb_moves)
    snakeSize = "Snake size : " + str(len(snake))
    if(ISPLAYABLE):
        myString.configure(text = snakeSize)
    else:
        myString.configure(text="Press Space to start the generation")
    win.update_idletasks()
    win.update()




    win.mainloop()


    # board = np.ones((NBROW, NBCOLUMN))-1
    # board[math.floor(NBROW-3)][math.floor(NBCOLUMN/2-1)] = 2
    # board[math.floor(NBROW)-2][math.floor(NBCOLUMN/2-1)] = 1
    # board[math.floor(NBROW)-1][math.floor(NBCOLUMN/2-1)] = 1
    #
    # print(board)