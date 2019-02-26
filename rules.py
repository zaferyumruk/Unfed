from common import maxnorm

class Rules():
    tickrate = 60
    windowsize = [1224, 800]
    basespeed = 90.0 / tickrate  #rate, pixels
    startingfatigue = 200.0  #value
    eatspeed = 1.0 / tickrate  #rate
    foodspawnchance = maxnorm([50, 40, 5])  #value
    bashstunspan = 5.0 * tickrate  #timespan
    scoremultiplier1 = 10  #value during game per food consumed
    scoremultiplier2 = 2  #value when game over per food left
    attackcd = 8.0 * tickrate  #timespan
    backpackcap = 60.0  #value
    startingbackpack = 0
    reachdistance = 20.0
    overlapdistance = 5.0
    apprxdirchanges = 3  # utilized in taskwander approximate number of direction changes per 10 secs
    apprxdirchanges_unittime = 10 # seconds
    visionrange = 150
    foodrespawntickperiod = 30
    startingfoodcount = 56
    spawnedfoodcap = 150


    class Fatiguedrain():
        move = 0.1  # per pixel
        collect = 1  #per action
        attack = 3  #per action
        beaten = 2  #per action
        lookaround = 3  #per action

    class Map():
        bounds = [[0, 1024], [0, 800]]
        center = [int((boundary[0]+boundary[1]) / 2) for boundary in bounds]
        
