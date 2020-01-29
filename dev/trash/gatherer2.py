import numpy as np
from enum import Enum

# ! check this
def unitvec(alist):
    norm = np.linalg.norm(alist)
    if norm == 0.0:
        return [0.0] * len(alist)
    return [val / norm for val in alist]

def maxnorm(alist):
    max_entry = sum(alist)
    return [val / max_entry for val in alist]

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


class Rules():
    tickrate = 60
    basespeed = 75.0 / tickrate #rate, pixels
    startingfatigue = 100.0 #value
    eatspeed = 1.0 / tickrate #rate
    foodspawnchance = maxnorm([50, 10, 2]) #value
    bashstunspan = 2.0 * tickrate #timespan
    scoremultiplier = 10 #value
    attackcd = 1.0 * tickrate #timespan
    backpackcap = 5.0  #value
    reachdistance = 20.0
    overlapdistance = 5.0
    chance2changedir = 0.02 # utilized in taskwander
    visionrange = 40
    class Fatiguedrain():
        move = 0.1  # per pixel
        collect = 1 #per action
        attack = 3  #per action
        beaten = 2  #per action
        lookaround = 3  #per action
    class Map():
        size = [800,600]
        bounds = [[0, 800],[0, 600]]
        center = [int(entry / 2) for entry in size]



class Entity():
    def __init__(self, startingpos):
        self.position = startingpos
        self.active = True


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
            self.amount = 1
            self.boost = []
        elif self.foodtype == Foodtypes.apple:
            self.amount = 2
            self.boost = []
        elif self.foodtype == Foodtypes.pineapple:
            self.amount = 1
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
        update_roll = np.random.randint(0, 1 / Rules.chance2changedir)
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
                return
        self.taskfollow(food)
        collected = self.collectFood(food)
        if collected:
            self.taskcancel()

    def informedfoodsaround(self,food):
        if food not in self.foodsaround:
            self.foodsaround.append(food)

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

    def mathStuff(self):
        return None

    def face(self,arg):
        [_,direction] = self.evalPosition(arg)
        self.assigndirection(direction)

    def evalPosition(self,arg):
        '''(distance,direction) = evalPosition(self,arg)
        arg: coords (as list) or entity'''
        posself = self.position

        if type(arg) is list:
            postarget = arg
        else:
            postarget = arg.position

        direction = [postarget[idx] - posself[idx] for idx in range(len(posself))]
        distance = 0
        for direc in direction:
            distance = distance + direc**2
        distance = np.sqrt(distance)
        return (distance,direction)

    def assigndirection(self, direction):
        self.direction = unitvec(direction)

    def checkBoundary(self,pos,bounds):
        if pos>bounds[1] or pos<bounds[0]:
            return False
        return True

def checkInRange(self, r, center, pos):
    xdiff = center[0] - pos[0]
    if abs(xdiff) > r:
        return False
    ydiff = center[1] - pos[1]
    if abs(ydiff) > r:
        return False
    if xdiff + ydiff < r:
        return True
    if xdiff**2 + ydiff**2 < r**2:
        return True