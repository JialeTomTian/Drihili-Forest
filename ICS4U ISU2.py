import pygame
import random 
import time
from pygame.locals import *

#------------------------------------------------------------------
#Always must have to play music
pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()

#Play Background music
pygame.mixer.music.load("Madagascar Escape.mp3") # setting music
pygame.mixer.music.set_volume(0.5) #setting volume(from 0 to 1)
pygame.mixer.music.play(-1) #playing it...-1 means loop endlessely
#-------------------------------------------------------------------


#Initialize of game and import of pictures
barracade = pygame.Rect(10, 10, 10, 10)
WIDTH = 1300
HEIGHT = 700
gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
characterImage = pygame.transform.scale(pygame.image.load('possible.png').convert_alpha(),(100,100))
characterImage = characterImage.convert_alpha()
mazeBackground = pygame.image.load('mazeBackground.jpg')
powerup = pygame.transform.scale(pygame.image.load('powerup.png').convert_alpha(),(50,50))

pygame.init()
white = 255,255,255
red = 255, 0 ,0
blue = 0,0,128
policeImage = pygame.transform.scale(pygame.image.load('Lion Chaser.png').convert_alpha(),(120,120))
clockobject = pygame.time.Clock()

#message to screen
def messageToScreen(msg,color,x,y,fontSize):
    '''
    messageToScreen is a function that outputs to the screen
    ---param
    msg: string
    color: tuple
    x:int(x coordinate)
    y:int(y coordinate)
    z:int(size of input text)
    ---return:none
    '''
    fontOne = pygame.font.Font('freesansbold.ttf',fontSize)
    screenText = fontOne.render(msg, True, color) #set message
    gameDisplay.blit(screenText,[x,y])
#end of messageToScreen

#Power Ups
class powerUps(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH),random.randint(50,HEIGHT))
    #end of initialization
#end of powerUps
        
#Chasing police officer
class movingPolice(pygame.sprite.Sprite):
    def __init__(self, image, initialX, initialY):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (initialX, initialY)
        self.x = initialX
        self.y = initialY
        self.__vy = 1
        self.__vx = 1
    #end of init

    def update(self):
        self.rect.y += (self.__vy)
        self.rect.x += (self.__vx)
    #end of update

    def changeSpeed(self, inputLocation):
        locationX = inputLocation[0]
        locationY = inputLocation[1]
        if self.rect.x > locationX:
            self.__vx = -1
        else:
            self.__vx = 1
        #end of if
        if self.rect.y > locationY:
            self.__vy = -1
        else:
            self.__vy = 1
        #end of if
    #end of changeSpeed

    def resetPosition(self):
        self.rect.center = (self.x, self.y)
    #end of resetPosition
#Character Class

class character(pygame.sprite.Sprite):
    '''
    character class used to gather information about character in the game
    '''
    def __init__(self, name, charImage, score = 0, health = 3):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.score = score
        self.image = charImage
        self.health = health
        self.rect = self.image.get_rect()
        self.rect.center = (500, 500)
    #end of __init__
    
    def update(self):
        start = time.time()
        self.__speedx = 0
        self.__speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.rect.left > -50:
            self.__speedx = -2
        if keystate[pygame.K_RIGHT] and self.rect.right < WIDTH+30:
            self.__speedx = 2
        if keystate[pygame.K_UP] and self.rect.top > 50:
            self.__speedy = -2
        if keystate[pygame.K_DOWN] and self.rect.bottom < HEIGHT+30:
            self.__speedy = +2
        self.rect.x += self.__speedx
        self.rect.y += self.__speedy
        end = time.time()
    #end of update

    def getPosition(self):
        #this returns the current position of the character
        return(self.rect.x, self.rect.y)
    #end of getPostion

    def plusScore(self):
        self.score += 1
    #end of plusScore

    def displayScore(self):
        messageToScreen("Your score is: " + str(self.score), red, 10, 10, 50)
    #end of displayScore

    def loseHealth(self):
        self.health -= 1
    #end of loseHealth

    def displayHealth(self):
        messageToScreen("Health: " + str(self.health), red, 800, 10, 50)
    #end of displayHealth

    def resetPosition(self):
        self.rect.center = (500,500)
    #end of resetPosition
#end of character

