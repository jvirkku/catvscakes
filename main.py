import pygame
import sys
from pygame.locals import *
pygame.init()
import random

print("hell yeah this is a game")

width = 1280
height = 854
displaySurface = pygame.display.set_mode((width, height))
screen_rect = displaySurface.get_rect()
pygame.display.set_caption("Cats in Space")

background = pygame.image.load("stars.jpg").convert()
cat = pygame.image.load("spacecat.png").convert_alpha()


displaySurface.blit(cat, (600, 800))
displaySurface.blit(background, (0,0))

pygame.display.flip()

catArea = cat.get_rect(bottomleft = (600,800))



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()




    pressings = pygame.key.get_pressed()
    if pressings[K_LEFT]:
        catArea.move_ip((-2,0))
    if pressings[K_RIGHT]:
        catArea.move_ip((2,0))
    
    catArea.clamp_ip(screen_rect)


    displaySurface.blit(background, (0,0))
    displaySurface.blit(cat, catArea)

    pygame.display.flip()