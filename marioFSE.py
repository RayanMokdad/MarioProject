from pygame import *
size=width,height=800,500
screen=display.set_mode(size)
RED=(255,0,0)   
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)


#Title Page
infinityloop=image.load("Title Page/mariobackground.png")
looppic=transform.smoothscale(infinityloop,(2000,500))

titleLogo=image.load("Title Page/smlogo.png")
logopic=transform.smoothscale(titleLogo,(500,350))

level=image.load("Title Page/level.png")
levelpic=transform.smoothscale(level,(400,300))
######## INSTRUCTION
instructionpics=image.load("Title Page/instructions.png")
instructionpic=transform.smoothscale(instructionpics,(250,300))


worldonemap=image.load("Game/world1.png")
worldonemappic=transform.smoothscale(worldonemap,(1800,500))

level2=image.load("Game/1-3.png")
level2pic=transform.smoothscale(level2,(3000,400))

###### MARIO
marioPic= image.load("mario/mario6.png")
marioPic=  transform.scale(marioPic,(50,70))

###### LEVEL 1
background1=image.load("level and mask/levelone.png")

######LEVEL 2

######LEVEL 3
background3=image.load("level and mask/levelthree.png")

####mask
maskL=[]

for x in range(1,2):
    masks=image.load("level and mask/mask%d.png" % x)
    maskL.append(masks)


marioL=[]

def pics(name,start,end):
    pic = []
    for i in range(start,end+1):
        pic.append(image.load("%s/%s%d.png" % (name,name,i)))
    return pic

###mario
marioPics= pics('mario',0,17)
for pic in marioPics:
    marioPics[marioPics.index(pic)]=transform.scale(marioPics[marioPics.index(pic)],(50,70))

###goomba
goombaPics = pics('goomba',0,21)
for pic in goombaPics:
    goombaPics[goombaPics.index(pic)]=transform.scale(goombaPics[goombaPics.index(pic)],(40,45))

#collidpoint rect
instructionRect=Rect(300,260,195,35)



def menu():
    x=0
    position = 0
    running=True
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                running=False
        keys=key.get_pressed()
        if keys[K_RETURN]:
            return "maingame"
        

        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        if mb[0]==1 and instructionRect.collidepoint(mx,my):
            return "instruction"
        if round(position) == 7:
            position = 0 
        titlepage(x,mb,round(position))
        if x ==-1200:
            x = -10
        x-=1
        position += 0.2

        
        



    
        display.flip()
    return "exit"

def titlepage(x,mb,position):
    screen.blit(looppic,(x,0))
    screen.blit(logopic,(150,-100))
    screen.blit(instructionpic,(265,130))
    screen.blit(levelpic,(180,80))
    screen.blit(marioPics[position], (300,380))
    
    display.flip()
    
def instruction():
    running = True
    while running:
        screen.fill((0,0,0))
        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "menu"

def maingame():
    running = True
    while running:
        screen.blit(worldonemappic,(0,0))
        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "menu"
        keys=key.get_pressed()
        if keys[K_1]:
            return "level1"
        if keys[K_3]:
            return "level3"


def level1():
    global maskL
    mask=maskL[0]
    #MARIO
    VY=2
    ONGROUND=3
    direction = "right"
    still = 4
    #goomba
    SPEEDGoomba = 2
    MAX = 3
    MIN = 4
    #BOTH
    X=0
    Y=1
    FRAMES = 5
    CURRENT = 6
    mario=[250,50,0,True,True,0,0]
    goomba=[[550,392,2,550,1050,0,0],[650,260,2,650,790,0,0]]
    WALL = (0,0,255,255)
    running = True
    while running:
        drawscenemain(screen,mario)
        moveMario(mario,X,Y,VY,WALL,mario)
        mx,my=mouse.get_pos()
        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "maingame"   
            


