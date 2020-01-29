from common import maxnorm

class Rules():
    tickrate = 60
    # windowsize = Map.windowsize
    basespeed = 90.0 / tickrate  #rate, pixels
    startingfatigue = 400.0  #value
    eatspeed = 1.0 / tickrate  #rate
    foodspawnchance = maxnorm([20, 12, 7])  #value
    foodsamount = [5,8,13]
    bashstunspan = 4.0 * tickrate  #timespan
    bashstolenfood = 20
    scoremultiplier1 = 10  #value during game per food consumed
    scoremultiplier2 = 2  #value when game over per food left
    attackcd = 8.0 * tickrate  #timespan
    backpackcap = 60.0  #value
    startingbackpack = 0
    reachdistance = 20.0
    overlapdistance = 5.0
    apprxdirchanges = 3  # utilized in taskwander approximate number of direction changes per 10 secs
    apprxdirchanges_unittime = 10 # seconds
    visionrange = 175
    foodrespawntickperiod = 30
    startingfoodcount = 35
    spawnedfoodcap = 100
    unitsize = 2.5
    


    class Fatiguedrain():
        move = 0.1  # per pixel
        collect = 1  #per action
        attack = 3  #per action
        beaten = 2  #per action
        lookaround = 3  #per action

    class Map():
        bezel = 10
        windowsize = [1024, 768]
        width = windowsize[0]-200 # left for fatigue bar etc. 
        height = windowsize[1]
        size = [width-2*bezel,height-2*bezel]
        bounds = [[0+bezel, width-bezel], [0+bezel, height-bezel]]
        center = [int((boundary[0]+boundary[1]) / 2) for boundary in bounds]
        
