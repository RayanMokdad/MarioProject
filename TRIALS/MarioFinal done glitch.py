from pygame import *
size=width,height = 800,500
screen=display.set_mode(size)
mask=display.set_mode(size)
RED=(255,0,0)   
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)

#######################################################
                    #####variable######
###empty list
mario=[]
goombas=[]
deadGoombas=[]
koopas=[]
deadKoopas=[]
coins=[]

#MARIO
VY=2
ONGROUND=3
direction = 5
still = 4
hearts=6

#Goomba
SPEED = 2
MAX = 3
MIN = 4

#universal
X=0
Y=1
frame=0
DELAY=5

#mask
WALL = (0,0,255,255)

########################################################
        ####loading / transforming pictures ####
#Title Page
infinityloop=image.load("Title Page/mariobackground.png")
looppic=transform.smoothscale(infinityloop,(2000,500))

titleLogo=image.load("Title Page/smlogo.png")
logopic=transform.smoothscale(titleLogo,(500,350))

#level options

levelselection=image.load("Title Page/levelselection.jpg")  
levelselection=transform.smoothscale(levelselection,(800,500))

level=image.load("Title Page/level.png")
levelpic=transform.smoothscale(level,(400,300))
levelRect=Rect(305,200,178,41)

levelone=image.load("Title Page/onebutton.png")
levelonepic=transform.smoothscale(levelone,(400,300))
leveloneRect=Rect(130,160,90,35)

######## INSTRUCTION
instructions=image.load("Title Page/instructions.jpg")
instructions=transform.smoothscale(instructions,(800,500))

instructionpics=image.load("Title Page/instructions.png")
instructionpic=transform.smoothscale(instructionpics,(250,300))
instructionRect=Rect(299,256,195,40)

###DEAD PAGE
deadpic=image.load("dead.png")
deadpic=transform.smoothscale(deadpic,(800,600))
#LEVELS
background1=image.load("level and mask/levelone.png")

background3=image.load("level and mask/levelthree.png")

#heart health
heart=image.load("heart.png")
heart=transform.smoothscale(heart,(50,50))

#coins
coinPic=image.load("coins.png")
coinPic=transform.smoothscale(coinPic,(40,30))

#brick
brickPic = image.load("brick.png")
brickPic = transform.scale(brickPic,(34,32))

#####function that load a group of pictures
def pics(name,start,end):
    pic = []
    for i in range(start,end+1):
        pic.append(image.load("%s/%s%d.png" % (name,name,i)))
    return pic

##mask
maskL= pics('mask',1,1)

###mario
marioPics= pics('mario',0,9)
for i in range (len(marioPics)):
    marioPics[i]=transform.scale(marioPics[i],(50,70))

###goomba
goombaPics = pics('goomba',0,11)
for i in range(len(goombaPics)):
    if i==11:
        goombaPics[i]=transform.scale(goombaPics[i],(40,10))
    else:
        goombaPics[i]=transform.scale(goombaPics[i],(40,45))
###Koopa
koopaPics= pics('koopa',0,3)
for i in range (len(koopaPics)):
    koopaPics[i]=transform.scale(koopaPics[i],(45,60))

###koopashells
deadkoopaPics= pics('koopashell',0,3)
for i in range (len(deadkoopaPics)):
    deadkoopaPics[i]=transform.scale(deadkoopaPics[i],(40,35))
        

        
'''
This is where the game starts
'''

def menu():
    x=0
    position = 0
    mario=[250,0,0,True,True,"right"] #for the loading screen where mario is running 
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
       
        titlepage(x,marioPics)
        if x ==-1200: #checking where the background is currently blitting there is a problem with this
            x = -10
        x-=1
    
        display.flip()
    return "exit"

def titlepage(x,marioPic):  ###this is where all the bliting in menu happens
    global frame
    screen.blit(looppic,(x,0))
    screen.blit(logopic,(150,-100))
    screen.blit(instructionpic,(265,130))
    screen.blit(levelpic,(180,80))
    frame+=1
    f = int(frame) // DELAY % (len(marioPics)-2)
    screen.blit(marioPics[f], (350,365))
    
    
def instruction(): #the instruction manual
    running = True
    while running:
        screen.blit(instructions,(0,0))
        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "menu"

