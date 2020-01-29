from gathering import Gathering, defaultTraining
from entities import State,Task, Foodtype

def collectclosestFood(self):
    closestfood = self.closestfood()
    if closestfood is not None:
        self.assignTask(Task.collect, closestfood)
    else:
        self.assignTask(Task.wander,0.1)

#you can add number of "default" gatherers
gathering = Gathering(gatherercount=6)

# you can also add your own gatherer
# check \sprites\characters folder, cXYYYY.png --> X is the gatherer sprite no
gathering.addGatherer('afguc',11) #(gatherername[string],gathererspriteno[int])
gathering.assign2Gatherer('afguc', collectclosestFood)  #(gatherername[string],instructions[func])

# starts the gathering
gathering.begin()
