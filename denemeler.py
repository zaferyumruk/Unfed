#%%

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from gatherer import gatherer
tickrate = 60
with PyCallGraph(output=GraphvizOutput()):
    aaron = gatherer(tickrate=tickrate, startingpos=[380, 280])
    aaron.update()


#%%
from gatherer import gatherer


#%%
dummy = gatherer()
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

#%%
import pygame
pygame.font.get_fonts()

#%%
