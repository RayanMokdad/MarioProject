from pygame import *
size=width,height = 800,500
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
levelRect=Rect(305,200,178,41)

#####LEVEL CHOOSING
worldMap=image.load("worldMap.jpg")
worldMap=transform.smoothscale(worldMap,(600,500))

######## INSTRUCTION
instructionpics=image.load("Title Page/instructions.png")
instructionpic=transform.smoothscale(instructionpics,(250,300))
intructionRect=Rect(355,200,178,45)
###### MARIO
marioPic= image.load("mario/mario6.png")
marioPic=  transform.scale(marioPic,(50,70))

###### LEVEL 1
background1=image.load("level and mask/levelone.png")

######LEVEL 2

######LEVEL 3
background3=image.load("level and mask/levelthree.png")

def pics(name,start,end):
    pic = []
    for i in range(start,end+1):
        pic.append(image.load("%s/%s%d.png" % (name,name,i)))
    return pic

##mask
maskL= pics('mask',1,1)

###mario
marioPics= pics('mario',0,17)
for pic in marioPics:
    marioPics[marioPics.index(pic)]=transform.scale(marioPics[marioPics.index(pic)],(50,70))

###goomba
goombaPics = pics('goomba',0,21)
for pic in goombaPics:
    goombaPics[goombaPics.index(pic)]=transform.scale(goombaPics[goombaPics.index(pic)],(40,45))

#MARIO
VY=2
ONGROUND=3
direction = 7
still = 4
#goomba
SPEED = 2
MAX = 3
MIN = 4
#BOTH
X=0
Y=1
FRAMES = 5
CURRENT = 6

WALL = (0,0,255,255)

def menu():
    x=0
    position = 0
    mario=[250,50,0,True,True,0,0,"right"]
    running=True
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                running=False
        keys=key.get_pressed()
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        if mb[0]==1 and levelRect.collidepoint(mx,my):
            return "levels"
       
        titlepage(x,marioPics[mario[CURRENT]])
        if x ==-1200:
            x = -10
        x-=1
       
        if mario[FRAMES]>=5:
                mario[FRAMES]=0
                mario[CURRENT]+=1
        else:
            mario[FRAMES] +=1
        if mario[CURRENT]==8:
            mario[CURRENT]=0
   
        display.flip()
    return "exit"

def titlepage(x,marioPic):
    screen.blit(looppic,(x,0))
    screen.blit(logopic,(150,-100))
    screen.blit(instructionpic,(265,130))
    screen.blit(levelpic,(180,80))
    screen.blit(marioPic, (350,365))
    
    

def instruction():
    running = True
    while running:
        screen.fill((0,0,0))
        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "menu"

def levels():
    running = True
    while running:
        screen.fill((106, 154, 216, 255))#(108, 153, 218, 255))
        screen.blit(worldMap,(100,0))
        display.flip()
        #print(screen.get_at((100,100)))
        for evt in event.get():
            if evt.type == QUIT:
                return "menu"
        keys=key.get_pressed()
        if keys[K_1]:
            return "level1"
        if keys[K_3]:
            return "level3"

def level1():
    mario=[350,50,0,True,True,0,0,"right"]
    goombas=[[550,392,2,550,840,0,0],[650,260,2,650,790,0,0]]
    mask=maskL[0]
    running = True
    while running:
        drawlevelone(screen,mario,goombas)
        moveMario(mario,mask)
        moveGoomba(goombas)
        
        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "levels"
            
def drawlevelone(screen,mario,goombas):
    offset = 350 - mario[X]
    screen.blit(background1, (offset,0))
    draw.rect(screen,RED,(mario[X]+offset+5,mario[Y]+5,5,5))
    draw.rect(screen,RED,(mario[X]+offset+45,mario[Y]+5,5,5))
    draw.rect(screen,RED,(mario[X]+offset+45,mario[Y]+60,5,5))
    draw.rect(screen,RED,(mario[X]+offset+5,mario[Y]+60,5,5))
    draw.rect(screen,BLACK,(mario[X]+offset+10,mario[Y]+60,5,5))
    draw.rect(screen,BLACK,(mario[X]+offset+45,mario[Y]+60,5,5))
    
