from pygame import *

mask= image.load("mask/mask2.png")
running = True
while running:
    mx,my=mouse.get_pos()
    screen.blit(mask,(0,0))
    print(mask.get_at((mx,my)))
    display.flip()
    for evt in event.get():
        if evt.type == QUIT:
            running = False
