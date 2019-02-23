#%%
from era import Era
from entities import State,Task,Food,Gatherer
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def assignRandomCollect_aggresive1(self):
    distratio = 1
    if self.state == State.idle or self.state == State.moving:
        f1 = self.closestfood()
        gat1 = self.closestgatherer()
        if (f1 is not None):
            fd = self.getdistance(f1)
            gd = self.getdistance(gat1)
            if (gd * distratio < fd) and (gat1.state != State.beaten) and (
                    self.foodcarried(gat1)):
                self.assignTask(Task.attackmove, gat1)
            elif len(self.visiblefoods()) > 0:
                self.assignTask(Task.collect, self.closestfood())
            else:
                self.assignTask(Task.wander)
        elif (gat1.state != State.beaten) and (self.foodcarried(gat1)):
            self.assignTask(Task.attackmove, gat1)
        else:
            self.assignTask(Task.wander)


def assignRandomCollect_aggresive2(self):
    distratio = 2
    # if self.state == States.idle or self.state == States.moving:
    f1 = self.closestfood()
    gat1 = self.closestgatherer()
    if (f1 is not None):
        fd = self.getdistance(f1)
        gd = self.getdistance(gat1)
        if (gd * distratio < fd) and (gat1.state != State.beaten) and (
                self.foodcarried(gat1)):
            self.assignTask(Task.attackmove, gat1)
        elif len(self.visiblefoods()) > 0:
            self.assignTask(Task.collect, self.closestfood())
        else:
            self.assignTask(Task.wander)
    elif (gat1.state != State.beaten) and (self.foodcarried(gat1)):
        self.assignTask(Task.attackmove, gat1)
    else:
        self.assignTask(Task.wander)


def assignRandomCollect_aggresive3(self):
    distratio = 3
    if self.state == State.idle or self.state == State.moving:
        f1 = self.closestfood()
        gat1 = self.closestgatherer()
        if (f1 is not None):
            fd = self.getdistance(f1)
            gd = self.getdistance(gat1)
            if (gd * distratio < fd) and (gat1.state != State.beaten) and (
                    self.foodcarried(gat1)):
                self.assignTask(Task.attackmove, gat1)
            elif len(self.visiblefoods()) > 0:
                self.assignTask(Task.collect, self.closestfood())
            else:
                self.assignTask(Task.wander)
        elif (gat1.state != State.beaten) and (self.foodcarried(gat1)):
            self.assignTask(Task.attackmove, gat1)
        else:
            self.assignTask(Task.wander)


def assignRandomCollect_aggresive4(self):
    distratio = 2.1
    # if self.state == States.idle or self.state == States.moving:
    f1 = self.closestfood()
    gat1 = self.closestgatherer()
    if (f1 is not None):
        fd = self.getdistance(f1)
        gd = self.getdistance(gat1)
        if (gd * distratio < fd) and (gat1.state != State.beaten) and (
                self.foodcarried(gat1)):
            self.assignTask(Task.attackmove, gat1)
        elif len(self.visiblefoods()) > 0:
            self.assignTask(Task.collect, self.closestfood())
        else:
            self.assignTask(Task.wander)
    elif (gat1.state != State.beaten) and (self.foodcarried(gat1)):
        self.assignTask(Task.attackmove, gat1)
    else:
        self.assignTask(Task.wander)


def assignRandomCollect(gatherer):
    # if gatherer.state == State.idle or gatherer.state == State.moving:
    if len(gatherer.visiblefoods()) > 0:
        gatherer.assignTask(Task.collect, gatherer.closestfood())
    else:
        gatherer.assignTask(Task.wander)


def assignRandomCollectStop(gatherer):
    # if gatherer.state == State.idle or gatherer.state == State.moving:
    if len(gatherer.visiblefoods()) > 0:
        gatherer.assignTask(Task.collect, gatherer.closestfood())
    else:
        gatherer.assignTask(Task.wander)


def assignRandomCollect_aggresivetry(self):
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


def trycollect(self):
    f1 = self.closestgatherer()
    if self.isvisible(f1):
        self.assignTask(Task.escape, f1)
    # else:
    #     self.assignTask(Task.wander)


myEra = Era()
myEra.startingfoodcount = 0
# myEra.foodrespawntickperiod = 45

name = 'eve'
myEra.addGatherer(Gatherer(name=name, startingpos=myEra.getRandomPos()))
myEra.assign2Gatherer(name, trycollect)

name = 'adam'
myEra.addGatherer(Gatherer(name=name, startingpos=myEra.getRandomPos()))
myEra.assign2Gatherer(name, trycollect)

name = 'cain'
myEra.addGatherer(Gatherer(name=name, startingpos=myEra.getRandomPos()))
myEra.assign2Gatherer(name, trycollect)

name = 'abel'
myEra.addGatherer(Gatherer(name=name, startingpos=myEra.getRandomPos()))
myEra.assign2Gatherer(name, trycollect)

myEra.begin()

# myEra.addFood(Food(startingpos=[200, 300]))
# myEra.addFood(Food(startingpos=[250, 350]))
# myEra.addFood(Food(startingpos=[280, 380]))
# myEra.addFood(Food(startingpos=[350, 380]))

# # myEra.assign2Gatherer('adam', assignRandomCollect_aggresive4)
# myEra.assign2Gatherer('eve', assignRandomCollect_aggresivetry)
# myEra.assign2Gatherer('cain', assignRandomCollect_aggresivetry)
# myEra.assign2Gatherer('abel', assignRandomCollect_aggresivetry)

#%%
# with PyCallGraph(output=GraphvizOutput()):
# myEra.begin()

#

# myEra.addGatherer(Gatherer(name='adam', startingpos=myEra.getRandomPos()))