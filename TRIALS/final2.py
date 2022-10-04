from pygame import *

size = width, height = 800, 500
screen = display.set_mode(size)
myClock = time.Clock()


backPic = image.load("mariolevel1.png")#level 1
#image.load("final/mariolevel2.png")#level 2
#image.load("final/mariolevel3.png")#level 3



marioPic= image.load("mario/mario6.png")
marioPic=  transform.scale(marioPic,(50,70))
mask = image.load("mask2.png")

WALL = (0,0,255,255)

def drawScene(screen,mario,goombas):
    global direction, still
    offset = 375 - mario[X]
    screen.blit(backPic, (offset,0))
    for goomba in goombas:
        if goomba[FRAMES]>=3:#GOOMBA START
            goomba[FRAMES]=0
            goomba[CURRENT]+=1
        else:
            goomba[FRAMES] +=1
        if goomba[CURRENT] ==10:
            goomba[CURRENT]=0

        if goomba[DIR]>0:
            screen.blit(goombaPics[goomba[CURRENT]], (goomba[X]+offset,goomba[Y]))
        else:
            screen.blit(goombaPics[goomba[CURRENT]+11], (goomba[X]+offset,goomba[Y]))#GOOMBA FINISH
            
        
    if direction=="left":#MARIO START
        if mario[ONGROUND]==False:
            screen.blit(marioPics[17], (350,mario[Y]))
        elif still:
            screen.blit(marioPics[8], (350,mario[Y]))            
        else:
            screen.blit(marioPics[mario[CURRENT]+8], (350,mario[Y]))
       

    elif direction=="right":
        
        if mario[ONGROUND]==False:
            screen.blit(marioPics[16], (350,mario[Y]))
        elif still:
            screen.blit(marioPics[0], (350,mario[Y]))
        else:
            screen.blit(marioPics[mario[CURRENT]], (350,mario[Y]))#MARIO FINISH



def moveMario(mario):
    global direction, still
    keys = key.get_pressed()
    
    if keys[K_LEFT] and mario[X] > 375:
        mario[X] -= 5
        direction= "left"
        if mario[FRAMES]>=3:
            mario[FRAMES]=0
            mario[CURRENT]+=1
        else:
            mario[FRAMES] +=1
        if mario[CURRENT]==8:
            mario[CURRENT]=0
        still=False
        
    elif keys[K_RIGHT] and mario[X] < 7000:
        mario[X] += 6
        direction= "right"
        if mario[FRAMES]>=3:
            mario[FRAMES]=0
            mario[CURRENT]+=1
        else:
            mario[FRAMES] +=1
        if mario[CURRENT]==8:
            mario[CURRENT]=0
        still=False
        
    else:
        still=True

    if keys[K_UP] and mario[ONGROUND]:
        mario[VY]=-12
        mario[ONGROUND]=False

    mario[Y]+=mario[VY]
    if mario[Y]>365:
        mario[Y]=365
        mario[VY]=0
        mario[ONGROUND]=True
    mario[VY]+=.5

    #if mario[Y]<340: #COLLIDING WITH BLOCKS
        #mario[VY]+=20
        
         
         
        
def moveGoomba(goombas):
    for goomba in goombas:
        goomba[X] += goomba[DIR]
        if goomba[X]<=goomba[RIGHT]:#sets barriers for goombas
            goomba[DIR]*= -1
        if goomba[X]>=goomba[LEFT]:
            goomba[DIR]*= -1

        
def pics(file,name,start,end):
    pic = []
    for i in range(start,end+1):
        pic.append(image.load("%s/%s/%s%d.png" % (file,name,name,i)))
    return pic


goombaPics = pics('final','goomba',0,21)
for pic in goombaPics:
    goombaPics[goombaPics.index(pic)]=transform.scale(goombaPics[goombaPics.index(pic)],(40,45))

marioPics= pics('final','mario',0,17)
for pic in marioPics:
    marioPics[marioPics.index(pic)]=transform.scale(marioPics[marioPics.index(pic)],(50,70))

still=True
direction="right"
X=0
Y=1
VY=2
ONGROUND=3
DIR = 2
LEFT = 3
RIGHT = 4
FRAMES=5
CURRENT=6
mario=[375,365,0,True,0,0,0]
goomba=[[550,392,2,550,1050,0,0],[650,260,2,650,790,0,0]]



running = True 
while running:
    for evnt in event.get():               
        if evnt.type == QUIT:
            running = False
    
    drawScene(screen,mario,goomba)
    moveMario(mario)
    moveGoomba(goomba)
  
    
        
    display.flip()
    time.wait(1)
quit()
