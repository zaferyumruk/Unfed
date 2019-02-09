#%%
import pygame
import numpy as np
from gatherer import gatherer
import random

pygame.init()

windowsize = (800,600)

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


pygame.font.init() # you have to call this at the start,
# if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 15) #This creates a new object on which you can call the render method.




gameDisplay = pygame.display.set_mode(windowsize)
pygame.display.set_caption('Unfed')
gameDisplay.fill(white)
clock = pygame.time.Clock()

Running = True
updating = False
tickrate = 60

adam = gatherer(tickrate=tickrate,startingpos=[400,300])

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
            # quit()
        # if event.type == pygame.MOUSEMOTION:
        if event.type == pygame.KEYDOWN:
            updating = True
            adam.assingdirection(list(np.random.rand(2)-0.5))
        if event.type == pygame.KEYUP:
            updating = False

    gameDisplay.fill(white)

    if updating:
        adam.update()
        pygame



    textsurface = myfont.render('Adam', False, black) #This creates a new surface with text already drawn onto it. At the end you can just blit the text surface onto your main screen.

    gameDisplay.blit(textsurface, (0, 0))
    pygame.draw.rect(gameDisplay, black, [50, 0, 100, 25], 1)
    pygame.draw.rect(gameDisplay, red, [50, 0,  int(adam.fatigue), 25], 0)
    pygame.draw.circle(gameDisplay, black, [int(pos) for pos in adam.position], 10)
    pygame.draw.circle(gameDisplay, red, [int(pos) for pos in adam.position],5)


    # quit()

    pygame.display.update()
    clock.tick(tickrate)
# crashed = False
# while not crashed:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             crashed = True
#         print(event)

#     pygame.display.update()

#     clock.tick(60)


# def updateScreen(self):




pygame.quit()

#%%
