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

def processSprites(infile='sprites\\sprites1.png',outdir = 'sprites\\characters\\', startingcharno=0):
    pageheight=192 #48
    pagewidth=144 #48
    frameheight = 48
    framewidth = 48
    start_num=0
    pathdir = outdir
    # im = cv2.imread(infile)
    im = Image.open(infile)
    images = {}
    for charno, charpage in enumerate(
            crop(im, pageheight, pagewidth), startingcharno):
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
                # images[charno][actionno].append(frame)


processSprites(infile='sprites\\sprites1.png', startingcharno=0)
processSprites(infile='sprites\\sprites2.png', startingcharno=8)