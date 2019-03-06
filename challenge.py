from gathering import Gathering, defaultTraining
from entities import State,Task, Foodtype

def SKYteamAttack(self):
    closestfood = self.closestfood()
    closestgatherer = self.closestgatherer()
    if self.readytoattack() == True:
        if self.getdistance(closestgatherer)<70:
            if self.checkstate(closestgatherer) == State.charging:
                self.assignTask(Task.attackmove, closestgatherer)
            else: 
                if self.foodcarried(closestgatherer) == 0:
                    self.assignTask(Task.collect, closestfood)
                else:
                    self.assignTask(Task.attackmove, closestgatherer)
        else:
            self.assignTask(Task.collect, closestfood)
    if self.readytoattack() == False:
        self.assignTask(Task.collect, closestfood)
    if closestfood is None:
        self.assignTask(Task.wander,20)

def icabTask(self):
    closestfood = self.closestfood()
    closestgatherer = self.closestgatherer()
    if closestfood is not None:
        if self.getdistance(closestfood)<self.getdistance(closestgatherer):
            self.assignTask(Task.collect, closestfood)
            return
    if self.checkstate(closestgatherer) != State.beaten:
        self.assignTask(Task.attackmove, closestgatherer)
    else:
        gatherers = self.visiblegatherers()
        for gatherer in gatherers:
            if self.getfacing(gatherer) < 10 :
                self.assignTask(Task.escape, gatherer)
                return  
        self.assignTask(Task.wander,20)

def must(self):
    closest_pineapple = self.closestfood(Foodtype.pineapple)
    closest_apple = self.closestfood(Foodtype.apple)
    closest_raspberry = self.closestfood(Foodtype.raspberry)
    closest_food = self.closestfood()
    closest_gatherer = self.closestgatherer()
    
    if closest_gatherer is not None and self.getdistance(closest_gatherer) < 60 and self.checkstate(closest_gatherer) != State.beaten:
        if self.foodcarried(self) > self.foodcarried(closest_gatherer):
            if self.getdistance(closest_food)+20 < self.getdistance(closest_gatherer):
                self.assignTask(Task.collect,closest_food)
            else:
                self.assignTask(Task.escape,closest_gatherer)
        else:        
            self.assignTask(Task.attackmove,closest_gatherer)
    else:
        if closest_pineapple is not None:
            self.assignTask(Task.collect,closest_pineapple)
        elif closest_apple is not None and self.getdistance(closest_apple) < 120 :
            self.assignTask(Task.collect,closest_apple)
        elif closest_raspberry is not None and self.getdistance(closest_raspberry) < 80 :
            self.assignTask(Task.collect,closest_raspberry)
        else:
            self.assignTask(Task.wander,3)



def peace(self):
    closestfood = self.closestfood()
    closestgatherer = self.closestgatherer()
    if (self.checkstate(closestgatherer) == State.following or self.checkstate(closestgatherer) == State.charging):
        if self.getdistance(closestgatherer)<25:
            self.assignTask(Task.escape, closestgatherer)
    if closestfood is not None:
        if self.getdistance(closestfood)<self.getdistance(closestgatherer):
            self.assignTask(Task.collect, closestfood)
            return
    else:
        self.assignTask(Task.wander,20)

def godofwar(self):

    closestfood = self.closestfood()
    closestgatherer = self.closestgatherer()

    if self.getdistance(closestgatherer)<21:
        if self.getfacing(closestgatherer) < 45:
            self.assignTask(Task.attackmove, closestgatherer)
    elif closestfood is not None:
        if self.getdistance(closestfood)<self.getdistance(closestgatherer):
            self.assignTask(Task.collect, closestfood)
            return
    else:
        self.assignTask(Task.wander,20)

gathering = Gathering(gatherercount=0)

gathering.addGatherer('seker',6)
gathering.assign2Gatherer('seker', peace)

gathering.addGatherer('biber',7)
gathering.assign2Gatherer('biber', godofwar)

gathering.addGatherer('must',10)
gathering.assign2Gatherer('must',must)

gathering.addGatherer('ICAB',9)
gathering.assign2Gatherer('ICAB', icabTask)

gathering.addGatherer('FrogInBlack',7)
gathering.assign2Gatherer('FrogInBlack', SKYteamAttack)

gathering.begin()
