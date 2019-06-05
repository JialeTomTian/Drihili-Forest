import pygame
import random 
import time
from pygame.locals import *

#------------------------------------------------------------------
#Always must have to play music
pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()

#Play Background music
#pygame.mixer.music.load("Madagascar Escape.mp3") # setting music
#pygame.mixer.music.set_volume(0.5) #setting volume(from 0 to 1)
#pygame.mixer.music.play(-1) #playing it...-1 means loop endlessely
#-------------------------------------------------------------------


#Initialize of game and import of pictures
barracade = pygame.Rect(10, 10, 10, 10)
WIDTH = 1300
HEIGHT = 700

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
wallImage = pygame.transform.scale(pygame.image.load('block.png').convert_alpha(),(50, 50))
emptyImage = pygame.transform.scale(pygame.image.load('empty.png').convert_alpha(),(50,50))
powerUp = pygame.transform.scale(pygame.image.load('powerup.png').convert_alpha(),(50,50))
pygame.init()
white = 255,255,255
red = 255, 0 ,0
blue = 0,0,128


class cell(pygame.sprite.Sprite):
    w, h = 50, 50
    def __init__(self, locationX, locationY, isWall, isPowerUp, image, rowPosition, columnPosition):
        pygame.sprite.Sprite.__init__(self)
        self.isWall = isWall
        if locationX == 100 and locationY == 100:
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.center = (locationX, locationY)
            self.origin = True
            self.rowPosition = rowPosition
            self.columnPosition = columnPosition
        elif isWall:
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.center = (locationX, locationY)
            self.rowPosition = rowPosition
            self.columnPosition = columnPosition
        else:
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.center= (locationX, locationY)
            self.rowPosition = rowPosition
            self.columnPosition = columnPosition
        #end of if
    #end of initialization

    def getLocation(self):
        return(self.rowPosition, self.columnPosition)
    #end of getLocation

    def checkWall(self):
        return(self.isWall)
    #end of checkWall(self):
#end of cell

def mapGeneration():
    def createMap():
        myX = list(range(400, 800, 50))
        myY = list(range(300, 600, 50))
        setA = random.choice(myX)
        setB = random.choice(myY)
        cells = []
        emptySpace = pygame.sprite.Group()
        specialSpace = pygame.sprite.Group()
        blockedWalls = pygame.sprite.Group()
        rowPosition = 0
        columnPosition = 0
        for counter in range(100, 800,50):
            columnPosition = 0
            row = []
            for value in range(100,600,50):
                check = random.randint(0,1)
                if counter == 100 and value == 100:
                    temp = cell(counter, value, False, False, emptyImage, rowPosition, columnPosition)
                    emptySpace.add(temp)
                elif counter == setA and value == setB:
                    temp = cell(counter, value, False, True, powerUp, rowPosition, columnPosition)
                    temp.isWall = "Score"
                    specialSpace.add(temp)
                elif not(check):
                    temp = cell(counter,value, True, False, wallImage, rowPosition, columnPosition)
                    blockedWalls.add(temp)
                else:
                    temp = cell(counter,value, False, False, emptyImage, rowPosition, columnPosition)
                    emptySpace.add(temp)
                row.append(temp)
                columnPosition += 1
            #end of for
            rowPosition += 1
            cells.append(row)
        #end of counter
        return(emptySpace, specialSpace, blockedWalls, cells)
    #end of createMap

    def checkMap(cells):
        checkList = cells.copy()
        start = checkList[0][0]
        queueList = [start]
        visitedList = [[0,0]]
        found = False
        moveCoordinates = [[1,0],[0,1],[-1,0],[0,-1]]
        while len(queueList) > 0 and not(found):
            check = queueList.pop(0)
            tempX,tempY = check.getLocation()
            for move in moveCoordinates:
                row = tempX + move[0]
                column = tempY + move[1]
                if (row > -1 and row <14) and (column > -1 and column < 10):
                    wallCheck = checkList[row][column].checkWall()
                    '''
                    print(" ")
                    print("Current:",(tempX, tempY))
                    print(row, column)
                    print(wallCheck)
                    print(visitedList)
                    print([row,column] in visitedList)
                    '''
                    if not(wallCheck) and [row,column] not in visitedList:
                        queueList.append(checkList[row][column])
                        visitedList.append([row,column])
                    elif (wallCheck == "Score"):
                        found = True
                    #print(queueList)
                #end of if
            #end of for
        #end of while
        return(found)
    #end of checkMap
    
    notMatched = True
    while notMatched:
        emptySpace, specialSpace, blockedWalls, cells = createMap()
        if checkMap(cells):
            return(emptySpace, specialSpace, blockedWalls, cells)
#end of mapGenearation


emptySpace, specialSpace, blockedWalls, cells = mapGeneration()
emptySpace.draw(gameDisplay)
blockedWalls.draw(gameDisplay)
specialSpace.draw(gameDisplay)
pygame.display.flip()





