#goomba frame later
    for goomba in goombas:
        if goomba[SPEED]>0:
            screen.blit(goombaPics[goomba[CURRENT]], (goomba[X]+offset,goomba[Y]))
        else:
            screen.blit(goombaPics[goomba[CURRENT]+11], (goomba[X]+offset,goomba[Y]))#GOOMBA FINISH
    
    if mario[direction]=="left":#MARIO START
        if mario[ONGROUND]==False:
            screen.blit(marioPics[17], (350,mario[Y]))
        elif mario[still]:
            screen.blit(marioPics[8], (350,mario[Y]))
        else:
            screen.blit(marioPics[mario[CURRENT]+8], (350,mario[Y]))

    elif mario[direction]=="right":
        if mario[ONGROUND]==False:
            screen.blit(marioPics[16], (350,mario[Y]))
        elif mario[still]:
            screen.blit(marioPics[0], (350,mario[Y]))
        else:
            screen.blit(marioPics[mario[CURRENT]], (350,mario[Y]))#MARIO FINISH
    
def moveMario(mario,mask):
    keys = key.get_pressed()
    if keys[K_LEFT] and mario[X] > 375:
        mario[direction] = "left"
        mario[still] = False
        if mario[FRAMES]>=5:
                mario[FRAMES]=0
                mario[CURRENT]+=1
        else:
            mario[FRAMES] +=1
        if mario[CURRENT]==8:
            mario[CURRENT]=0
        moveleft(mario,mask)
    elif keys[K_RIGHT] and mario[X] < 7000:
        mario[direction] = "right"
        mario[still] = False
        if mario[FRAMES]>=5:
            mario[FRAMES]=0
            mario[CURRENT]+=1
        else:
            mario[FRAMES] +=1
        if mario[CURRENT]==8:
            mario[CURRENT]=0
        moveright(mario,mask)
    else:
        mario[still] = True
    if keys[K_SPACE]and mario[ONGROUND] == True:
        
        mario[VY] =-15
        mario[3] = False
        
    
    hitdown(mario,mask)

#    if mario[Y]+70 >= 435:
#        mario[Y] = 365
#        mario[VY] = 0
#        mario[3]=True

def moveleft(mario,mask):
    for i in range(7):
        if mask.get_at((mario[X]+5,int(mario[Y]+5))) != WALL\
            and mask.get_at((mario[X]+5,int(mario[Y]+60))) != WALL:
            mario[X] -= 1
            
            

def moveright(mario,mask):
    for i in range(7):
        if mask.get_at((mario[X]+45,int(mario[Y]+5))) != WALL\
            and mask.get_at((mario[X]+45,int(mario[Y])+60)) != WALL:
            mario[X]+= 1
            

def hitdown(mario,mask):
    if mario[VY] == -15:
        mario[Y] += mario[VY]
        
    if mario[Y] > 420:
        return "level1"
    if mario[Y] > 0 and mario[Y] < 420:
        if mask.get_at((mario[X]+5,int(mario[Y]+70))) != WALL\
           and mask.get_at((mario[X]+45,int(mario[Y]+70))) != WALL:
            mario[Y] += mario[VY]
            mario[VY] += 0.7
            return(-1,-1,-1)
        elif (mask.get_at((mario[X]+5,int(mario[Y]+70))) == WALL or mask.get_at((mario[X]+45,int(mario[Y]+70))) == WALL) and mario[2]>=0:
            mario[VY] = 0
            mario[3] = True
            return(-1,-1,-1)
        else:
            mario[Y] += mario[VY]
            mario[VY] += 0.7
            return(-1,-1,-1)
    elif mario[Y] <0:
        mario[Y] += mario[VY]
        mario[VY] += 0.7
    
    
def moveGoomba(goombas):
    for goomba in goombas:
        goomba[X] += goomba[SPEED]
        if goomba[X]>=goomba[MAX]:#sets barriers for goombas
            goomba[SPEED]*= -1
        if goomba[X]<=goomba[MIN]:
            goomba[SPEED]*= -1
            
        if goomba[FRAMES]>=3:
            goomba[FRAMES]=0
            goomba[CURRENT]+=1
        else:
            goomba[FRAMES] +=1
        if goomba[CURRENT]==8:
            goomba[CURRENT]=0

page="menu"
while page!= "exit":
    if page == "menu":
        page=menu()
    if page == "instruction":
        page=instruction()
    if page == "levels":
        page=levels()
    if page == "level1":
        page=level1()
    if page == "level3":
        page=level3()
quit()