def levels(): #level choosing page
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
    global frame
    mario=[350,200,0,True,True,"right",3] #the positions specifically for level one
    goombas=[[550,392,3,550,840],[650,260,2,650,790],[1336,392,3,1336,1492],
             [2370,392,5,2370,2810],[3330,392,3,3330,3980],[5500,392,3,5500,5920]]
    
    koopas=[[985,380,4,985,1225],[1590,380,3,1590,1860],[2665,115,3,2665,2895],
            [3630,380,4,3330,4420],[5600,245,4,5600,5700]]
    
    coins=[[940, 330],[1273,295],[1540,265],[1600,235],[1655,200],[1725,165],
           [1795,200],[1850,235],[1910,265],[2720,75],[2770,75],[2820,75],[3130,267],
           [4040,120],[4090,120],[4315,260],[4615,385],[5055,261],[5110,220],[5165,260],
           [5450,320],[5980,320],[6282,121]]
    coinRects=[Rect(coins[i][0],coins[i][1],40,30) for i in range(len(coins))]

    mask=maskL[0]
    coinboxs=[[530,320],[695,320],[765,320],[730,185],[2600,320],
              [3135,185],[3537,320],[3635,320],[3735,320],[3635,185],
              [4303,185],[4337,185],[5673,320]]
    coincount = []
    running = True
    x=0
    kx=0
    flagRect=Rect(6600,80,20,450)
    gamelock = "OFF"
    times =""
    brick= []
    while running:
        offset = 350 -mario[X]
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        if mb[0] == 1:
            print(mx-offset,my)
        frame+=1
        if mario[hearts]==0:
            return "deadpage"
        drawlevelone(screen,mario,goombas,koopas,coinRects,coinboxs,brick)
        rec = moveMario(mario,mask,gamelock)
        if rec == "deadpage":
            return "deadpage"

        
        for goomba in goombas:
            moveEnemy(goomba)
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

                
        for koopa in koopas:
            hitMario(mario,koopa)
            moveEnemy(koopa)
            if jumpEnemy(mario,koopa)==True:
                koopas.remove(koopa)
                deadKoopas.append(koopa)
                #hitonce = False

        for deadkoopa in deadKoopas:
            moveEnemy(deadkoopa)
            hitMario(mario,deadkoopa)
            if kx>=30:
                deadKoopas.remove(deadkoopa)
                kx=0                
            else:
                kx+=.1
                
            if kx>=5:
                if jumpEnemy(mario,deadkoopa)==True:
                    deadkoopa[SPEED]=0  
            else:
                kx+=.1

        if mario[X] >= 6770:
            return "levels"
        

        marioRect=Rect(mario[X],mario[Y],50,70)
        offset = 350 - mario[X]
        hitbox=Rect(mario[X]+15,mario[Y],20,5)
        
        if flagRect.colliderect(marioRect):
            if times != "once":
                mario[X] = 6590
            times = "once"
            gamelock = "ON"
        for coinbox in coinboxs:
            t=coinbox
            coinbox=Rect(coinbox[X],coinbox[Y],27,15)
#            draw.rect(screen,RED,(mario[X]+15+offset,mario[Y],20,5))
            if coinbox.colliderect(hitbox):
                coinRects.append(Rect(coinbox[X]-5,coinbox[Y]-55,40,30))
                brick.append((coinbox[X]-3,coinbox[Y]-18))
                coinboxs.remove(t)
                break
        
        
        for coin in coinRects:
            if coin.colliderect(marioRect):
                coincount.append(coin)
                coinRects.remove(coin)
                break

        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "levels"

def deadpage():
    running = True
    while running:
        screen.blit(deadpic,(0,-50))
        display.flip()
        for evt in event.get():
            if evt.type==QUIT:
                return "levels"

def drawlevelone(screen,mario,goombas,koopas,coinRects,coinboxs,brick):
    offset = 350 - mario[X]
    screen.blit(background1, (offset,0))
    
    draw.rect(screen,RED,(6610+offset,80,20,450),4)
    if mario[hearts]==3:
        screen.blit(heart, (600,15))
        screen.blit(heart, (650,15))
        screen.blit(heart, (700,15))
    if mario[hearts]==2:
        screen.blit(heart, (650,15))
        screen.blit(heart, (700,15))
    if mario[hearts]==1:
        screen.blit(heart, (700,15))

#    draw.rect(screen,RED,(mario[X]+offset,mario[Y],5,5))
#    draw.rect(screen,RED,(mario[X]+offset+30,mario[Y],5,5))
#    draw.rect(screen,RED,(mario[X]+offset+30,mario[Y]+60,5,5))
#    draw.rect(screen,RED,(mario[X]+offset,mario[Y]+60,5,5))
#    draw.rect(screen,BLACK,(mario[X]+offset+7,mario[Y]+65,5,5))
#    draw.rect(screen,BLACK,(mario[X]+offset+23,mario[Y]+65,5,5))
    #draw.rect(screen,RED,(mario[X]+offset,mario[Y],50,65),5)
    #draw.rect(screen,RED,(),5)
        
    for c in coinRects:
        screen.blit(coinPic, (c[X]+offset,c[Y]))


#    for coinbox in coinboxs:
#        t=Rect(coinbox[X]+offset,coinbox[Y],27,15)
#        draw.rect(screen,RED,t)
    for b in brick:
        screen.blit(brickPic,(b[0]+offset,b[1]))
