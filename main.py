import pygame
import sys
from pygame.locals import *
pygame.init()
import random


width = 1280
height = 854
displaySurface = pygame.display.set_mode((width, height))
screen_rect = displaySurface.get_rect()
pygame.display.set_caption("Cats in Space")


background = pygame.image.load("stars.jpg").convert()
cat = pygame.image.load("spacecat.png").convert_alpha()

bullet = pygame.Surface((10,10)) #bullet is a rectangle
white = (255,255,255)
bullet.fill(white)


displaySurface.blit(background, (0,0))
displaySurface.blit(cat, (600, 800))
displaySurface.blit(bullet, (550,700))

pygame.display.flip()

catArea = cat.get_rect(bottomleft = (600,800))
bulletArea = bullet.get_rect(topleft=(catArea.centerx, catArea.top)) #bullet is positioned on cat's top center

bulletspeed = [0,-1]
bullets = []

pie = pygame.image.load("pie.png").convert_alpha()

pointEvent = pygame.event.Event(pygame.USEREVENT)
pygame.time.set_timer(pointEvent,2000)

pieList = [] # list of pies
speed2 = [0, 1]  # pies move down only
coordinateList = [] #list of coordinates for pie
speedList = [] #list of speeds for pies

#function to create new pies and add them to lists
def create_pie():
    pieArea = pie.get_rect(top=random.randint(-pie.get_height(), 0), left=random.randint(0, width - pie.get_width()))
    pieList.append(pie)
    coordinateList.append(pieArea)
    speedList.append(list(speed2))


clock = pygame.time.Clock()

while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == KEYDOWN: #if space is pressed, bullet shoots 
            if event.key == K_SPACE:
                bulletArea = bullet.get_rect(topleft=(catArea.centerx, catArea.top))
                bullets.append(bulletArea) 
        if event.type == pygame.USEREVENT: #creates pies every 2000milliseconds
            create_pie()
   


    pressings = pygame.key.get_pressed() #key pressings for cat, moves only horizontally and stays inside the screen
    if pressings[K_LEFT]:
        catArea.move_ip((-2,0))
    if pressings[K_RIGHT]:
        catArea.move_ip((2,0))  
    catArea.clamp_ip(screen_rect)

    for bulletArea in bullets: #bullet moves 
        bulletArea.move_ip((bulletspeed))

    # bullets = [bulletArea for bulletArea in bullets if bulletArea.bottom > 0]

    for i in range(len(pieList)):
            coordinateList[i].move_ip(speedList[i])
            if coordinateList[i].top > height:  # Remove pies that go below the screen
                del pieList[i]
                del coordinateList[i]
                del speedList[i]
                create_pie()  # Create a new pie


    j = 0
    for i in range(len(pieList)): #every time bullet hits the pie, it disappears and gets removed from the lists
        if bulletArea.colliderect(coordinateList[i - j]): 
            del pieList[i - j] 
            del coordinateList[i - j]
            del speedList[i - j]
            j += 1
            
    clock.tick(260) #speed of the game

    displaySurface.blit(background, (0,0))
    displaySurface.blit(cat, catArea)
    displaySurface.blit(bullet, bulletArea)

    for i in range(0,len(pieList)): #blits pies into the screen repeatedly
        displaySurface.blit(pieList[i], coordinateList[i])

    pygame.display.flip()