from common import maxnorm

class Rules():
    tickrate = 60
    basespeed = 75.0 / tickrate  #rate, pixels
    startingfatigue = 6000.0  #value
    eatspeed = 1.0 / tickrate  #rate
    foodspawnchance = maxnorm([50, 40, 5])  #value
    bashstunspan = 8.0 * tickrate  #timespan
    scoremultiplier = 10  #value
    attackcd = 3.0 * tickrate  #timespan
    backpackcap = 60.0  #value
    reachdistance = 20.0
    overlapdistance = 5.0
    chance2changedir = 0.005  # utilized in taskwander
    visionrange = 100
    foodrespawntickperiod = 20
    startingfoodcount = 5
    spawnedfoodcap = 5

    class Fatiguedrain():
        move = 0.1  # per pixel
        collect = 1  #per action
        attack = 3  #per action
        beaten = 2  #per action
        lookaround = 3  #per action

    class Map():
        size = [800, 600]
        bounds = [[0, 800], [0, 600]]
        center = [int(entry / 2) for entry in size]
