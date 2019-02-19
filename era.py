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
        # self.logictickperiod = int(Rules.logictickrate / Rules.tickrate)

        self.gathererupdatedict = defaultdict(lambda:None)
        self.clock = pygame.time.Clock()
        self.running = True
        self.updating = False

        self.gathererlist = []
        self.foodlist = []

        self.entityIDdict = {}

        self.createEntities()

    def createEntities(self):
        for _ in range(self.startingfoodcount):
            self.addFood(Food(startingpos=self.getRandomPos()))
        pass

    def addFood(self, food):
        self.foodlist.append(food)
        self.entityIDdict[food.uniqueID] = food

    def addGatherer(self, gatherer):
        self.gathererlist.append(gatherer)
        self.entityIDdict[gatherer.uniqueID] = gatherer

    # ! Implement
    def removeFood(self, idx):
        self.entityIDdict.pop(self.foodlist[idx].uniqueID)
        self.foodlist.pop(idx)

    # # ! Implement
    # def removeGatherer(self, gatherer):
    #     self.gathererlist.append(gatherer)
    #     self.gathererIddict = {gatherer.uniqueID:gatherer}


    def id2entity(self,id):
        return self.entityIDdict[id]

    def entity2id(self,entity):
        return entity.uniqueID

    def grant2Gatherer(self,gatherer):
        self.informfoodsvisible(gatherer)

    def informfoodsvisible(self,gatherer):
        newlist = []
        for food in self.foodlist:
            if checkInRange(gatherer.visionRange,gatherer.position,food.position):
                newlist.append(food)
        gatherer.informedfoodsvisible(newlist)


    def informgatherersknown(self, gatherer):
        gatherer.gatherersknown = []
        for gat in self.gathererlist:
            if gat!=gatherer:
                gatherer.gatherersknown.append(gat)

    def advanceGatherer(self,gatherer):
        func = self.gathererupdatedict[gatherer]
        if func is not None:
            func(gatherer)
        gatherer.update()

    def begin(self):
        # step = 0
        foodrespawncountdown = self.foodrespawntickperiod
        foodgrowing = True
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
                        if foodgrowing:
                            foodgrowing = False
                        else:
                            foodgrowing = True

            if self.updating:
                foodrespawncountdown = foodrespawncountdown - 1
                if foodrespawncountdown == 0:
                    foodrespawncountdown = self.foodrespawntickperiod
                    if foodgrowing:
                        self.addFood(Food(startingpos=self.getRandomPos()))
                # if step >= self.logictickperiod:
                #     self.updateEntitites()
                #     step = 0
                self.updateEntitites()
                self.updateSurface()

            self.clock.tick(self.tickrate)

    def initEntities(self):
        for gatherer in self.gathererlist:
            self.init4Gatherer(gatherer)

    def init4Gatherer(self,gatherer):
        self.informgatherersknown(gatherer)

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
        for idx, food in enumerate(self.foodlist):
            if not food.active and len(food.knownby)==0:
                self.removeFood(idx)

    def updateSurface(self):
        self.surface.update(self.gathererlist,self.foodlist)

    def getRandomPos(self):
        return [
            np.random.randint(0, self.surface.windowsize[0]),
            np.random.randint(0, self.surface.windowsize[1])
        ]
