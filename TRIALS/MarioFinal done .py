from pygame import *
size=width,height = 800,500
screen=display.set_mode(size)
mask=display.set_mode(size)
RED=(255,0,0)   
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)
mario=[]
goombas=[]
deadGoombas=[]
coins=[]

#Title Page
infinityloop=image.load("Title Page/mariobackground.png")
looppic=transform.smoothscale(infinityloop,(2000,500))

#heart health
heart=image.load("heart.png")
heart=transform.smoothscale(heart,(50,50))

titleLogo=image.load("Title Page/smlogo.png")
logopic=transform.smoothscale(titleLogo,(500,350))

instructions=image.load("Title Page/instructions.jpg")
instructions=transform.smoothscale(instructions,(800,500))

#levelchoosingscreen
levelselection=image.load("Title Page/levelselection.jpg")
levelselection=transform.smoothscale(levelselection,(800,500))

level=image.load("Title Page/level.png")
levelpic=transform.smoothscale(level,(400,300))
levelRect=Rect(305,200,178,41)

levelone=image.load("Title Page/onebutton.png")
levelonepic=transform.smoothscale(levelone,(400,300))
leveloneRect=Rect(130,160,90,35)



######## INSTRUCTION
instructionpics=image.load("Title Page/instructions.png")
instructionpic=transform.smoothscale(instructionpics,(250,300))
instructionRect=Rect(299,256,195,40)

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
goombaPics = pics('goomba',0,22)
for i in range(len(goombaPics)):
    if i==22:
        goombaPics[i]=transform.scale(goombaPics[i],(40,10))
    else:
        goombaPics[i]=transform.scale(goombaPics[i],(40,45))
        
coinPic=image.load("coins.png")
coinPic=transform.smoothscale(coinPic,(40,30))


#MARIO
VY=2
ONGROUND=3
direction = 7
still = 4
hearts=8
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
    mario=[250,0,0,True,True,0,0,"right"]
    running=True
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                running=False
        keys=key.get_pressed()
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        if mb[0] ==1 and levelRect.collidepoint(mx,my):
            return "levels"
        if mb[0]==1 and instructionRect.collidepoint(mx,my):
            return "instruction"
       
        titlepage(x,marioPics[mario[CURRENT]])
        if x ==-1200:
            x = -10
        x-=1
        frames(mario)
   
        display.flip()
    return "exit"

def titlepage(x,marioPic):
    screen.blit(looppic,(x,0))
    screen.blit(logopic,(150,-100))
    screen.blit(instructionpic,(265,130))
    screen.blit(levelpic,(180,80))
    screen.blit(marioPic, (350,365))
    #draw.rect(screen,WHITE,instructionRect,5)
    
    
def instruction():
    running = True
    while running:
        screen.blit(instructions,(0,0))
        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "menu"

def levels():
    running = True
    while running:
        screen.blit(levelselection,(0,0))
        screen.blit(levelonepic,(-20,30))
        display.flip()
        keys=key.get_pressed()
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        
        for evt in event.get():
            if evt.type == QUIT:
                return "menu"
        if mb[0]==1 and leveloneRect.collidepoint(mx,my):
            return "level1"
        if keys[K_3]:
            return "level3"
def level1():
    mario=[350,30,0,True,True,0,0,"right",3]
    goombas=[[550,392,2,550,840,0,0],[650,260,2,650,790,0,0],[985,392,4,985,1225,0,0]]
    coinboxs=[(528,320,32,15)]
    coins=[[939, 329],[1273,300]]
    x = 0
    mask=maskL[0]
    running = True
    
    while running:
        if mario[hearts]==0:
            return "deadpage"
        drawlevelone(screen,mario,goombas,coins,coinboxs)
        rec = moveMario(mario,mask)
        if rec == "deadpage":
            return "deadpage"
        moveGoomba(goombas)
        
        for goomba in goombas:
            hitMario(mario,goomba)
            if jumpEnemy(mario,goomba)==True:
                goombas.remove(goomba)
                deadGoombas.append((goomba[X],goomba[Y]+35))
        for goomba in deadGoombas:
            if x>=3:
                deadGoombas.remove(goomba)
                x=0                    
            else:
                x+=.2
        if mario[X] >= 6770:
            return "levels"
            

        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "levels"


    
def deadpage():
    running = True
    while running:
        draw.rect(screen,WHITE,(0,0,800,500))
        display.flip()
        for evt in event.get():
            if evt.type==QUIT:
                return "levels"

def drawlevelone(screen,mario,goombas,coins,coinboxs):
    offset = 350 - mario[X]
    screen.blit(background1, (offset,0))
    
        
    if mario[hearts]==3:
        screen.blit(heart, (600,15))
        screen.blit(heart, (650,15))
        screen.blit(heart, (700,15))
    if mario[hearts]==2:
        screen.blit(heart, (650,15))
        screen.blit(heart, (700,15))
    if mario[hearts]==1:
        screen.blit(heart, (700,15))
        
    #draw.rect(screen,RED,(mario[X]+offset+5,mario[Y]+5,5,5))
    #draw.rect(screen,RED,(mario[X]+offset+40,mario[Y]+5,5,5))
    #draw.rect(screen,RED,(mario[X]+offset+40,mario[Y]+60,5,5))
    #draw.rect(screen,RED,(mario[X]+offset+5,mario[Y]+60,5,5))
    #draw.rect(screen,BLACK,(mario[X]+offset+10,mario[Y]+70,5,5))
    #draw.rect(screen,BLACK,(mario[X]+offset+30,mario[Y]+70,5,5))
    #draw.rect(screen,RED,(mario[X]+offset,mario[Y],50,70),5)
    #draw.rect(screen,RED,(),5)

    for coin in coins:
        screen.blit(coinPic, (coin[X]+offset,coin[Y]))
        
    for coinbox in coinboxs:
        draw.rect(screen,RED,(coinbox[X] + offset,coinbox[Y],coinbox[2],coinbox[3]))

