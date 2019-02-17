import numpy as np
from enum import Enum

from rules import Rules
from common import unitvec

class ContainerStates(Enum):
    empty = 1
    nonempty = 2

class Tasks(Enum):
    cancel = 1
    follow = 2
    wander = 3
    attackmove = 4
    escape = 5
    collect = 6

class States(Enum):
    idle = 1
    following = 2
    moving = 3
    charging = 4
    fleeing = 5
    lookingaround = 6
    collecting = 7
    beaten = 8
    exhausted = 9

class Boosts(Enum):
    hotfeet = 1
    devourer = 2
    weeble = 3
    strongarm = 4
    ironlungs = 5

class Foodtypes(Enum):
    berry = 1
    apple = 2
    pineapple = 3

class Entity():
    entityuniqueID = 0
    def __init__(self, startingpos):
        self.position = startingpos
        self.active = True
        Entity.entityuniqueID = Entity.entityuniqueID + 1
        self.entityuniqueID = Entity.entityuniqueID


class Food(Entity):
    def __init__(self, startingpos=[0.0, 0.0], foodtype=None):
        super().__init__(startingpos)
        self.assignfoodtype(foodtype)
        self.assignfoodatts()

    def assignfoodtype(self, foodtype):
        if foodtype is None:
            idx = np.random.choice(
                np.arange(0, len(list(Foodtypes))), p=Rules.foodspawnchance)
            self.foodtype = list(Foodtypes)[idx]
        else:
            self.foodtype = foodtype

    def assignfoodatts(self):
        if self.foodtype == Foodtypes.berry:
            self.amount = 7
            self.boost = []
        elif self.foodtype == Foodtypes.apple:
            self.amount = 12
            self.boost = []
        elif self.foodtype == Foodtypes.pineapple:
            self.amount = 10
            idx = np.random.choice(np.arange(0, len(list(Boosts))))
            self.boost = []
        else:
            self.boost = []
            self.amount = 0


