#%%
from PIL import Image
import os

def crop(im,height,width):
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)
# ​
#%%
# if __name__=='__main__':
infile='sprites1.png'
pageheight=192 #48
pagewidth=144 #48
frameheight = 48
framewidth = 48
start_num=1
pathdir = 'out'
im = Image.open(infile)
for charno,charpage in enumerate(crop(im,pageheight,pagewidth),start_num):
    path=os.path.join(pathdir,"IMG-%s.png" % (charno))
    # charpage.save(path, 'png')
    for actionno, action in enumerate(crop(charpage, frameheight, pagewidth), start_num):
        # path=os.path.join(pathdir,"IMG-char%s-action%s.png" % (charno,actionno))
        # action.save(path)
        for frameno, frame in enumerate(crop(action, frameheight, framewidth), start_num):
            path = os.path.join(pathdir,
                                "IMG-char%s-action%s-frame%s.png" % (charno, actionno,frameno))
            frame.save(path)
    #         if actionno == 1:
    #             path=os.path.join(pathdir,"IMG-char%s-action%s-frame%s.png" % (charno,actionno,frameno))
    #             frame.save(path, 'png')
    # img=Image.new('RGB', (height,width), 255)
    # img.paste(piece)
    # path=os.path.join(pathdir,"IMG-%s.png" % k)
    # img.save(path)

#%%


#%%


#%%
import pygame, sys

screen = pygame.display.set_mode((800,600))

clock = pygame.time.Clock()

while 1:
    screen.fill((0,0,0))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()

#%%