def level3():
    global maskL
    #MARIO
    VY=2
    ONGROUND=3
    direction = "right"
    still = 4
    #goomba
    SPEEDGoomba = 2
    MAX = 3
    MIN = 4
    #BOTH
    X=0
    Y=1
    FRAMES = 5
    CURRENT = 6
    mario=[250,50,0,True,True,0,0]
    goomba=[[550,392,2,550,1050,0,0],[650,260,2,650,790,0,0]]
    WALL = (0,0,255,255)
    running = True
    while running:
        drawscenemain(screen,mario)
        moveMario(mario,X,Y,VY,WALL,vy)
        mx,my=mouse.get_pos()
        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "maingame"   
            
def drawscenemain(screen,mario):
    offset = 350 - mario[0]

    screen.blit(background1, (offset,0))
    screen.blit(marioPic, (350,mario[1]))
    #moveGoomba(goomba)
    draw.rect(screen,RED,(mario[0]+offset,mario[1]+5,5,5))
    draw.rect(screen,RED,(mario[0]+offset+50,mario[1]+5,5,5))
    draw.rect(screen,RED,(mario[0]+offset+50,mario[1]+60,5,5))
    draw.rect(screen,RED,(mario[0]+offset,mario[1]+60,5,5))
    draw.rect(screen,BLACK,(mario[0]+offset+5,mario[1]+70,5,5))
    draw.rect(screen,BLACK,(mario[0]+offset+45,mario[1]+70,5,5))

def hitdown(mario,WALL,VY,X,Y):
    global maskL
    mask=maskL[0]
    if mario[VY] == -15:
        mario[Y] += mario[VY]
    if mask.get_at((mario[X]+5,int(mario[Y]+70))) != WALL\
       and mask.get_at((mario[X]+45,int(mario[Y]+70))) != WALL:
        mario[Y] += mario[VY]
        mario[VY] += 0.7
        return(-1,-1,-1)
    elif (mask.get_at((mario[X],int(mario[Y]+70))) == WALL or mask.get_at((mario[X]+50,int(mario[Y]+70))) == WALL) and mario[2]>=0:
        mario[VY] = 0
        mario[3] = True
        return(-1,-1,-1)
    else:
        mario[Y] += mario[VY]
        mario[VY] += 0.7
        return(-1,-1,-1)
def moveright(mario,X,Y,WALL):
    for i in range(7):
        if mask.get_at((mario[X]+50,int(mario[Y]+5))) != WALL\
            and mask.get_at((mario[X]+50,int(mario[Y])+60)) != WALL:
            mario[X]+= 1
def moveleft(mario,X,Y,WALL):
    for i in range(7):
        if mask.get_at((mario[X],int(mario[Y]+5))) != WALL\
            and mask.get_at((mario[X],int(mario[Y]+60))) != WALL:
            mario[X] -= 1
        
def moveMario(mario,X,Y,VY,WALL):
    keys = key.get_pressed()
    if keys[K_LEFT] and mario[X] > 375:
        moveleft(mario,X,Y,WALL)
    if keys[K_RIGHT] and mario[X] < 7000:
        moveright(mario,X,Y,WALL)
    if keys[K_SPACE]and mario[3] == True:
        
        mario[VY] =-15
        mario[3] = False
        
    
    hitdown(mario,WALL,VY,X,Y)

    if mario[Y]+70 >= 435:
        mario[Y] = 365
        mario[VY] = 0
        mario[3]=True


    return mario[X],mario[Y]

def moveGoomba(goombas):
    for goomba in goombas:
        goomba[X] += goomba[DIR]
        if goomba[X]<=goomba[RIGHT]:#sets barriers for goombas
            goomba[DIR]*= -1
        if goomba[X]>=goomba[LEFT]:
            goomba[DIR]*= -1



page="menu"
while page!= "exit":
    if page == "menu":
        page=menu()
    if page == "instruction":
        page=instruction()
    if page == "maingame":
        page=maingame()
    if page == "level1":
        page=level1()
    if page == "level3":
        page=level3()
quit()
