from era import Era
from entities import State,Task,Food,Gatherer
from rules import Rules

class Gathering():
    def __init__(self,gatherercount = 3, 
    startingfoodcount = None, 
    foodregrowthperiod = None):

        self.era = Era()

        if startingfoodcount is not None:
            self.era.startingfoodcount = startingfoodcount

        if foodregrowthperiod is not None:
            self.era.foodrespawntickperiod = foodregrowthperiod * Rules.tickrate

        self.names = ['adam','eve','abel','cain']

        for aye in range(gatherercount):
            if aye>3:
                name = 'gatherer'+str(aye)
            else:
                name = self.names[aye]
            self.era.addGatherer(Gatherer(name=name, startingpos=self.era.getRandomPos()))
            self.era.assign2Gatherer(name, defaultTraining)

    def addGatherer(self,name):
        self.era.addGatherer(Gatherer(name=name, startingpos=self.era.getRandomPos()))
    
    def assign2Gatherer(self,name,instructions):
        self.era.assign2Gatherer(name, instructions)

    def begin(self):
        self.era.begin()


def defaultTraining(self):
    distratio = 1
    f1 = self.closestfood()
    gat1 = self.closestgatherer()
    if (f1 is not None):
        fd = self.getdistance(f1)
        gd = self.getdistance(gat1)
        if (gd * distratio < fd) and (self.checkstate(gat1) != State.beaten
                                    ) and (self.foodcarried(gat1)):
            self.assignTask(Task.attackmove, gat1)
        elif len(self.knownfoods()) > 0:
            self.assignTask(Task.collect, self.closestfood())
        else:
            self.assignTask(Task.wander)
    elif (self.checkstate(gat1) != State.beaten) and (self.foodcarried(gat1)):
        self.assignTask(Task.attackmove, gat1)
    else:
        self.assignTask(Task.wander)




