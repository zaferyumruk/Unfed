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
        self._position = startingpos
        self._active = True
        Entity._uniqueID = Entity._uniqueID + 1
        self._uniqueID = Entity._uniqueID


class Food(Entity):
    def __init__(self, startingpos=[0.0, 0.0], foodtype=None):
        super().__init__(startingpos)
        self._assignfoodtype(foodtype)
        self._assignfoodatts()
        self._knownby = []

    def _assignfoodtype(self, foodtype):
        if foodtype is None:
            idx = np.random.choice(
                np.arange(0, len(list(Foodtype))), p=Rules.foodspawnchance)
            self._foodtype = list(Foodtype)[idx]
        else:
            self._foodtype = foodtype

    def _assignfoodatts(self):
        if self._foodtype == Foodtype.berry:
            self._amount = 7
            self._boost = []
        elif self._foodtype == Foodtype.apple:
            self._amount = 12
            self._boost = []
        elif self._foodtype == Foodtype.pineapple:
            self._amount = 10
            idx = np.random.choice(np.arange(0, len(list(Boost))))
            self._boost = []
        else:
            self._boost = []
            self._amount = 0


class Gatherer(Entity):
    def __init__(self,
                 name = 'unnamed',
                 fatigue=Rules.startingfatigue,
                 startingpos=[0.0, 0.0],
                 direction=[1.0, 1.0]):
        super().__init__(startingpos)

        #attributes
        self._name = name
        self._currenttask = None
        self._taskvariables = []
        self._score = 0
        self._backpack = Rules.startingbackpack
        self._visionRange = Rules.visionrange
        self._foodsvisible = []
        self._foodsknown = []
        self._gatherersknown = []
        #variables
        self._assigndirection(direction)
        self._speed = Rules.basespeed
        self._fatigue = fatigue
        self._state = State.idle
        self._boosts = []
        self._modifier = {
            'fatiguedrain': 1.0,
            'speed': 1.0,
            'eatspeed': 1.0,
            'stuntime': 1.0,
            'stunnedtime': 1.0,
            'attackcd':1.0
        }
        self._stunnedleft = 0 # counter
        self._attackcd = 0  # counter
        self._foodsknowncount = 0 #debug info

        self._task2func = {
            None: lambda: None,
            Task.follow: self._taskfollow,
            Task.attackmove: self._taskattackmove,
            Task.wander: self._taskwander,
            Task.cancel: self._taskcancel,
            Task.escape: self._taskescape,
            Task.collect: self._taskcollect
        }

    def _update(self):
        self._updateStunnedCd()
        self._updateAttackCd()
        self._consumeFood()
        self._checkFatigue()
        self._updateVision()
        if self._checkReadytoExecute():
            self._executeActiveTask()

    def _checkReadytoExecute(self):
        return (not self._state == State.beaten) and (not self._state == State.exhausted)

    def _checkFatigue(self):
        if self._fatigue == 0.0:
            self._state = State.exhausted

    def _deduce(self,value):
        value, _, state = self._reduceLimited(value, 1)
        return value,state

    def _updateStunnedCd(self):
        [self._stunnedleft,state] = self._deduce(self._stunnedleft)
        if state == ContainerState.empty:
            self._state = State.idle

    def _updateAttackCd(self):
        [self._attackcd, _ ] = self._deduce(self._attackcd)

    # * TASKS
    def _executeActiveTask(self):
        self._task2func[self._currenttask]()

    def _taskfollow(self, target=None):
        self._state = State.following
        if target is None:
            target = self._taskvariables[0]
        [distance,direction] = self._evalPosition(target)
        if distance > Rules.overlapdistance:
            self._assigndirection(direction)
            self._step()

    def _taskescape(self, target=None):
        self._state = State.fleeing
        if target is None:
            target = self._taskvariables[0]
        if target.active:
            [distance,direction] = self._evalPosition(target)
            self._assigndirection([-direc for direc in direction])
            self._step()
        else:
            self._taskcancel()

    def _taskattackmove(self):
        self._state = State.charging
        target = self._taskvariables[0]
        self._taskfollow(target)
        bashed = self._bash(target)
        if bashed:
            self._taskcancel()

    def _taskcancel(self):
        self._state = State.idle
        self._currenttask = None
        self._taskvariables = []

    def _taskwander(self):
        self._state = State.moving
        update_roll = np.random.randint(0, int(1.0 / Rules.chance2changedir))
        if not update_roll:
            self._assigndirection(list(np.random.rand(2) - 0.5))
        self._step()

    def _taskcollect(self):
        self._state = State.moving
        food = self._taskvariables[0]
        if food in self._foodsvisible:
            if not food._active:
                self._taskcancel()
                self._foodsvisible.remove(food)
                self._forgetFood(food)
                return
        self._taskfollow(food)
        collected = self._collectFood(food)
        if collected:
            self._taskcancel()

    def _informedfoodsvisible(self,foodlist):
        self._foodsvisible = foodlist
        for food in foodlist:
            foodknown = food in self._foodsknown
            if not food._active:
                self._foodsvisible.remove(food)
                if foodknown:
                    self._forgetFood(food)
            elif not foodknown:
                self._noticeFood(food)
        self._foodsknowncount = len(self._foodsknown)

    def _forgetFood(self, food):
        self._foodsknown.remove(food)
        food._knownby.remove(self)
        self._foodsknowncount = len(self._foodsknown)

    def _noticeFood(self, food):
        self._foodsknown.append(food)
        food._knownby.append(self)
        self._foodsknowncount = len(self._foodsknown)

    def assignTask(self,task,args=None):
        self._currenttask = task
        if args is not list:
            args = [args]
        self._taskvariables = args


    # * BASIC ACTIONS
    def _collectFood(self,food):
        success = False
        if  self._checkReach(food):
            success = self._storeFood(food._amount)
            if success:
                food._active = False
                self._forgetFood(food)
        return success

    def _bash(self,other):
        success = False
        if  self._checkReach(other) and self._attackcd <= 0.0:
            _ = self._reducefatigue(Rules.Fatiguedrain.attack)
            _ = other._reducefatigue(Rules.Fatiguedrain.beaten)

            other._state = State.beaten
            self._state = State.idle

            self._attackcd = Rules.attackcd * self._modifier['attackcd']
            other._stunnedleft = Rules.bashstunspan * self._modifier[
                'stuntime'] * other._modifier['stunnedtime']

            self._storeFood(other._backpack)
            other._backpack = 0.0

            success = True
        return success

    def _checkReach(self,other):
        [distance,direction]=self._evalPosition(other)
        return distance<Rules.reachdistance

    # * UPDATES
    def _consumeFood(self):
        tobeconsumed = Rules.eatspeed * self._modifier['eatspeed']
        [self._backpack, ratioeaten, _] = self._reduceLimited(self._backpack, tobeconsumed)
        self._score = self._score + tobeconsumed * ratioeaten * Rules.scoremultiplier

    def _reflectBoostEffects(self):
        self._speed = Rules.basespeed * self._modifier['speed']

    # reveal foods within a vicinity, at no cost
    # ! Please call after collect food or maybe after everything else
    def _updateVision(self):
        pass

    # * USEFUL BASIC FUNCTIONS
    def _reducefatigue(self, fatigueloss):
        [self._fatigue, ratioextracted, state] = self._reduceLimited(
            self._fatigue, fatigueloss)
        if state == ContainerState.empty:
            self._state = State.exhausted
        return ratioextracted

    def _storeFood(self, foodamount):
        success = False
        if self._backpack < Rules.backpackcap:
            success = True
            if (self._backpack + foodamount) > Rules.backpackcap:
                self._backpack = Rules.backpackcap
            else:
                self._backpack = self._backpack + foodamount
        return success

    # ! direction manipulation at boundaries are problematic
    def _step(self):
        '''uses speed and current direction'''
        fatigueloss = self._speed * Rules.Fatiguedrain.move * self._modifier['fatiguedrain']
        if self._state != State.exhausted or self._state != State.beaten:
            remains = self._reducefatigue(fatigueloss)
            for idx in range(len(self._position)):
                stepsize = self._direction[idx] * self._speed * remains
                temp_pos = self._position[idx] + stepsize
                if not self._checkBoundary(temp_pos, Rules.Map.bounds[idx]):
                    self._direction[idx] = -self._direction[idx]
                    stepsize = self._direction[idx] * self._speed * remains
                    temp_pos = self._position[idx] + stepsize
                self._assigndirection(self._direction)
                self._position[idx] = temp_pos

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
            direction = np.subtract(arg, self._position)
        else:
            direction = np.subtract(arg._position, self._position)
        distance = np.linalg.norm(direction)
        return (distance,direction)

    def _assigndirection(self, direction):
        self._direction = unitvec(direction)

    def _checkBoundary(self,pos,bounds):
        if pos>bounds[1] or pos<bounds[0]:
            return False
        return True

    def getdistance(self,entity):
        direction = np.subtract(entity._position,self._position)
        distance = np.linalg.norm(direction)
        return distance

    def closestgatherer(self):
        return self.closestentity(self._gatherersknown)

    def closestfood(self,foodtype=None):
        return self.closestentity(self._listfoods(self._foodsknown,foodtype))

    def _listfoods(self, foodlist, foodtype=None):
        if foodtype is None:
            return foodlist
        else:
            filteredlist = [
                food for food in foodlist if food._foodtype == foodtype
            ]
            return filteredlist

    def visiblefoods(self,foodtype=None):
        return self._sortedlist2dictlist(self._sortwrtdistance(self._listfoods(self._foodsvisible,foodtype)),'Food')

    def knownfoods(self,foodtype=None):
        return self._sortedlist2dictlist(self._sortwrtdistance(self._listfoods(self._foodsknown, foodtype)),'Food')

    def knowngatherers(self):
        return self._sortedlist2dictlist(self._sortwrtdistance(self._gatherersknown),'Gatherer')

    def _sortwrtdistance(self,flist):
        if len(flist)>0:
            flist = flist
            dlist = np.sqrt(self._entitydistance_2(flist))
            df = sorted(zip(flist,dlist),key = lambda t: t[1])
            return df
        else:
            return []

    def _sortedlist2dictlist(self,flist,firstkey):
        return [{firstkey: tup[0], 'distance': tup[1]} for tup in flist]

    def foodcarried(self,gatherer):
        ratiofull = gatherer._backpack / Rules.backpackcap
        if ratiofull<=0.25:
            return 0
        elif ratiofull<=0.5:
            return 1
        elif ratiofull<=0.75:
            return 2
        elif ratiofull <= 1:
            return 3

    # def checkbackpack(self):
    #     return self._backpack

    def checkstate(self,gatherer):
        return gatherer._state

    def closestentity(self,entitylist):
        if len(entitylist)>0:
            return entitylist[np.argmin(self._entitydistance_2(entitylist))]
        else:
            return None

    def _entitydistance_2(self,entitylist):
        entitypos = [entity._position for entity in entitylist]
        nodes = np.asarray(entitypos)
        node = self._position
        dist_2 = np.sum((nodes - node)**2, axis=1)
        return dist_2