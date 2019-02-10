import numpy as np
from enum import Enum

# ! check this
def normalize(alist):
    norm = np.linalg.norm(alist)
    if norm == 0.0:
        return [0.0] * len(alist)
    return [val / norm for val in alist]


class containerStates(Enum):
    empty = 1
    nonempty = 2


class states(Enum):
    idle = 1
    lookingaround = 2
    moving = 3
    following = 4
    collecting = 5
    attacking = 6
    beaten = 7
    exhausted = 8

class boosts(Enum):
    hotfeet = 1
    devourer = 2
    weeble = 3
    strongarm = 4
    ironlungs = 5


class rules():
    tickrate = 60
    basespeed = 75 / tickrate #rate, pixels
    startingfatigue = 100 #value
    eatspeed = 1.0 / tickrate #rate
    foodspawnchance = normalize([50, 10, 2]) #value
    bashstunspan = 2 * tickrate #timespan
    scoremultiplier = 10 #value
    attackcd = 1 * tickrate #timespan
    backpackcap = 5  #value
    class fatiguedrain():
        move = 0.1  # per pixel
        collect = 1 #per action
        attack = 4  #per action
        beaten = 2  #per action
        lookaround = 3  #per action
    class foodtype(Enum):
        berry = 1
        apple = 2
        pineapple = 3


class mahluk():
    def __init__(self, startingpos):
        self.position = startingpos


class food(mahluk):
    def __init__(self, startingpos=[0.0, 0.0], foodtype=None):
        super().__init__(startingpos)
        self.assignfoodtype(foodtype)
        self.assignfoodatts()
        self.collected = False

    def assignfoodtype(self, foodtype):
        if foodtype is None:
            idx = np.random.choice(
                np.arange(0, len(list(rules.foodtype))), p=rules.foodspawnchance)
            self.foodtype = list(rules.foodtype)[idx]
        else:
            self.foodtype = foodtype

    def assignfoodatts(self):
        if self.foodtype == rules.foodtype.berry:
            self.amount = 1
            self.boost = None
        elif self.foodtype == rules.foodtype.apple:
            self.amount = 2
            self.boost = None
        elif self.foodtype == rules.foodtype.pineapple:
            self.amount = 1
            idx = np.random.choice(np.arange(0, len(list(boosts))))
            self.boost = boosts[idx]
        else:
            self.boost = None
            self.amount = 0


class gatherer(mahluk):
    def __init__(self,
                 name = 'unnamed',
                 fatigue=rules.startingfatigue,
                 startingpos=[0.0, 0.0],
                 direction=[1.0, 1.0]):
        super().__init__(startingpos)

        #attributes
        self.name = name
        #variables
        self.assingdirection(direction)
        self.speed = rules.basespeed
        self.fatigue = fatigue
        self.state = states.idle
        self.backpack = 0
        self.boosts = []
        self.modifier = {
            'fatiguedrain': 1.0,
            'speed': 1.0,
            'eatspeed': 1.0,
            'stuntime': 1.0,
            'stunnedtime': 1.0,
            'attackcd':1.0
        }
        self.stunnedleft = 0
        self.attackcd = 0
        self.currentcommand = None
        self.currentvariables = []
        self.score = 0

    def update(self):
        # self.checkStateBeaten()
        # self.reflectBoostEffects()
        self.consumeFood()
        self.step()
        # self.updateVision()

    def checkStateBeaten(self):
        if self.stunnedleft > 0:
            self.stunnedleft = self.stunnedleft - 1
            if self.stunnedleft <= 0:
                self.states = states.idle

    # * BASIC ACTIONS
    # if food is collected beforehand in same step collectFood fails, next step update vision solves the disappearing food problem
    def collectFood(self,food):
        success = False
        if food.collected is False:
            success = self.addFood(food.amount)
            if success:
                food.collected = True
        self.state = states.idle
        return success

    def bash(self,gatherer):
        success = False
        if self.attackcd <= 0.0:
            _ = self.reducefatigue(rules.fatiguedrain.attack)
            _ = gatherer.reducefatigue(rules.fatiguedrain.beaten)
            gatherer.stunnedleft = rules.bashstunspan * self.modifier['stuntime'] * gatherer.modifier['stunnedtime']
            gatherer.state = states.beaten
            self.attackcd = rules.attackcd * self.modifier['attackcd']
            self.addFood(gatherer.backpack)
            gatherer.backpack = 0.0
            success = True
        return success

    # reveal foods in whole map
    def lookaround(self):
        return None

    # * UPDATES
    def consumeFood(self):
        tobeconsumed = rules.eatspeed * self.modifier['eatspeed']
        [self.backpack, ratioeaten, _] = self.reduceLimited(self.backpack, tobeconsumed)
        self.score = self.score + tobeconsumed * ratioeaten * rules.scoremultiplier

    def reflectBoostEffects(self):
        self.speed = rules.basespeed * self.modifier['speed']

    # reveal foods within a vicinity, at no cost
    # ! Please call after collect food or maybe after everything else
    def updateVision(self):
        return None


    # * USEFUL BASIC FUNCTIONS
    def reducefatigue(self, fatigueloss):
        [self.fatigue, ratioextracted, state] = self.reduceLimited(
            self.fatigue, fatigueloss)
        if state == containerStates.empty:
            self.state = states.exhausted
        return ratioextracted

    def addFood(self, foodamount):
        success = False
        if self.backpack < rules.backpackcap:
            success = True
            if (self.backpack + foodamount) > rules.backpackcap:
                self.backpack = rules.backpackcap
            else:
                self.backpack = self.backpack + foodamount
        return success

    # uses speed and current direction
    # ! PLEASE HANDLE (0,0) direction
    def step(self):
        fatigueloss = self.speed * rules.fatiguedrain.move * self.modifier['fatiguedrain']
        if self.state != states.exhausted:
            remains = self.reducefatigue(fatigueloss)
            self.position[0] = self.position[
                0] + self.direction[0] * self.speed * remains
            self.position[1] = self.position[
                1] + self.direction[1] * self.speed * remains

    def reduceLimited(self, holdervariable, tobeextracted):
        ratioextracted = 0.0
        state = containerStates.empty
        if holdervariable != 0.0:
            if holdervariable <= tobeextracted:
                ratioextracted = holdervariable / tobeextracted
                holdervariable = 0.0
            else:
                holdervariable = holdervariable - tobeextracted
                state = containerStates.nonempty
                ratioextracted = 1.0
        return holdervariable, ratioextracted, state

    def mathStuff(self):
        return None

    def assingdirection(self, direction):
        self.direction = normalize(direction)
