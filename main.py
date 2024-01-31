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
pie = pygame.image.load("pie.png").convert_alpha()

bullet = pygame.Surface((10,10))
white = (255,255,255)
bullet.fill(white)


displaySurface.blit(background, (0,0))

displaySurface.blit(cat, (600, 800))
displaySurface.blit(pie, (0,0))
displaySurface.blit(bullet, (550,700))


pygame.display.flip()

catArea = cat.get_rect(bottomleft = (600,800))
pieArea = pie.get_rect()
pieArea.left = random.randrange(0,1280,1) #pie is randomly on the top of the screen
pieArea.top = 0
bulletArea = bullet.get_rect(topleft=(catArea.centerx, catArea.top)) #bullet is positioned on cat's top center


speed = [0,-1]
bullets = []


while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bulletArea = bullet.get_rect(topleft=(catArea.centerx, catArea.top))
                bullets.append(bulletArea) 
    

    pressings = pygame.key.get_pressed()
    if pressings[K_LEFT]:
        catArea.move_ip((-2,0))
    if pressings[K_RIGHT]:
        catArea.move_ip((2,0))  
    catArea.clamp_ip(screen_rect)

    for bulletArea in bullets:
        bulletArea.move_ip((speed))

   
    bullets = [bulletArea for bulletArea in bullets if bulletArea.bottom > 0]



    displaySurface.blit(background, (0,0)) #replaces the need to have dispsurf.blit.background
    
    displaySurface.blit(cat, catArea)
    displaySurface.blit(pie, pieArea)
    displaySurface.blit(bullet, bulletArea)
    
    pygame.display.flip()