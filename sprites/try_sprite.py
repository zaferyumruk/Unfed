#%%
from PIL import Image
import numpy as np
import pygame

infile = 'sprites1.png'
im = Image.open(infile).convert('RGBA')
pix = np.array(im)

#%%
# surf = pygame.surfarray.make_surface(pix)
# new_surf = pygame.pixelcopy.make_surface(pix)
notasfar = pygame.Surface((144, 192)).convert_alpha()
notasfar.fill((0, 0, 0, 0))
#%%
# pix = np.array(im)
pix.shape


#%%
pix
#%%
import pygame, sys
screen = pygame.display.set_mode((800, 600))
# surf = screen.
clock = pygame.time.Clock()

# frame = pygame.surfarray.make_surface(images[1][1][1])
running = True
while running:
    screen.fill((0, 0, 0))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # pygame.surfarray.blit_array(screen, pix)

    screen.blit(new_surf, (50, 50))
    pygame.display.update()


#%%
from PIL import Image
import os, cv2

def crop(im,height,width):
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

def cropcv(im,height,width):
    [imgwidth, imgheight, _] = im.shape
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            # box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im[j * width:(j + 1) * width, i * height:(i + 1) * height,:]
#%%
# if __name__=='__main__':
infile='sprites1.png'
pageheight=192 #48
pagewidth=144 #48
frameheight = 48
framewidth = 48
start_num=1
pathdir = 'out'
# im = cv2.imread(infile)
im = Image.open(infile)
images = {}
for charno, charpage in enumerate(crop(im, pageheight, pagewidth), start_num):
    path=os.path.join(pathdir,"IMG-%s.png" % (charno))
    # charpage.save(path, 'png')
    images[charno] = {}
    for actionno, action in enumerate(
            crop(charpage, frameheight, pagewidth), start_num):
        # path=os.path.join(pathdir,"IMG-char%s-action%s.png" % (charno,actionno))
        # action.save(path)
        images[charno][actionno] = []
        for frameno, frame in enumerate(
                crop(action, frameheight, framewidth), start_num):
            path = os.path.join(pathdir,
                                "c%sa%sf%s.png" % (charno, actionno,frameno))
            # path = os.path.join(pathdir,
            #                     "IMG-char%s-action%s-frame%s.png" % (charno, actionno,frameno))
            frame.save(path)
            images[charno][actionno].append(frame)



    #         if actionno == 1:
    #             path=os.path.join(pathdir,"IMG-char%s-action%s-frame%s.png" % (charno,actionno,frameno))
    #             frame.save(path, 'png')
    # img=Image.new('RGB', (height,width), 255)
    # img.paste(piece)
    # path=os.path.join(pathdir,"IMG-%s.png" % k)
    # img.save(path)


#%%
import numpy as np
im = Image.open(infile)
pix = np.array(im)
#%%
pix.shape
surf = pygame.surfarray.make_surface(pix)
#%%
# type(im)
images[1][1][1].shape
#%%
im = cv2.imread(infile)
print(im.shape)

# print(glob.glob('sprites1.png'))
surf = pygame.surfarray.make_surface(images[1][1][1])

#%%
import pygame
header = 'out\\'
# header = ''
frames = []
frames.append(pygame.image.load(header + "c3a1f1.png"))
frames.append(pygame.image.load(header + "c3a1f2.png"))
frames.append(pygame.image.load(header + "c3a1f3.png"))
#%%
frames[0]


#%%
frames
#%%
import pygame, sys


# def PIL2pygame(image):
#     # mode = image.mode
#     # size = image.size
#     # data = image.tobytes()
#     # return pygame.image.fromstring(data, size, mode)
#     imstr = image.convert("RGBA").tostring("raw", "RGBA")

#     return pygame.image.fromstring(data, size, mode)


screen = pygame.display.set_mode((800,600))
# surf = screen.
clock = pygame.time.Clock()
# header = 'out\\'
# header = ''
# frames = []
# frames.append(pygame.image.load(header+"c3a1f1.png"))
# frames.append(pygame.image.load(header+"c3a1f2.png"))
# frames.append(pygame.image.load(header+"c3a1f3.png"))
running = True
animupdperiod = 20
activeframe = 0
counter = 0
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    counter = counter - 1
    if counter == 0:
        screen.blit(frames[activeframe], (50, 50))
        activeframe = activeframe + 1
        counter = animupdperiod

    clock.tick(60)
    pygame.display.update()

#%%

#%%
import cv2

#%%
images[1]

#%%
images[1][1]

#%%
images[1][1][1]

#%%
images[1][1]

#%%
type(images[1][1])

#%%
images[1][1][0]

#%%
images[1][1][1]

#%%
images[1][1]

#%%
images[1][1][1]

#%%
len(images[1][1])

#%%
