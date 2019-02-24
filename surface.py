import pygame
from pygame import gfxdraw
import numpy as np

from common import checkStrConvert

class Colors():
    white = (255, 255, 255)
    black = (0, 0, 0)
    chocolate = (210, 105, 30)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    magenta = (255, 0, 255)


class Surface():
    def __init__(self, windowsize=[800, 600], caption='Unfed'):

        pygame.font.init()

        self.HUDfont = pygame.font.SysFont('Comic Sans MS', 15) #This creates a new object on which you can call the render method.
        self.labelfont = pygame.font.SysFont('Comic Sans MS', 10, True)
        self.infofont = pygame.font.SysFont('tahoma', 13)

        self.windowsize = windowsize
        self.colors = [
            Colors.black, Colors.chocolate, Colors.red, Colors.green,
            Colors.blue, Colors.magenta
        ]
        self.gameDisplay = pygame.display.set_mode(self.windowsize)
        self.gameDisplay.fill(Colors.white)
        pygame.display.set_caption(caption)

    def update(self,gathererlist,foodlist,gameover) :
        if gameover:
            self.gameDisplay.fill(Colors.blue)
        else:
            self.gameDisplay.fill(Colors.white)

        self.infoHUD()



        foodcount = 0
        for food in foodlist:
            self.updateFoodOnBoard(food, foodcount)
            foodcount = foodcount + 1

        dudecount = 0
        for dude in gathererlist:
            self.updateGathererOnBoard(dude, dudecount)
            dudecount = dudecount + 1
            self.infoHUD(dude, dudecount)


        #CUSTOM DEBUG TEXT
        # txt1 = gathererlist[1]._name + ' facing ' + gathererlist[0]._name + 'with '
        # self.custominfoHUD(txt1 + str(gathererlist[0].getfacing(gathererlist[1])) + ' degrees')

        afood = gathererlist[1].closestgatherer()
        if afood is not None:
            # txt1 = afood._foodtype.name + ' staying in ' + str(gathererlist[1].getdirection(afood))
            txt1 = afood._name + ' staying in ' + str(
                gathererlist[1].getdirection(afood))
            self.custominfoHUD( txt1 + 'degrees wrt ' + gathererlist[1]._name)

        pygame.display.update()

    def updateFoodOnBoard(self, food, count):
        count = food._uniqueID
        unitsize = 2
        if food._active:
            size = food._amount * unitsize + len(food._boost) * unitsize*2
        else:
            size = unitsize
        color1 = self.colors[(count) % len(self.colors)]
        intpos = [int(pos) for pos in food._position]
        nametext = self.labelfont.render(food._foodtype.name, False,
                                    Colors.black)
        if food._active:
            pygame.gfxdraw.box(
                self.gameDisplay,
                [intpos[0] - size / 2, intpos[1] - size / 2, size, size],
                color1)
            self.gameDisplay.blit(nametext, (intpos[0], intpos[1]))
        else:
            pygame.gfxdraw.box(
                self.gameDisplay,
                [intpos[0] - size / 2, intpos[1] - size / 2, size, size],
                color1)


    def updateGathererOnBoard(self,gatherer, count):
        color1 = self.colors[(count) % len(self.colors)]
        color2 = self.colors[(count + 1) % len(self.colors)]
        intpos = [int(pos) for pos in gatherer._position]
        dirlenscale = 15
        dirtippos = [
            int(pos + gatherer._direction[idx] * dirlenscale)
            for idx, pos in enumerate(gatherer._position)
        ]

        statustext = self.labelfont.render(
            str(gatherer._state), False, Colors.black)
        namelabel = self.labelfont.render(
            str(gatherer._name), False, Colors.black)

        # fatigueinfoBar(self, gatherer, count)

        pygame.gfxdraw.filled_circle(self.gameDisplay, intpos[0],
                                        intpos[1], 15, color1)
        pygame.gfxdraw.filled_circle(self.gameDisplay, intpos[0],
                                        intpos[1], 5, color2)
        pygame.gfxdraw.line(self.gameDisplay, intpos[0], intpos[1],
                            dirtippos[0], dirtippos[1], color2)
        pygame.gfxdraw.circle(self.gameDisplay, intpos[0], intpos[1],
                              gatherer._visionRange, color2)
        self.gameDisplay.blit(statustext,
                                (gatherer._position[0], gatherer._position[1]))
        self.gameDisplay.blit(
            namelabel, (gatherer._position[0],
                        gatherer._position[1] - statustext.get_height()))

    def custominfoHUD(self, text):
        customtext = self.labelfont.render(text, False, Colors.black)
        self.gameDisplay.blit(customtext, (200, 200))

    def fatigueinfoBar(self,gatherer,count):

        nametext = self.HUDfont.render(gatherer._name, False, Colors.black)
        datatext = self.HUDfont.render(str(gatherer._fatigue), False, Colors.black)

        h = 25
        ybase = count * (h + 5)

        self.gameDisplay.blit(nametext, (10, ybase))
        self.gameDisplay.blit(datatext, (200, ybase))
        pygame.draw.rect(self.gameDisplay, Colors.black,
                            [60, ybase, 100, 25], 1)
        barvalue = int(gatherer._fatigue)
        # barvalue = int(gatherer._backpack * 20)
        if barvalue != 0:
            pygame.draw.rect(self.gameDisplay, Colors.red,
                                [60, ybase, barvalue, 25], 0)

    def infoHUD(self, dude=None, count=0):
        watchedattrs = [
            '_foodsknowncount', '_fatigue', '_state', '_backpack',
            '_stunnedleft', '_attackcd', '_score', '_currenttask'
        ]
        hy = 15
        hx = 120
        ystart = self.windowsize[1] - 25
        xstart = hx * (count + 1)
        if dude is not None:
            for attrname in watchedattrs:
                attr = getattr(dude, attrname)
                if (type(attr) is list) and len(attr)>0 and (checkStrConvert(attr[0],float)):
                    bb = '%.2f:' * len(attr)
                    datatext = self.infofont.render(bb % tuple(attr), False,
                                                    Colors.black)
                elif type(attr) is float:
                    datatext = self.infofont.render('%.2f' % (attr), False,
                                                    Colors.black)
                else:
                    datatext = self.infofont.render(
                        str(attr), False, Colors.black)
                self.gameDisplay.blit(datatext, (xstart, ystart))
                ystart = ystart - hy
            datatext = self.infofont.render(
                str(dude._name), False, Colors.black)
            self.gameDisplay.blit(datatext, (xstart, ystart))
        else:
            for attrname in watchedattrs:
                datatext = self.infofont.render(
                    str(attrname), False, Colors.black)
                self.gameDisplay.blit(datatext, (xstart, ystart))
                ystart = ystart - hy