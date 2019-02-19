import numpy as np
from enum import Enum

from rules import Rules
from common import unitvec

class ContainerState(Enum):
    empty = 1
    nonempty = 2

class Task(Enum):
    cancel = 1
    follow = 2
    wander = 3
    attackmove = 4
    escape = 5
    collect = 6

class State(Enum):
    idle = 1
    following = 2
    moving = 3
    charging = 4
    fleeing = 5
    lookingaround = 6
    collecting = 7
    beaten = 8
    exhausted = 9

class Boost(Enum):
    hotfeet = 1
    devourer = 2
    weeble = 3
    strongarm = 4
    ironlungs = 5

class Foodtype(Enum):
    berry = 1
    apple = 2
    pineapple = 3

class Entity():
    _uniqueID = 0
    def __init__(self, startingpos):
        self.position = startingpos
        self.active = True
        Entity._uniqueID = Entity._uniqueID + 1
        self.uniqueID = Entity._uniqueID


class Food(Entity):
    def __init__(self, startingpos=[0.0, 0.0], foodtype=None):
        super().__init__(startingpos)
        self.assignfoodtype(foodtype)
        self.assignfoodatts()
        self.knownby = []

    def assignfoodtype(self, foodtype):
        if foodtype is None:
            idx = np.random.choice(
                np.arange(0, len(list(Foodtype))), p=Rules.foodspawnchance)
            self.foodtype = list(Foodtype)[idx]
        else:
            self.foodtype = foodtype

    def assignfoodatts(self):
        if self.foodtype == Foodtype.berry:
            self.amount = 7
            self.boost = []
        elif self.foodtype == Foodtype.apple:
            self.amount = 12
            self.boost = []
        elif self.foodtype == Foodtype.pineapple:
            self.amount = 10
            idx = np.random.choice(np.arange(0, len(list(Boost))))
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
        self.foodsvisible = []
        self.foodsknown = []
        self.gatherersknown = []
        #variables
        self._assigndirection(direction)
        self.speed = Rules.basespeed
        self.fatigue = fatigue
        self.state = State.idle
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
        self.foodsknowncount = 0 #debug info

        self.task2func = {
            None: lambda: None,
            Task.follow: self._taskfollow,
            Task.attackmove: self._taskattackmove,
            Task.wander: self._taskwander,
            Task.cancel: self._taskcancel,
            Task.escape: self._taskescape,
            Task.collect: self._taskcollect
        }

    def update(self):
        self._updateStunnedCd()
        self._updateAttackCd()
        self._consumeFood()
        self._checkFatigue()
        self._updateVision()
        if self._checkReadytoExecute():
            self._executeActiveTask()

    def _checkReadytoExecute(self):
        return (not self.state == State.beaten) and (not self.state == State.exhausted)

    def _checkFatigue(self):
        if self.fatigue == 0.0:
            self.state = State.exhausted

    def _deduce(self,value):
        value, _, state = self._reduceLimited(value, 1)
        return value,state

    def _updateStunnedCd(self):
        [self.stunnedleft,state] = self._deduce(self.stunnedleft)
        if state == ContainerState.empty:
            self.state = State.idle

    def _updateAttackCd(self):
        [self.attackcd, _ ] = self._deduce(self.attackcd)

    # * TASKS
    def _executeActiveTask(self):
        self.task2func[self.currenttask]()

    def _taskfollow(self, target=None):
        self.state = State.following
        if target is None:
            target = self.taskvariables[0]
        [distance,direction] = self._evalPosition(target)
        if distance > Rules.overlapdistance:
            self._assigndirection(direction)
            self._step()

    def _taskescape(self, target=None):
        self.state = State.fleeing
        if target is None:
            target = self.taskvariables[0]
        if target.active:
            [distance,direction] = self._evalPosition(target)
            self._assigndirection([-direc for direc in direction])
            self._step()
        else:
            self._taskcancel()

    def _taskattackmove(self):
        self.state = State.charging
        target = self.taskvariables[0]
        self._taskfollow(target)
        bashed = self._bash(target)
        if bashed:
            self._taskcancel()

    def _taskcancel(self):
        self.state = State.idle
        self.currenttask = None
        self.taskvariables = []

    def _taskwander(self):
        self.state = State.moving
        update_roll = np.random.randint(0, int(1.0 / Rules.chance2changedir))
        if not update_roll:
            self._assigndirection(list(np.random.rand(2) - 0.5))
        self._step()

    def _taskcollect(self):
        self.state = State.moving
        food = self.taskvariables[0]
        if food in self.foodsvisible:
            if not food.active:
                self._taskcancel()
                self.foodsvisible.remove(food)
                self._forgetFood(food)
                return
        self._taskfollow(food)
        collected = self._collectFood(food)
        if collected:
            self._forgetFood(food)
            self._taskcancel()

    def informedfoodsvisible(self,foodlist):
        self.foodsvisible = foodlist
        for food in foodlist:
            foodknown = food in self.foodsknown
            if not food.active:
                self.foodsvisible.remove(food)
                if foodknown:
                    self._forgetFood(food)
            elif not foodknown:
                self._noticeFood(food)
        self.foodsknowncount = len(self.foodsknown)

    def _forgetFood(self, food):
        self.foodsknown.remove(food)
        food.knownby.remove(self)
        self.foodsknowncount = len(self.foodsknown)

    def _noticeFood(self, food):
        self.foodsknown.append(food)
        food.knownby.append(self)
        self.foodsknowncount = len(self.foodsknown)

    def assignTask(self,task,args=None):
        self.currenttask = task
        if args is not list:
            args = [args]
        self.taskvariables = args


    # * BASIC ACTIONS
    def _collectFood(self,food):
        success = False
        if  self._checkReach(food):
            success = self._addFood(food.amount)
            if success:
                food.active = False
            self.state = State.idle
        return success

    def _bash(self,other):
        success = False
        if  self._checkReach(other) and self.attackcd <= 0.0:
            _ = self._reducefatigue(Rules.Fatiguedrain.attack)
            _ = other._reducefatigue(Rules.Fatiguedrain.beaten)

            other.state = State.beaten
            self.state = State.idle

            self.attackcd = Rules.attackcd * self.modifier['attackcd']
            other.stunnedleft = Rules.bashstunspan * self.modifier['stuntime'] * other.modifier['stunnedtime']

            other.backpack = 0.0
            self._addFood(other.backpack)

            success = True
        return success

    def _checkReach(self,other):
        [distance,direction]=self._evalPosition(other)
        return distance<Rules.reachdistance

    # * UPDATES
    def _consumeFood(self):
        tobeconsumed = Rules.eatspeed * self.modifier['eatspeed']
        [self.backpack, ratioeaten, _] = self._reduceLimited(self.backpack, tobeconsumed)
        self.score = self.score + tobeconsumed * ratioeaten * Rules.scoremultiplier

    def _reflectBoostEffects(self):
        self.speed = Rules.basespeed * self.modifier['speed']

    # reveal foods within a vicinity, at no cost
    # ! Please call after collect food or maybe after everything else
    def _updateVision(self):
        pass

    # * USEFUL BASIC FUNCTIONS
    def _reducefatigue(self, fatigueloss):
        [self.fatigue, ratioextracted, state] = self._reduceLimited(
            self.fatigue, fatigueloss)
        if state == ContainerState.empty:
            self.state = State.exhausted
        return ratioextracted

    def _addFood(self, foodamount):
        success = False
        if self.backpack < Rules.backpackcap:
            success = True
            if (self.backpack + foodamount) > Rules.backpackcap:
                self.backpack = Rules.backpackcap
            else:
                self.backpack = self.backpack + foodamount
        return success

    # ! direction manipulation at boundaries are problematic
    def _step(self):
        '''uses speed and current direction'''
        fatigueloss = self.speed * Rules.Fatiguedrain.move * self.modifier['fatiguedrain']
        if self.state != State.exhausted or self.state != State.beaten:
            remains = self._reducefatigue(fatigueloss)
            for idx in range(len(self.position)):
                stepsize = self.direction[idx] * self.speed * remains
                temp_pos = self.position[idx] + stepsize
                if not self._checkBoundary(temp_pos, Rules.Map.bounds[idx]):
                    self.direction[idx] = -self.direction[idx]
                    stepsize = self.direction[idx] * self.speed * remains
                    temp_pos = self.position[idx] + stepsize
                self._assigndirection(self.direction)
                self.position[idx] = temp_pos

    def _reduceLimited(self, holdervariable, tobeextracted):
        '''holdervariable, ratioextracted, state = self.reduceLimited(holdervariable, tobeextracted)'''
        ratioextracted = 0.0
        state = ContainerState.empty
        if holdervariable != 0.0:
            if holdervariable <= tobeextracted:
                ratioextracted = holdervariable / tobeextracted
                holdervariable = 0.0
            else:
                holdervariable = holdervariable - tobeextracted
                state = ContainerState.nonempty
                ratioextracted = 1.0
        return holdervariable, ratioextracted, state

    def _face(self,arg):
        [_,direction] = self._evalPosition(arg)
        self._assigndirection(direction)

    def _evalPosition(self,arg):
        '''(distance,direction) = evalPosition(self,arg)
        arg: coords (as list) or entity'''
        if type(arg) is list:
            direction = np.subtract(arg, self.position)
        else:
            direction = np.subtract(arg.position, self.position)
        distance = np.linalg.norm(direction)
        return (distance,direction)

    def _assigndirection(self, direction):
        self.direction = unitvec(direction)

    def _checkBoundary(self,pos,bounds):
        if pos>bounds[1] or pos<bounds[0]:
            return False
        return True

    def getdistance(self,entity):
        direction = np.subtract(entity.position,self.position)
        distance = np.linalg.norm(direction)
        return distance

    def closestgatherer(self):
        return self.closestentity(self.gatherersknown)

    def closestfood(self,foodtype=None):
        return self.closestentity(self._listfoods(self.foodsknown,foodtype))

    def _listfoods(self, foodlist, foodtype=None):
        if foodtype is None:
            return foodlist
        else:
            filteredlist = [
                food for food in foodlist if food.foodtype == foodtype
            ]
            return filteredlist

    def visiblefoods(self,foodtype=None):
        return self._sortedlist2dictlist(self._sortwrtdistance(self._listfoods(self.foodsvisible,foodtype)),'Food')

    def knownfoods(self,foodtype=None):
        return self._sortedlist2dictlist(self._sortwrtdistance(self._listfoods(self.foodsknown, foodtype)),'Food')

    def knowngatherers(self):
        return self._sortedlist2dictlist(self._sortwrtdistance(self.gatherersknown),'Gatherer')

    def _sortwrtdistance(self,flist):
        if len(flist)>0:
            flist = flist
            dlist = np.sqrt(self.entitydistance_2(flist))
            df = sorted(zip(flist,dlist),key = lambda t: t[1])
            return df
        else:
            return []

    def _sortedlist2dictlist(self,flist,firstkey):
        return [{firstkey: tup[0], 'distance': tup[1]} for tup in flist]

    def foodcarried(self,gatherer):
        ratiofull = gatherer.backpack / Rules.backpackcap
        if ratiofull<=0.25:
            return 0
        elif ratiofull<=0.5:
            return 1
        elif ratiofull<=0.75:
            return 2
        elif ratiofull <= 1:
            return 3

    # def checkbackpack(self):
    #     return self.backpack

    def checkstate(self,gatherer):
        return gatherer.state

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