###Goomba
    f = frame // DELAY % (len(goombaPics)-1)
    for goomba in goombas:
        if goomba[SPEED]>0:
            screen.blit(goombaPics[f], (goomba[X]+offset,goomba[Y]))
        else:
            screen.blit((transform.flip(goombaPics[f],True,False)), (goomba[X]+offset,goomba[Y]))
            
    for goomba in deadGoombas:
        screen.blit(goombaPics[11], (goomba[X]+offset,goomba[Y]))
        
###Koopa
    f = frame // DELAY % len(koopaPics)
    for koopa in koopas:
        if koopa[SPEED]>0:
            screen.blit(koopaPics[f], (koopa[X]+offset,koopa[Y]))
        else:
            screen.blit((transform.flip(koopaPics[f],True,False)), (koopa[X]+offset,koopa[Y]))

    f = frame // 3 % len(deadkoopaPics)
    for koopa in deadKoopas:
        screen.blit(deadkoopaPics[f], (koopa[X]+offset,koopa[Y]+20))
        
###Mario
    f = frame // DELAY % (len(marioPics)-2)
    if mario[direction]=="left":#MARIO START
        if mario[ONGROUND]==False:
            screen.blit(marioPics[9], (350,mario[Y]))
        elif mario[still]:
            screen.blit((transform.flip(marioPics[0],True,False)), (350,mario[Y]))
        else:
            screen.blit((transform.flip(marioPics[f],True,False)), (350,mario[Y]))

    elif mario[direction]=="right":
        if mario[ONGROUND]==False:
            screen.blit(marioPics[8], (350,mario[Y]))
        elif mario[still]:
            screen.blit(marioPics[0], (350,mario[Y]))
        else:
            screen.blit(marioPics[f], (350,mario[Y]))#MARIO FINISH

    
    
def moveMario(mario,mask,gamelock):

    keys = key.get_pressed()
    if keys[K_LEFT] and mario[X] > 375 and gamelock =="OFF":
        mario[direction] = "left"
        mario[still] = False
        
        moveleft(mario,mask)
    elif keys[K_RIGHT] and mario[X] < 7000 and gamelock == "OFF":
        mario[direction] = "right"
        mario[still] = False
        
        moveright(mario,mask)
    else:
        mario[still] = True
    if keys[K_SPACE] and mario[ONGROUND] == True and gamelock == "OFF":
        mario[VY] =-14
        mario[ONGROUND] = False
    hitup(mario,mask)
    rec = hitdown(mario,mask,gamelock)

    if rec == "deadpage":
        return "deadpage"


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

def hitdown(mario,mask,gamelock):
    if gamelock == "OFF":
        if mario[VY] == -14:
            mario[Y] += mario[VY]
            #return "level1"
        if mario[Y]+ 75 >= 490:
            mario[VY] = 0
            mario[hearts] = 0
            #health(mario)
            return "deadpage"
        elif mario[Y]+ 75 > 0 and mario[Y] +75 < 500:
            if mask.get_at((mario[X]+10,int(mario[Y]+75))) != WALL\
               and mask.get_at((mario[X]+30,int(mario[Y]+75))) != WALL:
                mario[Y] += mario[VY]
                mario[VY] += 0.7
                #return(-1,-1,-1)
            elif (mask.get_at((mario[X]+10,int(mario[Y]+75))) == WALL or mask.get_at((mario[X]+30,int(mario[Y]+75))) == WALL) and mario[2]>=0:
                mario[VY] = 0
                mario[ONGROUND] = True
                #return(-1,-1,-1)
        else:
            mario[Y] += mario[VY]
            mario[VY] += 0.7
            #return(-1,-1,-1)
    elif gamelock =="ON" and mask.get_at((mario[X]+10,int(mario[Y]+75))) != WALL\
        and mask.get_at((mario[X]+30,int(mario[Y]+75))) != WALL:
        if mario[VY] >0:
            mario[VY] == 0
        mario[VY] = -5
        mario[Y] -= mario[VY]
        
    else:
        #gamelock =="ON" and mask.get_at((mario[X]+10,int(mario[Y]+75))) == WALL\
        #and mask.get_at((mario[X]+30,int(mario[Y]+75))) == WALL:
        mario[X] += 7


def hitup(mario,mask):
    if mario[Y] <=0:
        mario[Y] += mario[VY]
        mario[VY] += 0.5
        mario[ONGROUND] = False
    elif mask.get_at((mario[X]+10,int(mario[Y]))) == WALL or mask.get_at((mario[X]+30,int(mario[Y]))) == WALL:
        if mario[VY] < 0:
            mario[VY] = 0
        mario[VY] += 0.05
        mario[Y] += mario[VY]

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
                mario[hearts]-=1


def moveEnemy(enemy):
    enemy[X] += enemy[SPEED]
    if enemy[X]>=enemy[MAX]:#sets barriers for goombas
        enemy[SPEED]*= -1
    if enemy[X]<=enemy[MIN]:
        enemy[SPEED]*= -1


    

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
