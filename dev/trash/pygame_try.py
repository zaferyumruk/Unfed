import pygame
from pygame import gfxdraw
import numpy as np
from gatherer import gatherer, Rules, Food
import random




def main():
    pygame.init()

    windowsize = [800,600]



    white = (255,255,255)
    black = (0,0,0)
    chocolate = (210, 105, 30)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    magenta = (255, 0, 255)
    colors = [
        red,
        green,
        chocolate,
        magenta,
        blue
    ]


    pygame.font.init() # you have to call this at the start,
    # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 15) #This creates a new object on which you can call the render method.
    labelfont = pygame.font.SysFont('Comic Sans MS', 10, True)
    infofont = pygame.font.SysFont('tahoma', 13)


    gameDisplay = pygame.display.set_mode(windowsize)
    pygame.display.set_caption('Unfed')
    gameDisplay.fill(white)
    clock = pygame.time.Clock()

    Running = True
    updating = False
    tickrate = Rules.tickrate

    eve = gatherer(name='eve', startingpos=[100, 100])
    adam = gatherer(name='adam', startingpos=[400, 300])

    gathererlist = []
    gathererlist.append(gatherer(name='adam', startingpos=[400, 300]))
    gathererlist.append(gatherer(name='eve', startingpos=[420, 320]))
    gathererlist.append(gatherer(name='cain', startingpos=[380, 280]))
    gathererlist.append(gatherer(name='abel', startingpos=[340, 260]))
    apple = Food(startingpos=[380, 280])

    def updateGathererOnBoard(gatherer, count):
        color1 = colors[(count) % len(colors)]
        color2 = colors[(count + 1) % len(colors)]
        intpos = [int(pos) for pos in gatherer.position]
        dirlenscale = 15
        dirtippos = [int(gatherer.position[idx]+gatherer.direction[idx]*dirlenscale)
                    for idx in range(len(gatherer.position))]
        # dirangle = np.arctan(
        #     gatherer.direction[1] / gatherer.direction[0]) / np.pi * 360 + 180

        nametext = myfont.render( gatherer.name, False, black)
        datatext = myfont.render(str(gatherer.fatigue), False, black)
        statustext = labelfont.render(str(gatherer.state), False, black)
        namelabel = labelfont.render(str(gatherer.name), False, black)

        h = 25
        ybase = count*(h+5)
        gameDisplay.blit(nametext, (10, ybase))
        gameDisplay.blit(datatext, (200, ybase))
        pygame.draw.rect(gameDisplay, black, [60, ybase, 100, 25], 1)
        barvalue = int(gatherer.fatigue)
        # barvalue = int(gatherer.backpack * 20)
        if barvalue != 0:
            pygame.draw.rect(gameDisplay, red, [60, ybase, barvalue, 25], 0)
        pygame.gfxdraw.filled_circle(gameDisplay, intpos[0], intpos[1], 15,
                                        color1)
        pygame.gfxdraw.filled_circle(gameDisplay, intpos[0], intpos[1], 5,
                                        color2)
        pygame.gfxdraw.line(gameDisplay, intpos[0], intpos[1],
                            dirtippos[0], dirtippos[1], color2)
        # pygame.gfxdraw.pie(gameDisplay, intpos[0], intpos[1], 15,
        #                    int(dirangle + 15), int(dirangle - 15), color1)
        gameDisplay.blit(statustext,
                         (gatherer.position[0], gatherer.position[1]))
        gameDisplay.blit(
            namelabel,
            (gatherer.position[0], gatherer.position[1] - statustext.get_height()))


    def infoHUD(dude = None, count=0):
        watchedattrs = ['fatigue','state','backpack','stunnedleft','attackcd','score']
        hy = 15
        hx = 70
        ystart = windowsize[1] - 25
        xstart = hx * (count+1)
        if dude is not None:
            for attrname in watchedattrs:
                attr = getattr(dude, attrname)
                if type(attr) is float:
                    datatext = infofont.render('%.2f' % (attr), False, black)
                else:
                    datatext = infofont.render(str(attr), False, black)
                gameDisplay.blit(datatext, (xstart, ystart))
                ystart = ystart - hy
            datatext = infofont.render(str(dude.name), False, black)
            gameDisplay.blit(datatext, (xstart, ystart))
        else:
            for attrname in watchedattrs:
                datatext = infofont.render(str(attrname), False, black)
                gameDisplay.blit(datatext, (xstart, ystart))
                ystart = ystart - hy

    while Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                # quit()
            # if event.type == pygame.MOUSEMOTION:
            if event.type == pygame.KEYDOWN:
                updating = True
                for dude in gathererlist:
                    dude.assingdirection(list(np.random.rand(2) - 0.5))
            if event.type == pygame.KEYUP:
                updating = False

        # myinfotext(3, apple.collected)

        if updating:
            gameDisplay.fill(white)
            dudecount = 0
            infoHUD()
            for dude in gathererlist:
                dude.update()
                updateGathererOnBoard(dude, dudecount)
                dudecount = dudecount + 1
                infoHUD(dude,dudecount)
            # myinfotext(3, apple.collected)
            pygame

        pygame.display.update()

        clock.tick(tickrate)





# quit()

# crashed = False
# while not crashed:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             crashed = True
#         print(event)

#     pygame.display.update()

#     clock.tick(60)


# def updateScreen(self):



main()

#%%