#Get character name
def getCharacterName():
    '''
    getCharacterName gets the name of the player
    ---param:none
    ---return:string
    '''
    output = ""
    gameDisplay.blit(mazeBackground, [0,0])
    messageToScreen("Please enter your name:", red, 300, 80, 50)
    pygame.display.update()
    endEvent = False
    while not(endEvent):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    endEvent = True
                elif event.key == pygame.K_SPACE:
                    output += chr(event.key)
                elif chr(event.key).isalpha():
                    output+=chr(event.key)
                    gameDisplay.blit(mazeBackground, [0,0])
                    messageToScreen("Please enter your name:", red, 300, 80, 50)
                    messageToScreen(output, red, 300, 150, 50)
                    pygame.display.update()
                elif event.key == pygame.K_BACKSPACE:
                    output = output[:len(output)-1]
                    gameDisplay.blit(mazeBackground, [0,0])
                    messageToScreen("Please enter your name:", red, 300, 80, 50)
                    messageToScreen(output, red, 300, 150, 50)
                    pygame.display.update()
                #end of if
            #end of if
        #end of for
    #end of while
    gameDisplay.blit(mazeBackground, [0,0])
    messageToScreen("Welcome " + output, red, 200, 200, 100)
    messageToScreen("Game starts in 3 seconds", red, 200, 400, 50)
    pygame.display.update()
    time.sleep(3)
    return(output)
#end of getCharacterName

dangers = pygame.sprite.Group()
playerSprite = pygame.sprite.Group()
powerSprite = pygame.sprite.Group()

def createPowerUps(number):
    ''' this function creates a certain number of powerups
    '''
    for counter in range(number):
        temp = powerUps(powerup)
        powerSprite.add(temp)
    #end of for
#end of createPowerUps

#Start game       
def startGame():
    exitGame = False
    
    ''' sets up game character and sprites '''
    counter = 0
    numberPower = 5
    createPowerUps(numberPower)
    name = getCharacterName()
    person = character(name, characterImage)
    police = movingPolice(policeImage, 200, 200)
    playerSprite.add(person)
    dangers.add(police)

    # collision detection and update screen
    def updateScreen():
        playerSprite.update()
        dangers.update()
        gameDisplay.fill(white)
        playerSprite.draw(gameDisplay)
        dangers.draw(gameDisplay)
        powerSprite.draw(gameDisplay)
        person.displayHealth()
        person.displayScore()
        pygame.display.flip()
        currentPosition = person.getPosition()
        police.changeSpeed(currentPosition)
    #end of updateScreen

    def collisionProcessing():
        hit = pygame.sprite.spritecollide(person, dangers, True)
        if hit:
            person.loseHealth()
            police.resetPosition()
            person.resetPosition()
            dangers.add(police) #Needs work on this section
            hit = False
        #end of if
        discovered = pygame.sprite.spritecollide(person,powerSprite, True)
        if discovered:
            discovered = False
            person.plusScore()
        #end of if
        if not(powerSprite):
            createPowerUps(numberPower)
        #end of if
    #end of collision Processing

    while not(exitGame):
        time.sleep(0.005)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exitGame = True
            #end of if
        #end of for
        collisionProcessing()
        updateScreen()
    #end of while
#end of startGame

#main menu
def mainMenu():
    '''
    mainMenu displays the main menu of the game
    no param and no return
    '''
    gameDisplay.blit(mazeBackground, [0,0]) #Sets backgound
    messageToScreen("Drihili Forest", red, 230, 80, 150)
    messageToScreen("Survive the longest you can!", red, 100, 300, 30)
    messageToScreen("Grab the Cubes!", red, 100, 400, 30)
    messageToScreen("Press C to Play, q to exit!", red, 100, 500, 30)
    pygame.display.update()
    gotEvent = False #Used to keep the while loop running
    while not(gotEvent):
        events = pygame.event.get() #Records events happening in the game
        for event in events:
            if event.type == pygame.QUIT: #If presses x button
                pygame.quit()
                gotEvent = True
            elif event.type == KEYDOWN and (event.key == K_x):
                pygame.quit()
                gotEvent = True
            elif event.type == KEYDOWN and (event.key == K_c):
                startGame()
            #end of if
        #end of for
    #end of while       
    #end of while
#end of mainMenu

mainMenu()
