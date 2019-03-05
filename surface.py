from pygame import gfxdraw
import numpy as np
import math, os, pygame
from entities import Foodtype, Direction, State, Food

from common import checkStrConvert, angle_vector, angle_vector_custom
from rules import Rules

class Colors():
    white = [255, 255, 255]
    black = [0, 0, 0]
    gray = [80, 80, 80]
    chocolate = [210, 105, 30]
    red = [255, 0, 0]
    yellow = [255, 255, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]
    magenta = [255, 0, 255]
    groundgreen = [50,80,50]
    darkgrey = [35,35,35]


class GameWindow():
    def __init__(self, windowsize=[800, 600], caption='Unfed', bounds = [[0,800],[0,600]]):

        pygame.font.init()

        # self.HUDfont = pygame.font.SysFont('Comic Sans MS', 15) #This creates a new object on which you can call the render method.
        self.HUDfont = pygame.font.SysFont('Rockwell', 15, True)
        self.labelfont = pygame.font.SysFont('Rockwell', 15, True)
        self.infofont = pygame.font.SysFont('tahoma', 13)

        self.windowsize = windowsize
        self.colors = [Colors.chocolate, Colors.red, Colors.green,
            Colors.blue, Colors.magenta
        ]
        self.gameDisplay = pygame.display.set_mode(self.windowsize)
        self.gameDisplay.fill(Colors.black)

        pygame.display.set_caption(caption)


        self.unitsize = Rules.unitsize
        self.acttop = bounds[0][0]
        self.actleft = bounds[1][0]
        self.actheight = bounds[0][1] - self.acttop
        self.actwidth = bounds[1][1] - self.actleft
        self.activerect = [self.acttop,self.actleft,self.actheight,self.actwidth]

        self.statesprites = preloadStateSprites()
        self.foodsprites = preloadFoodSprites()

        self.bordercolor = Colors.darkgrey
        self.borderxbase = self.actleft+self.actwidth
        self.borderybase = self.actleft+self.actwidth
        self.borderwidth = self.windowsize[0] - self.actwidth

        # self.watchedattrs = [
        #     '_foodsknowncount', '_fatigue', '_state', '_backpack',
        #     '_stunnedleft', '_attackcd', '_score', '_currenttask'
        # ]
        self.watchedattrs = [
            '_direction'
        ]
        self.infoHUDhy = 15
        self.infoHUDhx = 120
        self.infoHUDystart = self.windowsize[1] - 25

        self.fog = pygame.Surface(Rules.Map.size)
        self.playzone = pygame.Surface(Rules.Map.size)

        self.foodcolor = {Foodtype.raspberry: Colors.red,
            Foodtype.apple : Colors.green,
            Foodtype.pineapple : Colors.yellow}

        pygame.display.update()


    def update(self,era) :

        self.gameDisplay.fill(Colors.black)

        # pygame.display.update()

        gathererlist = era.gathererlist
        gathererspritelist = era.gathererspritelist
        foodlist = era.foodlist
        gameover = era.checkgameover()

        self.playzone.fill(Colors.groundgreen)
        self.fog.fill(Colors.white)
        # pygame.gfxdraw.box(self.gameDisplay, self.activerect , Colors.red + [10])

        # pixels = pygame.surfarray.pixels2d(self.fog)
        # pixels ^= 2 ** 32 - 1
        # del(pixels)
        # if gameover:
        #     self.gameDisplay.fill(Colors.blue)
        # else:
        #     self.gameDisplay.fill(Colors.white)

        # self.infoHUD()

        for food in foodlist:
            self.updateFoodOnBoard(food)

        # dudecount = 0
        for idx,dude in enumerate(gathererlist):
            self.updateGathererOnBoard(dude, gathererspritelist[dude])
            # dudecount = dudecount + 1
            # self.infoHUD(dude, dudecount)

        # self.infoHUD(gathererlist)

        self.fatigueinfoBar(gathererlist)

        self.fog.set_alpha(30,2)

        self.gameDisplay.blit(self.playzone,[self.acttop,self.actleft])
        self.gameDisplay.blit(self.fog,[self.acttop,self.actleft])

        #CUSTOM DEBUG TEXT
        # angle = ((angle_vector(gathererlist[0]._direction) + 180)+90)%360-180
        # angle = angle_vector_custom(gathererlist[0]._direction)
        # txt = 'direction:'+str(gathererlist[0]._direction) + ' angle:' + str(angle)
        # self.custominfoHUD(txt)

        # txt1 = gathererlist[0]._name + ' facing ' + gathererlist[-1]._name + 'with '
        # self.custominfoHUD(txt1 + str(gathererlist[-1].getfacing(gathererlist[0])) + ' degrees')

        # afood = gathererlist[1].closestgatherer()
        # if afood is not None:
        #     # txt1 = afood._foodtype.name + ' staying in ' + str(gathererlist[1].getdirection(afood))
        #     txt1 = afood._name + ' staying in ' + str(
        #         gathererlist[1].getdirection(afood))
        #     self.custominfoHUD( txt1 + 'degrees wrt ' + gathererlist[1]._name)
        # self.gameDisplay.blit(self.fog,[0,0])


        pygame.display.update()

    def updateFoodOnBoard(self, food):
        count = food._uniqueID

        if food._active:
            size =int ( food._amount * self.unitsize + len(food._boost) * self.unitsize*2 )
        else:
            size = int (self.unitsize)
        # color1 = self.colors[(count) % len(self.colors)]
        color1 = self.foodcolor[food._foodtype]
        intpos = [int(pos) for pos in food._position]
        nametext = self.labelfont.render(food._foodtype.name, False,
                                    Colors.black)
        if food._active:
            # pygame.gfxdraw.box(
            #     self.playzone,
            #     [intpos[0] - size / 2, intpos[1] - size / 2, size, size],
            #     color1)
            self.playzone.blit(self.foodsprites[food._foodtype], (intpos[0], intpos[1]))

            # self.playzone.blit(nametext, (intpos[0], intpos[1]))
        else:
            pygame.gfxdraw.box(
                self.playzone,
                [intpos[0] - size / 2, intpos[1] - size / 2, size, size],
                color1)


    def updateGathererOnBoard(self,gatherer,gatherersprite):
        # innerradius = int(self.unitsize * 2)
        # outerradius = int(self.unitsize * 7)
        count = gatherer._uniqueID

        # color1 = self.colors[(count) % len(self.colors)]
        # color2 = self.colors[(count + 1) % len(self.colors)]
        intpos = [int(pos) for pos in gatherer._position]
        # dirlenscale = int(self.unitsize * 7)
        # dirtippos = [
        #     int(pos + gatherer._direction[idx] * dirlenscale)
        #     for idx, pos in enumerate(gatherer._position)
        # ]

        # statustext = self.labelfont.render(
        #     str(gatherer._state), False, Colors.white)
        namelabel = self.labelfont.render(
            str(gatherer._name), False, Colors.white)

        # pygame.gfxdraw.filled_circle(self.playzone, intpos[0],
        #                                 intpos[1], outerradius, color1)
        # pygame.gfxdraw.filled_circle(self.playzone, intpos[0],
        #                                 intpos[1], innerradius, color2)
        # pygame.gfxdraw.line(self.playzone, intpos[0], intpos[1],
        #                     dirtippos[0], dirtippos[1], color2)
        # pygame.gfxdraw.circle(self.gameDisplay, intpos[0], intpos[1],
        #                       gatherer._visionRange, color1+[120])

        gatherersprite.step(self.playzone,namelabel)



        pygame.gfxdraw.filled_circle(self.fog, intpos[0],
                                        intpos[1], gatherer._visionRange, Colors.black)
        # self.playzone.blit(statustext,
        #                         (gatherer._position[0], gatherer._position[1]))
        # self.playzone.blit(namelabel,
        #                    (intpos[0] - self.charsprite_halfsize[0],
        #                     intpos[1] - self.charsprite_halfsize[1]))

    def custominfoHUD(self, text):
        customtext = self.labelfont.render(text, False, Colors.black)
        self.gameDisplay.blit(customtext, (200, 200))

    def fatigueinfoBar(self,gathererlist):
        gathererlist.sort(key=lambda x: x._score,reverse = True)
        ybezel = 20
        xbase = Rules.Map.bounds[0][1]+35
        for idx,gatherer in enumerate(gathererlist):
            count = gatherer._uniqueID
            color1 = self.colors[(count) % len(self.colors)]

            nametext = self.HUDfont.render(gatherer._name, False, Colors.white)
            datatext = self.HUDfont.render('%d'% (gatherer._score), False, Colors.white)

            h = 30
            ybase = idx * (h + 5) + ybezel


            pygame.draw.rect(self.gameDisplay, Colors.white,
                                [xbase, ybase, 100, 25], 1)
            barvalue = int(gatherer._fatigue/Rules.startingfatigue * 100)
            # barvalue = int(gatherer._backpack * 20)
            if barvalue != 0:
                pygame.draw.rect(self.gameDisplay, color1,
                                    [xbase, ybase, barvalue, 25], 0)

            self.gameDisplay.blit(nametext, (xbase+10, ybase))
            self.gameDisplay.blit(datatext, (xbase+120, ybase))
            self.gameDisplay.blit(self.statesprites[gatherer._state], (xbase-33, ybase-3))



    def drawborder(self):
        pygame.draw.rect(self.gameDisplay, self.bordercolor,[self.borderxbase, self.borderybase, self.actheight, self.borderwidth], 0)

    def infoHUD(self, gathererlist):
        drawsurface = self.playzone
        for attrname in self.watchedattrs:
            self.infoHUDxstart = self.infoHUDhx
            datatext = self.infofont.render(
                str(attrname), False, Colors.black)
            drawsurface.blit(datatext,
                             (self.infoHUDxstart, self.infoHUDystart))
            self.infoHUDystart = self.infoHUDystart - self.infoHUDhy

        for idx, gatherer in enumerate(gathererlist):
            self.infoHUDxstart = self.infoHUDhx * (idx + 1)
            for attrname in self.watchedattrs:
                attr = getattr(gatherer, attrname)
                if (type(attr) is list) and len(attr)>0 and (checkStrConvert(attr[0],float)):
                    bb = '%.2f:' * len(attr)
                    datatext = self.infofont.render(bb % tuple(attr), False,
                                                    Colors.black)
                elif type(attr) is float:
                    datatext = self.infofont.render('%.2f' % (attr), False,
                                                    Colors.black)
                else:
                    datatext = self.infofont.render(
                        str(attr), False, Colors.black)
                drawsurface.blit(datatext,
                                 (self.infoHUDxstart, self.infoHUDystart))
                self.infoHUDystart = self.infoHUDystart - self.infoHUDhy
            datatext = self.infofont.render(
                str(gatherer._name), False, Colors.black)
            drawsurface.blit(datatext,
                             (self.infoHUDxstart, self.infoHUDystart))