#goomba frame later
    for goomba in goombas:
        if goomba[SPEED]>0:
            screen.blit(goombaPics[goomba[CURRENT]], (goomba[X]+offset,goomba[Y]))
        else:
            screen.blit(goombaPics[goomba[CURRENT]+11], (goomba[X]+offset,goomba[Y]))
            
    for goomba in deadGoombas:
        screen.blit(goombaPics[22], (goomba[X]+offset,goomba[Y]))

            
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
        frames(mario)
        moveleft(mario,mask)
    elif keys[K_RIGHT] and mario[X] < 7000:
        mario[direction] = "right"
        mario[still] = False
        frames(mario)
        moveright(mario,mask)
    else:
        mario[still] = True
    if keys[K_SPACE] and mario[ONGROUND] == True:
        mario[VY] =-13
        mario[ONGROUND] = False
    hitup(mario,mask)
    rec = hitdown(mario,mask)
    if rec == "deadpage":
        return "deadpage"

def frames(character):
    if character[FRAMES]>=4:
        character[FRAMES]=0
        character[CURRENT]+=1
    else:
        character[FRAMES] +=1
    if character[CURRENT]==8:
        character[CURRENT]=0

def moveleft(mario,mask):
    if mario[Y] <=0:
        mario[X] -= 7
    else:
        for i in range(7):
            if mask.get_at((mario[X]+5,int(mario[Y]+5))) != WALL\
                and mask.get_at((mario[X],int(mario[Y]+60))) != WALL:
                mario[X] -= 1

def moveright(mario,mask):
    if mario[Y] <=0:

        mario[X] +=7
    else:
        for i in range(7):
            if mask.get_at((mario[X]+40,int(mario[Y]+5))) != WALL\
                and mask.get_at((mario[X]+40,int(mario[Y])+60)) != WALL:
                mario[X]+= 1

def hitdown(mario,mask):
    if mario[VY] == -15:
        mario[Y] += mario[VY]

        #return "level1"
    if mario[Y]+ 75 >= 490:
        mario[VY] = 0
        mario[hearts] = 0
        health(mario)
        return "deadpage"
    elif mario[Y]+ 75 > 0 and mario[Y] +75 < 500:
        if mask.get_at((mario[X]+10,int(mario[Y]+75))) != WALL\
           and mask.get_at((mario[X]+30,int(mario[Y]+75))) != WALL:
            mario[Y] += mario[VY]
            mario[VY] += 0.5
            #return(-1,-1,-1)
        elif (mask.get_at((mario[X]+10,int(mario[Y]+75))) == WALL or mask.get_at((mario[X]+30,int(mario[Y]+75))) == WALL) and mario[2]>=0:
            mario[VY] = 0
            mario[ONGROUND] = True
            #return(-1,-1,-1)
        else:
            mario[Y] += mario[VY]
            mario[VY] += 0.5
            #return(-1,-1,-1)

        

def hitup(mario,mask):
    if mario[Y] <=0:
        mario[Y] += mario[VY]
        mario[VY] += 0.5
        mario[ONGROUND] = False
    elif mask.get_at((mario[X]+10,int(mario[Y]))) == WALL or mask.get_at((mario[X]+30,int(mario[Y]))) == WALL:
        if mario[VY] < 0:
            mario[VY] = 0
        mario[VY] += 0.05
        mario[Y] += 0.5

def jumpEnemy(mario,enemy):
    enemy= Rect(enemy[X],enemy[Y],40,5)
    for x in range(0,52):
        for y in range(60,70):
            if enemy.collidepoint(mario[X]+x,mario[Y]+y):
                mario[VY] =-5
                mario[ONGROUND] = False
                return True
            
def hitMario(mario,enemy):
    enemy= Rect(enemy[X],enemy[Y],40,5)
    for x in range(0,52):
        for y in range(0,55):
            if enemy.collidepoint(mario[X]+x,mario[Y]+y):
                mario[VY] =-10
                if mario[direction] == "right":
                    mario[X] = 350
                if mario[direction] == "left":
                    mario[X] = 350
                health(mario)

                    

def health(mario):
    mario[hearts]-=1
 
        #mario[hearts]=6

        
    
def moveGoomba(goombas):
    for goomba in goombas:
        goomba[X] += goomba[SPEED]
        if goomba[X]>=goomba[MAX]:#sets barriers for goombas
            goomba[SPEED]*= -1
        if goomba[X]<=goomba[MIN]:
            goomba[SPEED]*= -1
        frames(goomba)


    

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
    if page == "deadpage":
        page=deadpage()
quit()
