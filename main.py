import pygame
import sys
import random
from pygame.locals import *
pygame.init()


width = 1280
height = 900
displaySurface = pygame.display.set_mode((width, height))
screen_rect = displaySurface.get_rect()
pygame.display.set_caption("Cat VS Cakes")


background = pygame.image.load("universe.jpg").convert()
cat = pygame.image.load("spacecat.png").convert_alpha()
bullet = pygame.image.load("laser_bullet.png").convert_alpha()
gameover = pygame.image.load("universe.jpg").convert()
menu = pygame.image.load("main_menu.png").convert()
gameoverArea = gameover.get_rect(topleft=(-10000,-10000))
gameovertext = pygame.image.load("game_over_text.png").convert_alpha()

displaySurface.blit(background, (0, 0))
displaySurface.blit(cat, (600, 800))
displaySurface.blit(menu, (0, 0))

white = (255, 255, 255)
orange = ((255,100,10))
font = pygame.font.Font("freesansbold.ttf", 30)

menuArea = menu.get_rect(topleft=(0,0))
catArea = cat.get_rect(bottomleft=(600, 900))
gameovertextAREA = gameovertext.get_rect(midtop=(-5500,-5500))

howtoplay = font.render("Shoot evil cakes for points, missing cakes will decrease your points.", True, orange)
luck = font.render("Good Luck!", True, orange)

#bullets
bulletspeed = [0, -2]  # bullets move up only
bullets = []
bcoordinates = []
bspeedlist = []
bulletArea = bullet.get_rect(topleft=(catArea.centerx, catArea.top))  # bullet is positioned on cat's top center

def create_bullet():
    bulletArea = bullet.get_rect(topleft=(catArea.centerx, catArea.top)) 
    bullets.append(bullet)
    bcoordinates.append(bulletArea)
    bspeedlist.append(list(bulletspeed))

# cakes
pie = pygame.image.load("pie.png").convert_alpha()

pointEvent = pygame.event.Event(pygame.USEREVENT)
pygame.time.set_timer(pointEvent,1500)

pieList = [] # list of pies
speed2 = [0, 1]  # pies move down only
coordinateList = []  # list of coordinates for pie
speedList = []  # list of speeds for pies
points = 0

text = font.render('Points: '+str(points) , True, white)

#function to create new pies and add them to lists
def create_pie():
    pieArea = pie.get_rect(top=random.randint(-pie.get_height(), 0), left=random.randint(0, width - pie.get_width()))
    pieList.append(pie)
    coordinateList.append(pieArea)
    speedList.append(list(speed2))



clock = pygame.time.Clock()

pygame.mixer.music.load("gamemusic.wav")
pygame.mixer.music.play(-1)


while True:
    
    displaySurface.blit(menu, menuArea)
    displaySurface.blit(howtoplay, (150, 80))
    displaySurface.blit(luck, (550, 120))
    pygame.display.flip()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RETURN:
                    while True:
                        menuArea = menu.get_rect(topleft=(-1000,-1000))
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
                                    gameovertextAREA = gameovertext.get_rect(midtop=(600,400))

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

                        displaySurface.blit(text, (10,10))
                        displaySurface.blit(gameover, gameoverArea)
                        displaySurface.blit(menu, menuArea)
                        displaySurface.blit(gameovertext, gameovertextAREA)

                        pygame.display.flip()


