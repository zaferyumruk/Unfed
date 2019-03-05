import pygame
from pygame import gfxdraw
import numpy as np
from gatherer import Gatherer, Rules, Food, Tasks, States, checkInRange
import random
from collections import defaultdict
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


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

    def update(self,gathererlist,foodlist) :
        self.gameDisplay.fill(Colors.white)
        self.infoHUD()
        # custominfoHUD(str(adam.evalPosition(eve)))

        foodcount = 0
        for food in foodlist:
            self.updateFoodOnBoard(food, foodcount)
            foodcount = foodcount + 1

        dudecount = 0
        for dude in gathererlist:
            self.updateGathererOnBoard(dude, dudecount)
            dudecount = dudecount + 1
            self.infoHUD(dude, dudecount)

        pygame.display.update()

    def updateFoodOnBoard(self, food, count):
        size = food.amount * 14 + len(food.boost) * 8
        color1 = self.colors[(count) % len(self.colors)]
        intpos = [int(pos) for pos in food.position]
        nametext = self.labelfont.render(food.foodtype.name, False,
                                    Colors.black)
        pygame.gfxdraw.box(
            self.gameDisplay,
            [intpos[0] - size / 2, intpos[1] - size / 2, size, size],
            color1)
        self.gameDisplay.blit(nametext, (intpos[0], intpos[1]))

    def updateGathererOnBoard(self,gatherer, count):
        color1 = self.colors[(count) % len(self.colors)]
        color2 = self.colors[(count + 1) % len(self.colors)]
        intpos = [int(pos) for pos in gatherer.position]
        dirlenscale = 15
        dirtippos = [
            int(pos + gatherer.direction[idx] * dirlenscale)
            for idx, pos in enumerate(gatherer.position)
        ]
        nametext = self.HUDfont.render(gatherer.name, False, Colors.black)
        datatext = self.HUDfont.render(
            str(gatherer.fatigue), False, Colors.black)
        statustext = self.labelfont.render(
            str(gatherer.state), False, Colors.black)
        namelabel = self.labelfont.render(
            str(gatherer.name), False, Colors.black)

        h = 25
        ybase = count * (h + 5)
        self.gameDisplay.blit(nametext, (10, ybase))
        self.gameDisplay.blit(datatext, (200, ybase))
        pygame.draw.rect(self.gameDisplay, Colors.black,
                            [60, ybase, 100, 25], 1)
        barvalue = int(gatherer.fatigue)
        # barvalue = int(gatherer.backpack * 20)
        if barvalue != 0:
            pygame.draw.rect(self.gameDisplay, Colors.red,
                                [60, ybase, barvalue, 25], 0)
        pygame.gfxdraw.filled_circle(self.gameDisplay, intpos[0],
                                        intpos[1], 15, color1)
        pygame.gfxdraw.filled_circle(self.gameDisplay, intpos[0],
                                        intpos[1], 5, color2)
        pygame.gfxdraw.line(self.gameDisplay, intpos[0], intpos[1],
                            dirtippos[0], dirtippos[1], color2)
        pygame.gfxdraw.circle(self.gameDisplay, intpos[0], intpos[1],
                              gatherer.visionRange, color2)
        self.gameDisplay.blit(statustext,
                                (gatherer.position[0], gatherer.position[1]))
        self.gameDisplay.blit(
            namelabel, (gatherer.position[0],
                        gatherer.position[1] - statustext.get_height()))

    def custominfoHUD(self, text):
        customtext = self.labelfont.render(text, False, Colors.black)
        self.gameDisplay.blit(customtext, (200, 200))

    def infoHUD(self, dude=None, count=0):
        watchedattrs = [
            'foodsaround','fatigue', 'state', 'backpack', 'stunnedleft', 'attackcd',
            'score', 'currenttask', 'direction'
        ]
        hy = 15
        hx = 120
        ystart = self.windowsize[1] - 25
        xstart = hx * (count + 1)
        if dude is not None:
            for attrname in watchedattrs:
                attr = getattr(dude, attrname)
                if (type(attr) is list) and len(attr) and (checkStrConvert(attr[0],float)):
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
                str(dude.name), False, Colors.black)
            self.gameDisplay.blit(datatext, (xstart, ystart))
        else:
            for attrname in watchedattrs:
                datatext = self.infofont.render(
                    str(attrname), False, Colors.black)
                self.gameDisplay.blit(datatext, (xstart, ystart))
                ystart = ystart - hy


class NewEra():
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.surface = Surface()

        self.tickrate = Rules.tickrate
        self.gathererupdatedict = defaultdict(lambda:None)
        self.clock = pygame.time.Clock()
        self.running = True
        self.updating = False

        self.gathererlist = []
        self.foodlist = []

        self.createEntities()

    def createEntities(self):
        pass

    def addFood(self, food):
        self.foodlist.append(food)

    def addGatherer(self, gatherer):
        self.gathererlist.append(gatherer)

    def grant2Gatherer(self,gatherer):
        self.informfoodsaround(gatherer)

    def informfoodsaround(self,gatherer):
        for food in self.foodlist:
            if checkInRange(gatherer.visionRange,gatherer.position,food.position):
                gatherer.informedfoodsaround(food)

    def advanceGatherer(self,gatherer):
        func = self.gathererupdatedict[gatherer]
        if func is not None:
            func(self, gatherer)
        gatherer.update()

    def begin(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.updating = True
                if event.type == pygame.KEYUP:
                    self.updating = False

            if self.updating:
                self.updateEntitites()
                self.updateSurface()

            self.clock.tick(self.tickrate)


    def assign2Gatherer(self, gatherer, func):
        if type(gatherer) is str:
            check = gatherer
        else:
            check = gatherer.name
        for activegatherer in self.gathererlist:
            if activegatherer.name == check:
                self.gathererupdatedict[activegatherer] = func

    def updateEntitites(self):
        randomgathererlist = self.gathererlist.copy()
        random.shuffle(randomgathererlist)
        for gatherer in randomgathererlist:
            self.grant2Gatherer(gatherer)
            self.advanceGatherer(gatherer)

    def updateSurface(self):
        self.surface.update(self.gathererlist,self.foodlist)

    def getRandomPos(self):
        return [
            np.random.randint(0, self.surface.windowsize[0]),
            np.random.randint(0, self.surface.windowsize[1])
        ]

def checkStrConvert(s,checktype):
    try:
        if type(s) is str:
            checktype(s)
            return True
        else:
            return False
    except ValueError:
        return False

myEra = NewEra()

myEra.addGatherer(Gatherer(name='adam', startingpos=myEra.getRandomPos()))
# myEra.addGatherer(Gatherer(name='eve', startingpos=myEra.getRandomPos()))
# myEra.addGatherer(Gatherer(name='cain', startingpos=myEra.getRandomPos()))
# myEra.addGatherer(Gatherer(name='abel', startingpos=myEra.getRandomPos()))

myEra.addFood(Food(startingpos=myEra.getRandomPos()))

myEra.addFood(Food(startingpos=[200, 300]))
myEra.addFood(Food(startingpos=[250, 350]))
myEra.addFood(Food(startingpos=[280, 380]))

# ! field should be removed, only gatherer should do the job!
def assignRandomCollect(field, gatherer):
    if gatherer.state == States.idle:
        if gatherer.foodsaround:
            gatherer.assignTask(Tasks.collect, gatherer.foodsaround[0])
        else:
            gatherer.assignTask(Tasks.wander)




myEra.assign2Gatherer('adam', assignRandomCollect)

myEra.begin()