from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from gatherer import Gatherer
tickrate = 60
with PyCallGraph(output=GraphvizOutput()):
    aaron = Gatherer(startingpos=[380, 280])
    aaron.update()