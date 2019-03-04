import pygame
from pygame import gfxdraw
import numpy as np
from entities import Foodtype

from common import checkStrConvert
from rules import Rules

class Colors():
    white = [255, 255, 255]
    black = [0, 0, 0]
    gray = [80, 80, 80]
    chocolate = [210, 105, 30]
    red = [255, 0, 0]
    yellow = [255, 255, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]
    magenta = [255, 0, 255]
    groundgreen = [50,80,50]
    darkgrey = [35,35,35]


class GameWindow():
    def __init__(self, windowsize=[800, 600], caption='Unfed', bounds = [[0,800],[0,600]]):

        pygame.font.init()

        self.HUDfont = pygame.font.SysFont('Comic Sans MS', 15) #This creates a new object on which you can call the render method.
        self.labelfont = pygame.font.SysFont('Comic Sans MS', 10, True)
        self.infofont = pygame.font.SysFont('tahoma', 13)

        self.windowsize = windowsize
        self.colors = [Colors.chocolate, Colors.red, Colors.green,
            Colors.blue, Colors.magenta
        ]
        self.gameDisplay = pygame.display.set_mode(self.windowsize)
        self.gameDisplay.fill(Colors.black)

        pygame.display.set_caption(caption)


        self.unitsize = Rules.unitsize
        self.acttop = bounds[0][0]
        self.actleft = bounds[1][0]
        self.actheight = bounds[0][1] - self.acttop
        self.actwidth = bounds[1][1] - self.actleft
        self.activerect = [self.acttop,self.actleft,self.actheight,self.actwidth]


        self.bordercolor = Colors.darkgrey
        self.borderxbase = self.actleft+self.actwidth
        self.borderybase = self.actleft+self.actwidth
        self.borderwidth = self.windowsize[0] - self.actwidth

        self.watchedattrs = [
            '_foodsknowncount', '_fatigue', '_state', '_backpack',
            '_stunnedleft', '_attackcd', '_score', '_currenttask'
        ]
        self.infoHUDhy = 15
        self.infoHUDhx = 120
        self.infoHUDystart = self.windowsize[1] - 25

        self.fog = pygame.Surface(Rules.Map.size)
        self.playzone = pygame.Surface(Rules.Map.size)

        self.foodcolor = {Foodtype.berry: Colors.red,
            Foodtype.apple : Colors.green,
            Foodtype.pineapple : Colors.yellow}

        pygame.display.update()


    def update(self,era) :

        self.gameDisplay.fill(Colors.black)

        # pygame.display.update()

        gathererlist = era.gathererlist
        foodlist = era.foodlist
        gameover = era.checkgameover()

        self.playzone.fill(Colors.groundgreen)
        self.fog.fill(Colors.white)
        # pygame.gfxdraw.box(self.gameDisplay, self.activerect , Colors.red + [10])

        # pixels = pygame.surfarray.pixels2d(self.fog)
        # pixels ^= 2 ** 32 - 1
        # del(pixels)
        # if gameover:
        #     self.gameDisplay.fill(Colors.blue)
        # else:
        #     self.gameDisplay.fill(Colors.white)

        # self.infoHUD()

        for food in foodlist:
            self.updateFoodOnBoard(food)

        # dudecount = 0
        for dude in gathererlist:
            self.updateGathererOnBoard(dude)
            # dudecount = dudecount + 1
            # self.infoHUD(dude, dudecount)

        self.infoHUD(gathererlist)

        self.fatigueinfoBar(gathererlist)

        self.fog.set_alpha(30,2)

        self.gameDisplay.blit(self.playzone,[self.acttop,self.actleft])
        self.gameDisplay.blit(self.fog,[self.acttop,self.actleft])

        #CUSTOM DEBUG TEXT

        # txt1 = gathererlist[0]._name + ' facing ' + gathererlist[-1]._name + 'with '
        # self.custominfoHUD(txt1 + str(gathererlist[-1].getfacing(gathererlist[0])) + ' degrees')

        # afood = gathererlist[1].closestgatherer()
        # if afood is not None:
        #     # txt1 = afood._foodtype.name + ' staying in ' + str(gathererlist[1].getdirection(afood))
        #     txt1 = afood._name + ' staying in ' + str(
        #         gathererlist[1].getdirection(afood))
        #     self.custominfoHUD( txt1 + 'degrees wrt ' + gathererlist[1]._name)
        # self.gameDisplay.blit(self.fog,[0,0])


        pygame.display.update()

    def updateFoodOnBoard(self, food):
        count = food._uniqueID

        if food._active:
            size =int ( food._amount * self.unitsize + len(food._boost) * self.unitsize*2 )
        else:
            size = int (self.unitsize)
        # color1 = self.colors[(count) % len(self.colors)]
        color1 = self.foodcolor[food._foodtype]
        intpos = [int(pos) for pos in food._position]
        nametext = self.labelfont.render(food._foodtype.name, False,
                                    Colors.black)
        if food._active:
            pygame.gfxdraw.box(
                self.playzone,
                [intpos[0] - size / 2, intpos[1] - size / 2, size, size],
                color1)
            self.playzone.blit(nametext, (intpos[0], intpos[1]))
        else:
            pygame.gfxdraw.box(
                self.playzone,
                [intpos[0] - size / 2, intpos[1] - size / 2, size, size],
                color1)


    def updateGathererOnBoard(self,gatherer):
        innerradius = int(self.unitsize * 2)
        outerradius = int(self.unitsize * 7)
        count = gatherer._uniqueID

        color1 = self.colors[(count) % len(self.colors)]
        color2 = self.colors[(count + 1) % len(self.colors)]
        intpos = [int(pos) for pos in gatherer._position]
        dirlenscale = int(self.unitsize * 7)
        dirtippos = [
            int(pos + gatherer._direction[idx] * dirlenscale)
            for idx, pos in enumerate(gatherer._position)
        ]

        statustext = self.labelfont.render(
            str(gatherer._state), False, Colors.white)
        namelabel = self.labelfont.render(
            str(gatherer._name), False, Colors.white)

        pygame.gfxdraw.filled_circle(self.playzone, intpos[0],
                                        intpos[1], outerradius, color1)
        pygame.gfxdraw.filled_circle(self.playzone, intpos[0],
                                        intpos[1], innerradius, color2)
        pygame.gfxdraw.line(self.playzone, intpos[0], intpos[1],
                            dirtippos[0], dirtippos[1], color2)
        # pygame.gfxdraw.circle(self.gameDisplay, intpos[0], intpos[1],
        #                       gatherer._visionRange, color1+[120])

        pygame.gfxdraw.filled_circle(self.fog, intpos[0],
                                        intpos[1], gatherer._visionRange, Colors.black)
        self.playzone.blit(statustext,
                                (gatherer._position[0], gatherer._position[1]))
        self.playzone.blit(
            namelabel, (gatherer._position[0],
                        gatherer._position[1] - statustext.get_height()))

    def custominfoHUD(self, text):
        customtext = self.labelfont.render(text, False, Colors.black)
        self.gameDisplay.blit(customtext, (200, 200))

    def fatigueinfoBar(self,gathererlist):
        gathererlist.sort(key=lambda x: x._score,reverse = True)
        ybezel = 20
        xbase = Rules.Map.bounds[0][1]+20
        for idx,gatherer in enumerate(gathererlist):
            count = gatherer._uniqueID
            color1 = self.colors[(count) % len(self.colors)]

            nametext = self.HUDfont.render(gatherer._name, False, Colors.white)
            datatext = self.HUDfont.render('%d'% (gatherer._score), False, Colors.white)

            h = 25
            ybase = idx * (h + 5) + ybezel


            pygame.draw.rect(self.gameDisplay, Colors.white,
                                [xbase, ybase, 100, 25], 1)
            barvalue = int(gatherer._fatigue/Rules.startingfatigue * 100)
            # barvalue = int(gatherer._backpack * 20)
            if barvalue != 0:
                pygame.draw.rect(self.gameDisplay, color1,
                                    [xbase, ybase, barvalue, 25], 0)

            self.gameDisplay.blit(nametext, (xbase+10, ybase))
            self.gameDisplay.blit(datatext, (xbase+120, ybase))


    def drawborder(self):
        pygame.draw.rect(self.gameDisplay, self.bordercolor,[self.borderxbase, self.borderybase, self.actheight, self.borderwidth], 0)

    def infoHUD(self, gathererlist):
        drawsurface = self.gameDisplay
        for attrname in self.watchedattrs:
            self.infoHUDxstart = self.infoHUDhx
            datatext = self.infofont.render(
                str(attrname), False, Colors.black)
            drawsurface.blit(datatext,
                             (self.infoHUDxstart, self.infoHUDystart))
            self.infoHUDystart = self.infoHUDystart - self.infoHUDhy

        for idx, gatherer in enumerate(gathererlist):
            self.infoHUDxstart = self.infoHUDhx * (idx + 1)
            for attrname in self.watchedattrs:
                attr = getattr(gatherer, attrname)
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
                drawsurface.blit(datatext,
                                 (self.infoHUDxstart, self.infoHUDystart))
                self.infoHUDystart = self.infoHUDystart - self.infoHUDhy
            datatext = self.infofont.render(
                str(gatherer._name), False, Colors.black)
            drawsurface.blit(datatext,
                             (self.infoHUDxstart, self.infoHUDystart))
