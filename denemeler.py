#%%


class Colors():
    white = (255, 255, 255)
    black = (0, 0, 0)
    chocolate = (210, 105, 30)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    magenta = (255, 0, 255)
#%%
Colors.white

#%%

#%%
colorset = list(colors)
#%%
from gatherer import Gatherer

#%%

#%%
checkStrConvert('13',int)
#%%
dummy = Gatherer()
dummy.fatigue
#%%
a = None

#%%

from enum import Enum


class foodtype(Enum):
    berry = 1
    apple = 2
    pineapple = 3
#%%
def anf(a,b,c):
    return (a,b,c)
#%%
[out1,out2,out3] = anf(1,2,3)
#%%
out1
#%%
np.arange(1, len(list(foodtype)))
#%%
dir(list(foodtype)[0].name)
len(list(foodtype))
#%%
if not a:
    print('waw')
#%%
int(a)

#%%
b = a/np.linalg.norm(a)

#%%
import numpy as np
np.arctan(1/np.sqrt(3))/np.pi*360

#%%
class fatiquedrain():
    move = 1
    eat = 1
    attack = 3

#%%
fatiquedrain.move

#%%
from enum import Enum


class gathererstates(Enum):
    lookingaround = 1
    following = 2
    eating = 3
    digesting = 4
#%%
from gatherer import normalize

#%%
norm = np.linalg.norm([0, 0])
norm
#%%
'%.2f' % (3.98344)
#%%
[0.0] * len([0,0,0])
#%%
type(1.0) is float

#%%
(out)
#%%
import pygame
pygame.init()
infofont = pygame.font.SysFont('tahoma', 13)
#%%
infofont.linesize()
#%%
namelabel = infofont.render(str('a'), False, (0, 0, 0))

#%%
namelabel.get_height()
#%%
class fatiguedrain():
    move = 1  #0.05
    collect = 1
    attack = 4
    beaten = 2
    lookaround = 3
    class fatiguedrain1():
        move = 1  #0.05
        collect = 1
        attack = 4
        beaten = 2
        lookaround = 3

fatiguedrain.move
#%%
import pygame
pygame.font.get_fonts()

#%%


gFood=[]
gFood.append(Gatherer(name='eve', startingpos=myEra.getRandomPos()))
gFood.append(Gatherer(name='eve', startingpos=myEra.getRandomPos()))
gFood.append(Gatherer(name='eve', startingpos=myEra.getRandomPos()))
gFood.append(Gatherer(name='eve', startingpos=myEra.getRandomPos()))
gFood.append(Gatherer(name='eve', startingpos=myEra.getRandomPos()))

g1=Gatherer(name='adam', startingpos=myEra.getRandomPos())

#%%
g1.closestentity(gFood)

#%%
gFood[2]

#%%
[g1._evalPosition(ga) for ga in gFood]

#%%
from entities import Gatherer,Food,Foodtype
from era import Era

myEra = Era()

gFood = []
gFood.append(Food(startingpos=myEra.getRandomPos()))
gFood.append(Food(startingpos=myEra.getRandomPos()))
gFood.append(Food(startingpos=myEra.getRandomPos()))
gFood.append(Food(startingpos=myEra.getRandomPos()))
gFood.append(Food(startingpos=myEra.getRandomPos()))
gFood.append(Food(startingpos=myEra.getRandomPos()))
gFood.append(Food(startingpos=myEra.getRandomPos()))

gGatherer = []
gGatherer.append(Gatherer(name='eve', startingpos=myEra.getRandomPos()))
gGatherer.append(Gatherer(name='eve', startingpos=myEra.getRandomPos()))
gGatherer.append(Gatherer(name='eve', startingpos=myEra.getRandomPos()))
gGatherer.append(Gatherer(name='eve', startingpos=myEra.getRandomPos()))

g1 = Gatherer(name='adam', startingpos=myEra.getRandomPos())

g1.foodsvisible = gFood
g1.gatherersknown = gGatherer


#%%
g1.foodsvisible()
#%%

g1.getdistance(g1.foodsvisible[0])


#%%
dists = [[g1._evalPosition(ga),ga.foodtype] for ga in gFood]
dists

#%%

#%%
g1.getdistance(g1.gatherersaround())

#%%
out

#%%
a = [1,2,3]

#%%
a.remove(4)

#%%