class Gatherer(Entity):
    def __init__(self,
                 name = 'unnamed',
                 fatigue=Rules.startingfatigue,
                 startingpos=[0.0, 0.0],
                 direction=[1.0, 1.0]):
        super().__init__(startingpos)

        #attributes
        self.name = name
        self.currenttask = None
        self.taskvariables = []
        self.score = 0
        self.backpack = 5
        self.visionRange = Rules.visionrange
        self.foodsaround = []
        self.gatherersaround = []
        #variables
        self.assigndirection(direction)
        self.speed = Rules.basespeed
        self.fatigue = fatigue
        self.state = States.idle
        self.boosts = []
        self.modifier = {
            'fatiguedrain': 1.0,
            'speed': 1.0,
            'eatspeed': 1.0,
            'stuntime': 1.0,
            'stunnedtime': 1.0,
            'attackcd':1.0
        }
        self.stunnedleft = 0 # counter
        self.attackcd = 0  # counter
        self.foodsaroundcount = 0 #debug info

        self.task2func = {
            None: lambda: None,
            Tasks.follow: self.taskfollow,
            Tasks.attackmove: self.taskattackmove,
            Tasks.wander: self.taskwander,
            Tasks.cancel: self.taskcancel,
            Tasks.escape: self.taskescape,
            Tasks.collect: self.taskcollect
        }

    def update(self):
        self.updateStunnedCd()
        self.updateAttackCd()
        self.consumeFood()
        self.checkFatigue()
        self.updateVision()
        if self.checkReadytoExecute():
            self.executeActiveTask()

    def checkReadytoExecute(self):
        return (not self.state == States.beaten) and (not self.state == States.exhausted)

    def checkFatigue(self):
        if self.fatigue == 0.0:
            self.state = States.exhausted

    def deduce(self,value):
        value, _, state = self.reduceLimited(value, 1)
        return value,state

    def updateStunnedCd(self):
        [self.stunnedleft,state] = self.deduce(self.stunnedleft)
        if state == ContainerStates.empty:
            self.state = States.idle

    def updateAttackCd(self):
        [self.attackcd, _ ] = self.deduce(self.attackcd)

    # * TASKS
    def executeActiveTask(self):
        self.task2func[self.currenttask]()

    def taskfollow(self, target=None):
        self.state = States.following
        if target is None:
            target = self.taskvariables[0]
        if target.active:
            [distance,direction] = self.evalPosition(target)
            if distance > Rules.overlapdistance:
                self.assigndirection(direction)
                self.step()
        else:
            self.taskcancel()

    def taskescape(self, target=None):
        self.state = States.fleeing
        if target is None:
            target = self.taskvariables[0]
        if target.active:
            [distance,direction] = self.evalPosition(target)
            self.assigndirection([-direc for direc in direction])
            self.step()
        else:
            self.taskcancel()

    def taskattackmove(self):
        self.state = States.charging
        target = self.taskvariables[0]
        self.taskfollow(target)
        bashed = self.bash(target)
        if bashed:
            self.taskcancel()

    def taskcancel(self):
        self.state = States.idle
        self.currenttask = None
        self.taskvariables = []

    def taskwander(self):
        self.state = States.moving
        update_roll = np.random.randint(0, int(1.0 / Rules.chance2changedir))
        if not update_roll:
            self.assigndirection(list(np.random.rand(2) - 0.5))
        self.step()

    def taskcollect(self):
        self.state = States.moving
        food = self.taskvariables[0]
        if food in self.foodsaround:
            if not food.active:
                self.taskcancel()
                self.foodsaround.remove(food)
                self.foodsaroundcount = len(self.foodsaround)
                return
        self.taskfollow(food)
        collected = self.collectFood(food)
        if collected:
            self.taskcancel()

    def informedfoodsaround(self,foodlist):
        for food in foodlist:
            foodknown = food in self.foodsaround
            if not food.active:
                if foodknown:
                    self.foodsaround.remove(food)
            elif not foodknown:
                self.foodsaround.append(food)
        self.foodsaroundcount = len(self.foodsaround)

    def assignTask(self,task,args=None):
        self.currenttask = task
        if args is not list:
            args = [args]
        self.taskvariables = args


    # * BASIC ACTIONS
    def collectFood(self,food):
        success = False
        if  self.checkReach(food):
            success = self.addFood(food.amount)
            if success:
                food.active = False
            self.state = States.idle
        return success

    def bash(self,other):
        success = False
        if  self.checkReach(other) and self.attackcd <= 0.0:
            _ = self.reducefatigue(Rules.Fatiguedrain.attack)
            _ = other.reducefatigue(Rules.Fatiguedrain.beaten)

            other.state = States.beaten
            self.state = States.idle

            self.attackcd = Rules.attackcd * self.modifier['attackcd']
            other.stunnedleft = Rules.bashstunspan * self.modifier['stuntime'] * other.modifier['stunnedtime']

            other.backpack = 0.0
            self.addFood(other.backpack)

            success = True
        return success

    def checkReach(self,other):
        [distance,direction]=self.evalPosition(other)
        return distance<Rules.reachdistance

    # * UPDATES
    def consumeFood(self):
        tobeconsumed = Rules.eatspeed * self.modifier['eatspeed']
        [self.backpack, ratioeaten, _] = self.reduceLimited(self.backpack, tobeconsumed)
        self.score = self.score + tobeconsumed * ratioeaten * Rules.scoremultiplier

    def reflectBoostEffects(self):
        self.speed = Rules.basespeed * self.modifier['speed']

    # reveal foods within a vicinity, at no cost
    # ! Please call after collect food or maybe after everything else
    def updateVision(self):
        pass

    # * USEFUL BASIC FUNCTIONS
    def reducefatigue(self, fatigueloss):
        [self.fatigue, ratioextracted, state] = self.reduceLimited(
            self.fatigue, fatigueloss)
        if state == ContainerStates.empty:
            self.state = States.exhausted
        return ratioextracted

    def addFood(self, foodamount):
        success = False
        if self.backpack < Rules.backpackcap:
            success = True
            if (self.backpack + foodamount) > Rules.backpackcap:
                self.backpack = Rules.backpackcap
            else:
                self.backpack = self.backpack + foodamount
        return success

    # ! direction manipulation at boundaries are problematic
    def step(self):
        '''uses speed and current direction'''
        fatigueloss = self.speed * Rules.Fatiguedrain.move * self.modifier['fatiguedrain']
        if self.state != States.exhausted or self.state != States.beaten:
            remains = self.reducefatigue(fatigueloss)
            for idx in range(len(self.position)):
                stepsize = self.direction[idx] * self.speed * remains
                temp_pos = self.position[idx] + stepsize
                if not self.checkBoundary(temp_pos, Rules.Map.bounds[idx]):
                    self.direction[idx] = -self.direction[idx]
                    stepsize = self.direction[idx] * self.speed * remains
                    temp_pos = self.position[idx] + stepsize
                self.assigndirection(self.direction)
                self.position[idx] = temp_pos

    def reduceLimited(self, holdervariable, tobeextracted):
        '''holdervariable, ratioextracted, state = self.reduceLimited(holdervariable, tobeextracted)'''
        ratioextracted = 0.0
        state = ContainerStates.empty
        if holdervariable != 0.0:
            if holdervariable <= tobeextracted:
                ratioextracted = holdervariable / tobeextracted
                holdervariable = 0.0
            else:
                holdervariable = holdervariable - tobeextracted
                state = ContainerStates.nonempty
                ratioextracted = 1.0
        return holdervariable, ratioextracted, state

    def face(self,arg):
        [_,direction] = self.evalPosition(arg)
        self.assigndirection(direction)

    def evalPosition(self,arg):
        '''(distance,direction) = evalPosition(self,arg)
        arg: coords (as list) or entity'''
        if type(arg) is list:
            direction = np.subtract(arg, self.position)
        else:
            direction = np.subtract(arg.position, self.position)
        distance = np.linalg.norm(direction)
        return (distance,direction)

    def assigndirection(self, direction):
        self.direction = unitvec(direction)

    def checkBoundary(self,pos,bounds):
        if pos>bounds[1] or pos<bounds[0]:
            return False
        return True

    def getdistance(self,entity):
        direction = np.subtract(entity.position,self.position)
        distance = np.linalg.norm(direction)
        return distance


    def closestgatherer(self):
        return self.closestentity(self.gatherersaround)

    def closestfood(self,foodtype=None):
        return self.closestentity(self._listfoodsaround(foodtype))

    def _listfoodsaround(self,foodtype=None):
        if foodtype is None:
            return self.foodsaround
        else:
            filteredlist = [
                food for food in self.foodsaround if food.foodtype == foodtype
            ]
            return filteredlist

    def listfoodsaround(self,foodtype=None):
        return self.sortwrtdistance(self._listfoodsaround(foodtype))

    def listgatherersaround(self):
        return self.sortwrtdistance(self.gatherersaround)

    def sortwrtdistance(self,flist):
        flist = flist
        dlist = np.sqrt(self.entitydistance_2(flist))
        df = sorted(zip(flist,dlist),key = lambda t: t[1])
        return df

    def iscarryingfood(self,gatherer):
        return gatherer.backpack > 0.0

    # def checkbackpack(self):
    #     return self.backpack

    # def checkstate(self):
    #     return self.state

    def closestentity(self,entitylist):
        if len(entitylist)>0:
            return entitylist[np.argmin(self.entitydistance_2(entitylist))]
        else:
            return None

    def entitydistance_2(self,entitylist):
        entitypos = [entity.position for entity in entitylist]
        nodes = np.asarray(entitypos)
        node = self.position
        dist_2 = np.sum((nodes - node)**2, axis=1)
        return dist_2