import pygame
from pygame import gfxdraw
import numpy as np
from gatherer import Gatherer, Rules, Food, Tasks, States
import random

class Colors():
    white = (255, 255, 255)
    black = (0, 0, 0)
    chocolate = (210, 105, 30)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    magenta = (255, 0, 255)


class Field():
    def __init__(self,windowsize = [800,600]):

        pygame.init()
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
        pygame.display.set_caption('Unfed')
        self.clock = pygame.time.Clock()
        self.running = True
        self.updating = False
        self.tickrate = Rules.tickrate
        self.gathererlist = []
        self.foodlist = []

    def addFood(self, food):
        self.foodlist.append(food)

    def addGatherer(self, gatherer):
        self.gathererlist.append(gatherer)

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
            'fatigue', 'state', 'backpack', 'stunnedleft', 'attackcd',
            'score', 'currenttask', 'direction'
        ]
        hy = 15
        hx = 120
        ystart = self.windowsize[1] - 25
        xstart = hx * (count + 1)
        if dude is not None:
            for attrname in watchedattrs:
                attr = getattr(dude, attrname)
                if type(attr) is list:
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

    def getRandomPos(self):
        return [
            np.random.randint(0, self.windowsize[0]),
            np.random.randint(0, self.windowsize[1])
        ]


    def main(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    # quit()
                # if event.type == pygame.MOUSEMOTION:
                if event.type == pygame.KEYDOWN:
                    self.updating = True
                    # for dude in gathererlist:
                    #     dude.assingdirection(list(np.random.rand(2) - 0.5))
                if event.type == pygame.KEYUP:
                    self.updating = False

            # myinfotext(3, apple.collected)

            if self.updating:
                self.gameDisplay.fill(Colors.white)
                self.infoHUD()
                # custominfoHUD(str(adam.evalPosition(eve)))
                # if adam.state == states.idle:
                #     adam.assignTask(tasks.attackmove, [eve])


                foodcount = 0
                for food in self.foodlist:
                    self.updateFoodOnBoard(food, foodcount)
                    foodcount = foodcount + 1

                dudecount = 0
                for dude in self.gathererlist:
                    dude.update()
                    self.updateGathererOnBoard(dude, dudecount)
                    dudecount = dudecount + 1
                    self.infoHUD(dude, dudecount)
                # myinfotext(3, apple.collected)
                pygame

            pygame.display.update()

            self.clock.tick(self.tickrate)



field = Field()

field.addGatherer(Gatherer(name='adam', startingpos=field.getRandomPos()))
field.addGatherer(Gatherer(name='eve', startingpos=field.getRandomPos()))
field.addGatherer(Gatherer(name='cain', startingpos=field.getRandomPos()))
field.addGatherer(Gatherer(name='abel', startingpos=field.getRandomPos()))

field.addFood(Food(startingpos=field.getRandomPos()))
field.addFood(Food(startingpos=field.getRandomPos()))
field.addFood(Food(startingpos=field.getRandomPos()))
field.addFood(Food(startingpos=field.getRandomPos()))
field.addFood(Food(startingpos=field.getRandomPos()))
field.addFood(Food(startingpos=field.getRandomPos()))
field.addFood(Food(startingpos=field.getRandomPos()))
field.addFood(Food(startingpos=field.getRandomPos()))
field.addFood(Food(startingpos=field.getRandomPos()))

for gatherer in field.gathererlist:
    gatherer.assignTask(Tasks.collect, random.choice(field.foodlist))

field.main()









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




#%%
