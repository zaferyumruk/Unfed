import pygame
header = 'sprites\\out\\'
# header = ''
frames = []
frames.append(pygame.image.load(header + "c3a2f1.png"))
frames.append(pygame.image.load(header + "c3a2f2.png"))
frames.append(pygame.image.load(header + "c3a2f3.png"))

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
animupdperiod = 5
seqidx = 0
counter = animupdperiod
seq2frame = [0, 1, 2, 1]
activeframe = 0
while running:
    screen.fill((0, 0, 0))
    screen.blit(frames[activeframe], (50, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    counter = counter - 1
    if counter == 0:
        seqidx = (seqidx + 1) % len(seq2frame)
        activeframe = seq2frame[seqidx]
        counter = animupdperiod

    clock.tick(60)
    pygame.display.update()