def preloadStateSprites():
    statespritelist = {}
    basedir = 'sprites\\states'
    iconlist = os.listdir(basedir)  # returns list
    for icon in iconlist:
        statename = ''.join(icon.split('.')[0:-1])
        state = getattr(State, statename)
        statespritelist[state] = pygame.transform.scale(
            pygame.image.load(basedir + '\\' + icon), (30, 30))
    return statespritelist


def preloadFoodSprites():
    foodspritelist = {}
    basedir = 'sprites\\foods'
    iconlist = os.listdir(basedir)  # returns list
    basesize = (3,3)
    for icon in iconlist:
        foodtypename = ''.join(icon.split('.')[0:-1])
        try:
            foodtype = getattr(Foodtype, foodtypename)
        except:
            continue
        amount, _ = Food()._getfoodatts(foodtype)
        size = [el*amount for el in basesize]
        foodspritelist[foodtype] = pygame.transform.scale(
            pygame.image.load(basedir + '\\' + icon), size)
    return foodspritelist

class GathererSprite():
    def __init__(self, gatherer, characterskin = 1, seq2frame=[0, 1, 2, 1], stride=6):
        self.gatherer = gatherer
        self.characterskin = characterskin
        self.stride = stride
        self.updateperiod = np.round(
            Rules.tickrate / (Rules.basespeed * Rules.tickrate / self.stride))
        self.seq2frame = seq2frame
        self.activeframe = 1 #initially standing
        self.seqidx = 1 #to be correlated with activeframe
        self.updatecd = self.updateperiod
        self.activedirection = Direction.south #initially facing south
        self.dir2action = {Direction.south:0 ,Direction.west:1,Direction.east:2,Direction.north:3}
        self.updateactiveaction()
        self.frames = np.unique(seq2frame)

        self.preloadsprites()
        self.updateactivespritelist()

    def preloadsprites(self):
        self.charspritelists = {}
        pathheader = 'sprites\\characters\\'
        for direct in self.dir2action:
            self.charspritelists[direct] = []
            for frame in self.frames:
                path = pathheader+'c%sa%sf%s.png' % (self.characterskin,self.dir2action[direct],frame)
                self.charspritelists[direct].append(pygame.image.load(path))
        self.charsprite_halfsize = [24,24]

        self.statespritelists = {}

        for frame in self.frames:
            path = pathheader+'c%sa%sf%s.png' % (self.characterskin,self.dir2action[direct],frame)
            self.charspritelists[direct].append(pygame.image.load(path))

    def step(self, surface, namelabel):
        self.updateactiveaction()
        self.updateactivespritelist()
        self.updateactiveframe()
        self.add2surface(surface, namelabel)

    def add2surface(self, surface, namelabel):
        intpos = [int(pos) for pos in self.gatherer._position]
        surface.blit(
            self.activespritelist[self.activeframe],
            (intpos[0] - self.charsprite_halfsize[0],
             intpos[1] - self.charsprite_halfsize[1]))  #intpos replace
        surface.blit(namelabel, (intpos[0] - namelabel.get_width()/2,
                                 intpos[1] - namelabel.get_height()/2 - self.charsprite_halfsize[1]-3))  #intpos replace

    def updateactiveframe(self):
        if self.isgathererstationary():
            self.activeframe = 1
        elif self.updatecd == 0:
            self.seqidx = (self.seqidx + 1) % len(self.seq2frame)
            self.activeframe = self.seq2frame[self.seqidx]
            self.updatecd = self.updateperiod
        else:
            self.updatecd = self.updatecd - 1

    def updateactiveaction(self):
        angle = angle_vector_custom(self.gatherer._direction)
        if -45 <= angle < 45:
            self.activedirection = Direction.north
        elif 45 <= angle < 135:
            self.activedirection = Direction.east
        elif 135 <= angle <= 180 or -180 <= angle < -135:
            self.activedirection = Direction.south
        elif -135 <= angle < -45:
            self.activedirection = Direction.west
        self.activeaction = self.dir2action[self.activedirection]

    def updateactivespritelist(self):
        self.activespritelist = self.charspritelists[self.activedirection]

    def isgathererstationary(self):
        state = self.gatherer._state
        if state == State.beaten or state == State.exhausted or state == State.idle or state == State.lookingaround:
            return True
        else:
            return False