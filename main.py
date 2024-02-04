import pygame
import sys
import random
from pygame.locals import *
pygame.init()


width = 1280
height = 854
displaySurface = pygame.display.set_mode((width, height))
screen_rect = displaySurface.get_rect()
pygame.display.set_caption("Cat VS Cakes")


background = pygame.image.load("cartoon_space.png").convert()
cat = pygame.image.load("spacecat.png").convert_alpha()
bullet = pygame.image.load("laser_bullet.png").convert_alpha()

displaySurface.blit(background, (0, 0))
displaySurface.blit(cat, (600, 800))

pygame.display.flip()

catArea = cat.get_rect(bottomleft=(600, 900))

white = (255, 255, 255)
pink = (255, 0, 130)

bulletEvent = pygame.event.Event(pygame.USEREVENT + 1)
pygame.time.set_timer(bulletEvent, 1000)

bulletspeed = [0, -1]  # bullets move up only
bullets = []
bcoordinates = []
bspeedlist = []
bulletArea = bullet.get_rect(topleft=(catArea.centerx, catArea.top))  # bullet is positioned on cat's top center


def create_bullet():
    bulletArea = bullet.get_rect(topleft=(catArea.centerx, catArea.top)) 
    bullets.append(bullet)
    bcoordinates.append(bulletArea)
    bspeedlist.append(list(bulletspeed))


# here pie and lists are created
pie = pygame.image.load("pie.png").convert_alpha()

pointEvent = pygame.event.Event(pygame.USEREVENT)
pygame.time.set_timer(pointEvent,1500)

pieList = [] # list of pies
speed2 = [0, 1]  # pies move down only
coordinateList = []  # list of coordinates for pie
speedList = []  # list of speeds for pies

points = 0
font = pygame.font.Font("freesansbold.ttf", 30)
text = font.render('Points: '+str(points) , True, white)

#function to create new pies and add them to lists
def create_pie():
    pieArea = pie.get_rect(top=random.randint(-pie.get_height(), 0), left=random.randint(0, width - pie.get_width()))
    pieList.append(pie)
    coordinateList.append(pieArea)
    speedList.append(list(speed2))

gameover = pygame.Surface((1280,905))
gameover.fill(white)
endingtext = font.render("Game Over!", True, pink)
textArea = endingtext.get_rect()
textArea.center = (-300, -400)
gameoverArea = gameover.get_rect(topleft=(-1000,-1000))

clock = pygame.time.Clock()

pygame.mixer.music.load("gamemusic.wav")
pygame.mixer.music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_SPACE:
                create_bullet()
        if event.type == pygame.USEREVENT:  # creates pies every 2000milliseconds
            create_pie()

    pressings = pygame.key.get_pressed()  # key pressings for cat, moves only horizontally and stays inside the screen
    if pressings[K_LEFT]:
        catArea.move_ip((-2, 0))
    if pressings[K_RIGHT]:
        catArea.move_ip((2, 0))
    catArea.clamp_ip(screen_rect)

    for i in range(len(bullets)):
        bcoordinates[i].move_ip(bspeedlist[i])

    for i in range(len(pieList)):
        coordinateList[i].move_ip(speedList[i])
        if coordinateList[i].top > height:  # Remove pies that go below the screen
            del pieList[i]
            del coordinateList[i]
            del speedList[i]
            create_pie()  # Create a new pie
            points = points-2
            text = font.render('Points: '+str(points), True, white)
            if points <= 0:
                gameoverArea = gameover.get_rect(topleft=(0,0)) # gameover screen appears
                textArea = endingtext.get_rect(center = (600, 452))

    j = 0  # every time a collision between pie and bullet happens, both of them are removed from the lists
    for i in range(len(pieList) - 1, -1, -1):
        for j, bulletArea in enumerate(bcoordinates):
            if bulletArea.colliderect(coordinateList[i]):
                points = points + 1
                text = font.render('Points: '+str(points), True, white)
                del pieList[i]
                del coordinateList[i]
                del speedList[i]
                del bcoordinates[j]
                del bspeedlist[j]
                del bullets[j]
                break

    clock.tick(260)  # speed of the game

    displaySurface.blit(background, (0, 0))
    displaySurface.blit(cat, catArea)

    for i in range(0, len(bullets)):  # blits bullets into the screen
        displaySurface.blit(bullets[i], bcoordinates[i])
    for i in range(0, len(pieList)):  # blits pies into the screen repeatedly
        displaySurface.blit(pieList[i], coordinateList[i])
    displaySurface.blit(text, (0,0))
    displaySurface.blit(gameover, gameoverArea)
    displaySurface.blit(endingtext,textArea)
    pygame.display.flip()
