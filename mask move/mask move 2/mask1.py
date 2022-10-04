from pygame import *
screen = display.set_mode((684,513))

def drawScene(screen,x,y):
    screen.blit(maze,(0,0))
    draw.circle(screen, (255,0,0), (x,y),5)         
    display.flip()


def clear(x,y):
    if x<0 or x >= mask.get_width() or y<0 or y >= mask.get_height():
        return False
    else:
        return mask.get_at((x,y)) != WALL

def move(x,y):
    # check, on the mask, 7 pixels away in the direction they are trying to move.
    # 7, because the guy has radius 5 and they are moving 2.
    if keys[K_UP] and clear(x,y-7):
        y -= 2
    if keys[K_DOWN] and clear(x,y+7):
        y += 2
    if keys[K_LEFT] and clear(x-7,y):
        x -= 2
    if keys[K_RIGHT] and clear(x+7,y):
        x += 2

    return x,y
      
running = True
myClock = time.Clock()
mask = image.load("mask.png")
maze = image.load("maze.jpg")
WALL = (0,0,255,255)

x = 10
y = 55

while running:
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False

    keys = key.get_pressed()
    if keys[27]: break

    x,y = move(x,y)

    drawScene(screen,x,y)
                    
    display.flip()
    myClock.tick(60)                        
    
quit()
