from sampleRun import sampleHunt
from entities import State,Task, Foodtype



def collectclosestFood(self):
    closestfood = self.closestfood()
    if closestfood is not None:
        self.assignTask(Task.collect, closestfood)
    else:
        self.assignTask(Task.wander)

def appleLover(self):
    closestfood = self.closestfood(Foodtype.apple)
    if closestfood is not None:
        self.assignTask(Task.collect, closestfood)
    else:
        self.assignTask(Task.wander)


def attackclosestgatherer(self):
    gatherers = self.visiblegatherers()
    self.assignTask(Task.attackmove, gatherers[0])

def attackclosestgatherer_nonhater(self):
    gatherers = self.visiblegatherers()
    for gatherer in gatherers:
        if self.checkstate(gatherer) != State.beaten:
            self.assignTask(Task.attackmove, gatherer)
            return

def attackorcollect(self):
    closestfood = self.closestfood()
    closestgatherer = self.closestgatherer()
    if closestfood is not None:
        if self.getdistance(closestfood)<self.getdistance(closestgatherer):
            self.assignTask(Task.collect, closestfood)
            return
    self.assignTask(Task.attackmove, closestgatherer)

def runfromhatefuleyes(self):
    gatherers = self.visiblegatherers()
    for gatherer in gatherers:
        if self.getfacing(gatherer) < 10 :
            self.assignTask(Task.escape, gatherer)
            return
    self.assignTask(Task.wander, gatherer)


def runfromhatefuleyes_ifclose(self):
    gatherers = self.visiblegatherers()
    for gatherer in gatherers:
        if self.getfacing(gatherer) < 10 and self.getdistance(gatherer) < 300:
            self.assignTask(Task.escape, gatherer)
            return
    self.assignTask(Task.wander, gatherer)

def runfromhatefuleyes_ifcloseandnotbeaten(self):
    gatherers = self.visiblegatherers()
    for gatherer in gatherers:
        if self.getfacing(gatherer) < 10 and self.getdistance(gatherer) < 300 and self.checkstate(gatherer) != State.beaten:
            self.assignTask(Task.escape, gatherer)
            return
    self.assignTask(Task.wander, gatherer)



hunt = sampleHunt(gatherercount=7)

hunt.addGatherer('zaf')
hunt.assign2Gatherer('zaf',appleLover)

hunt.begin()