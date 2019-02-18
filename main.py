#%%
from era import Era
from entities import States,Tasks,Food,Gatherer
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


myEra = Era()
# myEra.foodrespawntickperiod = 45

myEra.addGatherer(Gatherer(name='adam', startingpos=myEra.getRandomPos()))
myEra.addGatherer(Gatherer(name='eve', startingpos=myEra.getRandomPos()))

myEra.addGatherer(Gatherer(name='cain', startingpos=myEra.getRandomPos()))
myEra.addGatherer(Gatherer(name='abel', startingpos=myEra.getRandomPos()))

for _ in range(15):
    myEra.addFood(Food(startingpos=myEra.getRandomPos()))

# myEra.addFood(Food(startingpos=[200, 300]))
# myEra.addFood(Food(startingpos=[250, 350]))
# myEra.addFood(Food(startingpos=[280, 380]))
# myEra.addFood(Food(startingpos=[350, 380]))

def assignRandomCollect(gatherer):
    if gatherer.state == States.idle or gatherer.state == States.moving:
        if len(gatherer.foodsaround)>0:
            gatherer.assignTask(Tasks.collect, gatherer.closestfood())
        else:
            gatherer.assignTask(Tasks.wander)


def assignRandomCollect_aggresive1(self):
    distratio = 1
    if self.state == States.idle or self.state == States.moving:
        f1 = self.closestfood()
        gat1 = self.closestgatherer()
        if (f1 is not None):
            fd = self.getdistance(f1)
            gd = self.getdistance(gat1)
            if (gd * distratio < fd) and (gat1.state != States.beaten) and (
                    self.iscarryingfood(gat1)):
                self.assignTask(Tasks.attackmove, gat1)
            elif len(self.foodsaround) > 0:
                self.assignTask(Tasks.collect, self.closestfood())
            else:
                self.assignTask(Tasks.wander)
        elif (gat1.state != States.beaten) and (self.iscarryingfood(gat1)):
            self.assignTask(Tasks.attackmove, gat1)
        else:
            self.assignTask(Tasks.wander)


def assignRandomCollect_aggresive2(self):
    distratio = 2
    # if self.state == States.idle or self.state == States.moving:
    f1 = self.closestfood()
    gat1 = self.closestgatherer()
    if (f1 is not None):
        fd = self.getdistance(f1)
        gd = self.getdistance(gat1)
        if (gd * distratio < fd) and (gat1.state != States.beaten) and (
                self.iscarryingfood(gat1)):
            self.assignTask(Tasks.attackmove, gat1)
        elif len(self.foodsaround) > 0:
            self.assignTask(Tasks.collect, self.closestfood())
        else:
            self.assignTask(Tasks.wander)
    elif (gat1.state != States.beaten) and (self.iscarryingfood(gat1)):
        self.assignTask(Tasks.attackmove, gat1)
    else:
        self.assignTask(Tasks.wander)


def assignRandomCollect_aggresive3(self):
    distratio = 3
    if self.state == States.idle or self.state == States.moving:
        f1 = self.closestfood()
        gat1 = self.closestgatherer()
        if (f1 is not None):
            fd = self.getdistance(f1)
            gd = self.getdistance(gat1)
            if (gd * distratio < fd) and (gat1.state != States.beaten) and (
                    self.iscarryingfood(gat1)):
                self.assignTask(Tasks.attackmove, gat1)
            elif len(self.foodsaround) > 0:
                self.assignTask(Tasks.collect, self.closestfood())
            else:
                self.assignTask(Tasks.wander)
        elif (gat1.state != States.beaten) and (self.iscarryingfood(gat1)):
            self.assignTask(Tasks.attackmove, gat1)
        else:
            self.assignTask(Tasks.wander)


def assignRandomCollect_aggresive4(self):
    distratio = 2.1
    # if self.state == States.idle or self.state == States.moving:
    f1 = self.closestfood()
    gat1 = self.closestgatherer()
    if (f1 is not None):
        fd = self.getdistance(f1)
        gd = self.getdistance(gat1)
        if (gd * distratio < fd) and (gat1.state != States.beaten) and (
                self.iscarryingfood(gat1)):
            self.assignTask(Tasks.attackmove, gat1)
        elif len(self.foodsaround) > 0:
            self.assignTask(Tasks.collect, self.closestfood())
        else:
            self.assignTask(Tasks.wander)
    elif (gat1.state != States.beaten) and (self.iscarryingfood(gat1)):
        self.assignTask(Tasks.attackmove, gat1)
    else:
        self.assignTask(Tasks.wander)


myEra.assign2Gatherer('adam', assignRandomCollect)
myEra.assign2Gatherer('eve', assignRandomCollect_aggresive4)
myEra.assign2Gatherer('cain', assignRandomCollect_aggresive2)
myEra.assign2Gatherer('abel', assignRandomCollect_aggresive3)

#%%
with PyCallGraph(output=GraphvizOutput()):
    myEra.begin()
