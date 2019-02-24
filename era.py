import pygame
import numpy as np
import random
from collections import defaultdict

from surface import Surface
from entities import Gatherer, Food, Task, State
from common import checkInRange, maxnorm
from rules import Rules

class Era():
    def __init__(self):

        pygame.init()

        self.surface = Surface()

        self.startingfoodcount = Rules.startingfoodcount
        self.foodrespawntickperiod = Rules.foodrespawntickperiod
        self.tickrate = Rules.tickrate
        self.spawnedfoodcap = Rules.spawnedfoodcap
        # self.logictickperiod = int(Rules.logictickrate / Rules.tickrate)

        self.gathererupdatedict = defaultdict(lambda:None)
        self.clock = pygame.time.Clock()
        self.running = True
        self.updating = False

        self.foodrespawncountdown = self.foodrespawntickperiod
        self.foodgrowing = True

        self.gathererlist = []
        self.foodlist = []

        self._entityIDdict = {}

    def createFoods(self):
        for _ in range(self.startingfoodcount):
            self.addFood(Food(startingpos=self.getRandomPos()))
        pass

    def addFood(self, food):
        self.foodlist.append(food)
        self._entityIDdict[food._uniqueID] = food

    def addGatherer(self, gatherer):
        self.gathererlist.append(gatherer)
        self._entityIDdict[gatherer._uniqueID] = gatherer

    # ! Implement
    def removeFood(self, idx):
        self._entityIDdict.pop(self.foodlist[idx]._uniqueID)
        self.foodlist.pop(idx)

    # # ! Implement
    # def removeGatherer(self, gatherer):
    #     self.gathererlist.append(gatherer)
    #     self.gathererIddict = {gatherer._uniqueID:gatherer}


    def id2entity(self,id):
        return self._entityIDdict[id]

    def entity2id(self,entity):
        return entity._uniqueID

    def grant2Gatherer(self,gatherer):
        self.informfoodsvisible(gatherer)

    def informfoodsvisible(self,gatherer):
        newlist = []
        for food in self.foodlist:
            if checkInRange(gatherer._visionRange,gatherer._position,food._position):
                newlist.append(food)
        gatherer._informedfoodsvisible(newlist)


    def informgatherersknown(self, gatherer):
        gatherer._gatherersknown = []
        for gat in self.gathererlist:
            if gat!=gatherer:
                gatherer._gatherersknown.append(gat)

    def advanceGatherer(self,gatherer):
        func = self.gathererupdatedict[gatherer]
        if func is not None:
            func(gatherer)
        gatherer._update()

    def begin(self):
        self.initEntities()
        while self.running:
            # step = step + 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.updating = True
                if event.type == pygame.KEYUP:
                    self.updating = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.dict['button'] == 1:
                        self.addFood(Food(startingpos=event.dict['pos']))

                    if event.dict['button'] == 3:
                        if self.foodgrowing:
                            self.foodgrowing = False
                        else:
                            self.foodgrowing = True

            if self.updating:

                self.spawnfood()
                self.updateEntitites()
                self.updateSurface()

            self.clock.tick(self.tickrate)

    def initEntities(self):
        self.createFoods()
        for gatherer in self.gathererlist:
            self.init4Gatherer(gatherer)

    # ! since no gatherer added later on, each informed of all others only once at the start
    def init4Gatherer(self,gatherer):
        self.informgatherersknown(gatherer)

    def assign2Gatherer(self, gatherer, func):
        if type(gatherer) is str:
            check = gatherer
        else:
            check = gatherer._name
        for activegatherer in self.gathererlist:
            if activegatherer._name == check:
                self.gathererupdatedict[activegatherer] = func

    def spawnfood(self):
        self.foodrespawncountdown -= 1
        if self.foodrespawncountdown == 0:
            self.foodrespawncountdown = self.foodrespawntickperiod
            if len(self.foodlist) < self.spawnedfoodcap and self.foodgrowing:
                self.addFood(Food(startingpos=self.getRandomPos()))


    def updateEntitites(self):
        randomgathererlist = self.gathererlist.copy()
        random.shuffle(randomgathererlist)
        for gatherer in randomgathererlist:
            self.grant2Gatherer(gatherer)
            self.advanceGatherer(gatherer)
        for idx, food in enumerate(self.foodlist):
            if not food._active and len(food._knownby)==0:
                self.removeFood(idx)

    def updateSurface(self):
        self.surface.update(self.gathererlist,self.foodlist,self.checkgameover())

    def getRandomPos(self):
        return [
            np.random.randint(0, self.surface.windowsize[0]),
            np.random.randint(0, self.surface.windowsize[1])
        ]

    def checkgameover(self):
        over = True
        allfoodconsumed = True
        for gatherer in self.gathererlist:
            if gatherer._state != State.exhausted:
                over = False
            if gatherer._backpack > 0.0:
                allfoodconsumed = False
        if over :
            if allfoodconsumed:
                return True
            else:
                for gatherer in self.gathererlist:
                    gatherer._modifier['eatspeed'] = 1000
                    gatherer._scoremultiplier = Rules.scoremultiplier2
