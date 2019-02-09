import numpy as np
from enum import Enum


class states(Enum):
    idle = 1
    lookingaround = 2
    following = 3
    eating = 4
    exhausted = 5



class fatiguedrain():
    move = 0.1
    eat = 1
    attack = 2
    beaten = 4


class gatherer():
    def __init__(self, tickrate, fatigue = 100, startingpos = [0.0,0.0], speed = 2.5, direction = [1.0,1.0]):
        #variables
        self.position = startingpos
        self.assingdirection(direction)
        self.fatigue = fatigue
        self.state = states.idle
        self.belly = None
        self.boosts = []
        self.modifier = {
            'fatiguedrain': 1.0,
            'speed': 1.0,
            'eattime': 1.0,
            'stuntime': 1.0,
            'stunnedtime': 1.0
        }

        # attributes
        self.speedbase = speed
        self.eattimebase = 3
        self.stunbase = 4

    def update(self):
        self.mathStuff()
        self.applyModifiers()
        self.step()
        self.updateVision()

    def applyModifiers(self):
        self.speed = self.speedbase * self.modifier['speed']

    def step(self):
        fatigueloss = self.speed * fatiguedrain.move * self.modifier['fatiguedrain']
        if self.fatigue != 0:
            if self.fatigue < fatigueloss:
                remains = self.fatigue / fatigueloss
                self.fatigue = 0
            else:
                remains = 1
                self.fatigue = self.fatigue - fatigueloss

            self.position[0] = self.position[0] + self.direction[0] * self.speed * remains
            self.position[1] = self.position[1] + self.direction[1] * self.speed * remains



    def updateVision(self):
        return None

    def mathStuff(self):
        return None

    def assingdirection(self,direction):
        norm = np.linalg.norm(direction)
        self.direction = [ax/norm for ax in direction]
