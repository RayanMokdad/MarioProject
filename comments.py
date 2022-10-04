from pygame import *
from math import *
size=width,height = 800,500
screen=display.set_mode(size)
mask=display.set_mode(size)
font.init()
fnt = font.Font("arcade.ttf",40)
init()


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
HEARTS=6

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
WALL=(0,0,255,255)

########################################################
        ####loading / transforming pictures ####
#Title Page
looppic=image.load("Title Page/mariobackground.png")

logopic=image.load("Title Page/smlogo.png")

#level options

levelselection=image.load("Title Page/levelselection.jpg")  

levelpic=image.load("Title Page/level.png")
levelRect=Rect(305,200,178,41)

levelonepic=image.load("Title Page/onebutton.png")
leveloneRect=Rect(130,160,90,35)

leveltwopic = image.load("Title Page/twobutton.png")
leveltwoRect = Rect(550,160,90,35)

leveloneshot=image.load("Title Page/leveloneshot.png")
leveltwoshot=image.load("Title Page/leveltwoshot.png")

difficulty=image.load("Title Page/difficulty.png")
difficultypic= transform.smoothscale(difficulty,(600,600))

######## INSTRUCTION
instructions=image.load("Title Page/instructions.jpg")

instructionpic=image.load("Title Page/instructions.png")


###DEAD PAGE
deadpic=image.load("dead.png")
deadpic=transform.smoothscale(deadpic,(800,500))

#LEVELS
background1=image.load("level and mask/levelone.png")

background2=image.load("level and mask/leveltwo.png")

#heart health
heart=image.load("heart.png")

#coins
coinPic=image.load("coins.png")

#brick
brickPic = image.load("brick.png")

#back
backPic = image.load("back.png")
backPic = transform.scale(backPic,(70,60))
backRect= Rect(10,20,70,60)

#####function that load a group of pictures
def pics(name,start,end):
    pic = []
    for i in range(start,end+1):
        pic.append(image.load("%s/%s%d.png" % (name,name,i)))
    return pic

##mask
maskL= pics('mask',1,2)

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

####sounds
coineffect=mixer.Sound("sounds/coin.wav") #
flagpoleeffect=mixer.Sound("sounds/flagpole.wav") #
jumpeffect=mixer.Sound("sounds/jump.wav") #
stompeffect=mixer.Sound("sounds/stomp.wav") #
deatheffect=mixer.Sound("sounds/death.wav") #
mixer.music.load("sounds/Theme.mp3")
mixer.music.play(-1)
#mixer.Sound.get_volume()
        
'''
This is where the game starts
'''

def menu():
    x=0
    position = 0
    instructionRect=Rect(299,316,195,40)
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
            return "levels" #takes us to level 
        if mb[0]==1 and instructionRect.collidepoint(mx,my):
            return "instruction" #takes us to instruction
       
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
    screen.blit(instructionpic,(265,190))
    screen.blit(levelpic,(180,80))
    frame+=1
    f = int(frame) // DELAY % (len(marioPics)-2) #ILL COMMENT THAT ITS REALLY CONFUSING
    screen.blit(marioPics[f], (350,365))

    
def instruction(): #the instruction manule
    running = True
    while running:
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        
        screen.blit(instructions,(0,0))
        screen.blit(backPic,(10,20))
        display.flip()
        if mb[0] == 1 and backRect.collidepoint(mx,my):
            return "menu"
        for evt in event.get():
            if evt.type == QUIT:
                return "menu"

def levels(): #level choosing page
    running = True
    while running:
        screen.blit(levelselection,(0,0))
        screen.blit(levelonepic,(-20,30))
        screen.blit(leveltwopic,(450,30))
        screen.blit(leveloneshot,(20,250))
        screen.blit(leveltwoshot,(440,250))
        screen.blit(backPic,(10,20))
        display.flip()
        keys=key.get_pressed()
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        
        for evt in event.get():
            if evt.type == QUIT:
                return "menu"
        if mb[0]== 1:
            if backRect.collidepoint(mx,my):
                return "menu"
            elif leveloneRect.collidepoint(mx,my):
                return "level1"
            elif leveltwoRect.collidepoint(mx,my):
                return "level2"


def level1():
    global frame
    #OUR VARIABLE THAT WE NEED THEM TO CHANGE
    once = False
    mario=[350,250,0,True,True,"right",5] #the positions specifically for level one
    #X,Y,SPEED,MAX,MIN
    goombas=[[550,392,3,550,840],[650,260,2,650,790],[1336,392,3,1336,1492],
             [2370,392,5,2370,2810],[3330,392,3,3330,3980],[5500,392,3,5500,5920]]
    
    koopas=[[985,380,4,985,1225],[1590,380,3,1590,1860],[2665,115,3,2665,2895],
            [3630,380,4,3330,4420],[5600,245,4,5600,5700]]
    
    coins=[[940, 330],[1273,295],[1540,265],[1600,235],[1655,200],[1725,165],
           [1795,200],[1850,235],[1910,265],[2720,75],[2770,75],[2820,75],[3130,267],
           [4040,120],[4090,120],[4315,260],[4615,385],[5055,261],[5110,220],[5165,260],
           [5450,320],[5980,320],[6282,121]]
    #TO MAKE THESE COINS INTO RECT
    coinRects=[Rect(coins[i][0],coins[i][1],40,30) for i in range(len(coins))]
    #THIS MASK IS FOR LEVEL ONE
    mask=maskL[0]
    #PLACES WHERE MARIO HITS THE BRICKS TO GET COINS
    coinboxs=[[530,320],[695,320],[765,320],[730,185],[2600,320],
              [3135,185],[3537,320],[3635,320],[3735,320],[3635,185],
              [4303,185],[4337,185],[5673,320]]
    score=0
    #GOOMBA DEAD TIMER
    x=0
    #KOOPA DEAD TIMER
    kx=0
    #WHERE MARIO IS HITTING THE END
    flagRect=Rect(6600,80,20,450)
    #LOCKING PLAYERS CONTROLS
    gamelock = "OFF"
    times =""
    #LIST TO BLIT BRICKS
    brick= []
    #THIS ALLOWS THE USER CHOOSE LEVEL DIFFICULTY
    rec= difficulty()
    if rec == "levels":
        return "levels"
    mario[HEARTS] = rec


    running = True
    while running:
        offset = 350 -mario[X]
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        if mb[0] == 1:
            print(mx-offset,my)
        #CONSTANTLY INCREASING BY ONE SO THE ANIMATION WILL CHANGE ACCORDING TO THIS
        frame+=1
        if mario[HEARTS]==0:
            return "deadpage"
        #GOES TO THE DRAWING FUNCTION
        drawlevelone(screen,mario,goombas,koopas,coinRects,coinboxs,brick,score)
        #CONSTATLY CHECKING MARIO'S MOVEMENT
        rec = moveMario(mario,mask,gamelock,once)
        if rec == "deadpage":
            return "deadpage"

        
        for goomba in goombas:
            moveEnemy(goomba)
            hitMario(mario,goomba)
            if jumpEnemy(mario,goomba)==True:#IF MARIO HITS GOOMBA
                goombas.remove(goomba) #TAKES GOOMBA OUT OF THE LIST
                deadGoombas.append((goomba[X],goomba[Y]+35)) #ADD IT TO THE DEAD LIST
        for goomba in deadGoombas: #THIS CREATES THE LITTLE ANIMATION OF GOOMBA DEAD
            #ON THE GROUND (FLAT)
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

        for deadkoopa in deadKoopas:
            moveEnemy(deadkoopa)
            hitMario(mario,deadkoopa)
            if kx>=40:
                deadKoopas.remove(deadkoopa)
                kx=0                
            else:
                kx+=.1
                
            if kx>=3:
                if jumpEnemy(mario,deadkoopa)==True:
                    deadkoopa[SPEED]=0  
            else:
                kx+=.1

        if mario[X] >= 6770:
            return "levels"
        
        #THIS MARIO RECT CHECKS IF MARIO IS HITTING ANY OF THE BRICKS THAT CONTAINS COINS
        marioRect=Rect(mario[X],mario[Y],50,70) 
        hitbox=Rect(mario[X]+15,mario[Y],20,5)
        
        if flagRect.colliderect(marioRect):
            if times != "once": #THIS LIMITS THE TIMES TO ONE SO THE
                #CODE WONT KEEP ON GOING OVER AND KEEP MARIO AT 6590
                mario[X] = 6590
                once = True
            times = "once"
            gamelock = "ON"
            
        for coinbox in coinboxs:
            t=coinbox #there was an error if we just did coinbox
            coinbox=Rect(coinbox[X],coinbox[Y],27,15) #make our coinbox a rect
            if coinbox.colliderect(hitbox): #if mario hits our rec than
                #append it to the coin list with all the other coin
                coinRects.append(Rect(coinbox[X]-5,coinbox[Y]-55,40,30))
                #append it to this list so we can blit the bricks over the
                #question mark bricks
                brick.append((coinbox[X]-3,coinbox[Y]-18))
                coinboxs.remove(t)
                #breaks the loop so they dont repeate this alot of time
                break
        
        
        for coin in coinRects:
            #if coin's rec is hit by mario takes it out of the list so
            #next time we draw them they wont comeout
            if coin.colliderect(marioRect):
                coineffect.play()
                score+=1
                coinRects.remove(coin)
                break

        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "levels"


def drawlevelone(screen,mario,goombas,koopas,coinRects,coinboxs,brick,score):
    offset = 350 - mario[X]
    screen.blit(background1, (offset,0))
    
    if mario[HEARTS] != "levels": #prevents the code from crashing becuase
        #sometimes it does not return the number
        for h in range(mario[HEARTS]):
            screen.blit(heart,(750-50*h,15))
            #this blits the hearts
        
    for c in coinRects:
        screen.blit(coinPic, (c[X]+offset,c[Y]))
        #blits out coins
        
    txtPic = fnt.render(str(score),True,(255,255,255))
    xPic = fnt.render("x",True,(255,255,255))
    screen.blit(coinPic,(10,20))
    screen.blit(txtPic,(80,15))
    screen.blit(xPic,(55,15))

    for b in brick:
        screen.blit(brickPic,(b[0]+offset,b[1]))
        #blits the newly appended bricks on the map so it covers the question mark
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

def level2():
    global frame
    once = False
    mario=[350,250,0,True,True,"right",5]
    mask=maskL[1]
    goombas=[[935,360,1,1000,935],[1140,290,1,1220,1135],[1500,390,3,1700,1500],[1650,390,3,1900,1650],[2782,390,2,2900,2782],[3743,390,4,4003,3740],[3720,390,2,3800,3720],[3800,390,2,4000,3800]]
    koopas=[[1550,378,4,2000,1500],[2300,378,3,2435,2300],[2400,378,3,2435,2100],[3302,280,1,3380,3300],[4660,350,3,4830,4660]]
    coinboxs=[[575,315],[610,315],[1540,320],[2218,335],[2255,335],[4623,283],[4690,283],[5443,319]]
    coins=[[1280,135],[1325,135],[1335,400],[1485,400],[2660,275],[2700,300],[2735,340],[2760,390],[3075,390],[3220,400],[3280,400],[4790,360]]
    coinRects=[Rect(coins[i][0],coins[i][1],40,30) for i in range(len(coins))]
    brick=[]
    coincount = []
    gamelock = "OFF"
    flagRect=Rect(6660,95,20,200)
    times = ""
    score=0
    x=0
    kx=0
    soundtime=0
    rec= difficulty()
    if rec == "levels":
        return "levels"
    mario[HEARTS] = rec

    running = True
    while running:  
        offset = 350 -mario[X]
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        if mb[0] == 1:
            print(mx-offset,my)
        frame+=1
        
        rec = moveMario(mario,mask,gamelock,once)
        if rec == "deadpage":
            return "deadpage"
        
        if mario[HEARTS]==0:
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
                
            if kx>=3:
                if jumpEnemy(mario,deadkoopa)==True:
                    deadkoopa[SPEED]=0  
            else:
                kx+=.1

        drawlevel2(mario,mask,coinboxs,brick,coinRects,goombas,koopas,score)            
        if mario[X] >= 6930:
            return "levels"
        
        marioRect=Rect(mario[X],mario[Y],50,70)
        hitbox=Rect(mario[X]+15,mario[Y],20,5)
        
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
                score += 1
                coineffect.play()
                coinRects.remove(coin)
                break
        if flagRect.colliderect(marioRect):
            if times != "once":
                once = True
                mario[X] = 6660
            times = "once"
            
            gamelock = "ON"
            
        display.flip()
        for evt in event.get():
            if evt.type==QUIT:
                return "levels"

def drawlevel2(mario,mask,coinboxs,brick,coinRects,goombas,koopas,score):
    offset = 350 - mario[X]
    screen.blit(background2, (offset,0))

    txtPic = fnt.render(str(score),True,(255,255,255))
    xPic = fnt.render("x",True,(255,255,255))
    screen.blit(coinPic,(10,20))
    screen.blit(txtPic,(80,15))
    screen.blit(xPic,(55,15))

    if mario[HEARTS] != "levels":
        for h in range(mario[HEARTS]):
            screen.blit(heart,(750-50*h,15))

    for c in coinRects:
        screen.blit(coinPic, (c[X]+offset,c[Y]))

    for coinbox in coinboxs:
        t=Rect(coinbox[X]+offset,coinbox[Y],28,15)

    for b in brick:
        screen.blit(brickPic,(b[0]+offset,b[1]))
    
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

def difficulty():

    running = True
    while running:
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        screen.blit(levelselection,(0,0))
        screen.blit(difficultypic,(80,0))
        if mb[0] == 1:
            if Rect(238,160,310,60).collidepoint(mx,my):
                return 5 #5 HEARTS
            if Rect(250,230,280,60).collidepoint(mx,my):
                return 3 #3HEARTS
            if Rect(250,300,280,60).collidepoint(mx,my):
                return 1 #ONE HEARTS
        display.flip()
        for evt in event.get():
            if evt.type==QUIT:
                return "levels"
    
def deadpage():
    deatheffect.play() #PLAYS THE SOUND MARIO DYING
    running = True
    while running:
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        if mb[0] == 1:
            if Rect(310,180,160,40).collidepoint(mx,my):
                return "levels"
            elif Rect(320,260,160,40).collidepoint(mx,my):
                return "menu"
        screen.blit(deadpic,(0,0))
        display.flip()
        for evt in event.get():
            if evt.type==QUIT:
                return "levels"
 
    
def moveMario(mario,mask,gamelock,once):

    keys = key.get_pressed()
    if keys[K_LEFT] and mario[X] > 375 and gamelock =="OFF":
        mario[direction] = "left" #WHAT DIRECTION MARIO IS FACING IN ORDER TO BLIT
        mario[still] = False #he is moving 
        
        moveleft(mario,mask)
    elif keys[K_RIGHT] and mario[X] < 7000 and gamelock == "OFF":
        mario[direction] = "right" #WHAT DIRECTION MARIO IS FACING IN ORDER TO BLIT
        mario[still] = False
        
        moveright(mario,mask,gamelock)
    else:
        mario[still] = True #he is not moving for bliting mario
    
    if keys[K_SPACE] and mario[ONGROUND] == True and gamelock == "OFF":
        jumpeffect.play()
        mario[VY] =-14
        mario[ONGROUND] = False
    hitup(mario,mask)
    rec = hitdown(mario,mask,gamelock,once)
    if rec == "deadpage":
        return "deadpage"
    if keys[K_DOWN] and mario[ONGROUND] == False and gamelock == "OFF":
        mario[VY] +=3


def moveleft(mario,mask):
    if mario[Y] <=0:
        #if mario is out of the screen we use this becuase mask.get_at would crash

        mario[X] -= 7
    else:
        for i in range(7):
            #outting for i in range checks each pixel before we move mario
            if mask.get_at((mario[X]+40,int(mario[Y]+5))) != WALL\
                and mask.get_at((mario[X]+40,int(mario[Y])+60)) != WALL:
                #this gets the colour at the mask we created and than checks if
            #mario is hitting them, we do this so mario is running within the map
                mario[X] -= 1

def moveright(mario,mask,gamelock):
    if mario[Y] <=0:
        mario[X] +=7
    else:
        for i in range(7):
            if mask.get_at((mario[X]+40,int(mario[Y]+5))) != WALL\
                and mask.get_at((mario[X]+40,int(mario[Y])+60)) != WALL:
                mario[X]+= 1

def hitdown(mario,mask,gamelock,once):
    if gamelock == "OFF":
        if mario[VY] == -14:
            mario[Y] += mario[VY]
            
        if mario[Y]+ 75 >= 490: #Checks if mario falls off the screen
            mario[VY] = 0
            mario[HEARTS] = 0
            return "deadpage"
        
        elif mario[Y]+ 75 > 0 and mario[Y] +75 < 500:
            if mask.get_at((mario[X]+10,int(mario[Y]+75))) != WALL\
               and mask.get_at((mario[X]+30,int(mario[Y]+75))) != WALL:
                mario[VY] += 0.7

            elif (mask.get_at((mario[X]+10,int(mario[Y]+75))) == WALL or mask.get_at((mario[X]+30,int(mario[Y]+75))) == WALL) and mario[2]>=0:
                # move mario out of the ground so he doesn't get dirty
                while((mask.get_at((mario[X]+10,int(mario[Y]+75))) == WALL or mask.get_at((mario[X]+30,int(mario[Y]+75))) == WALL))and mario[2]>=0:
                    mario[Y]-=1
                mario[Y]+=1 # put him 1 pixel in, for friction reasons
                mario[VY] = 0
                mario[ONGROUND] = True
            else:
                mario[Y] += mario[VY]
                mario[VY] += 0.7
                
    elif gamelock =="ON" and mask.get_at((mario[X]+10,int(mario[Y]+75))) != WALL\
        and mask.get_at((mario[X]+30,int(mario[Y]+75))) != WALL:
        if mario[VY] >0:
            mario[VY] == 0
        mario[VY] = -5
        mario[Y] -= mario[VY]

    else:
        mario[X] += 7

    if once == True:
        stagecleareffect.play()
        once == False

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
    enemy= Rect(enemy[X],enemy[Y],50,5)
    for x in range(0,52):
        for y in range(60,70):
            if enemy.collidepoint(mario[X]+x,mario[Y]+y):
                stompeffect.play()
                mario[VY] =-5
                mario[ONGROUND] = False
                return True
            
def hitMario(mario,enemy):
    enemy= Rect(enemy[X],enemy[Y],40,5)

    for x in range(0,52):
        for y in range(0,55):
            if enemy.collidepoint(mario[X]+x,mario[Y]+y):
                
                if mario[direction] == "right" or mario[direction] == "left":
                    if mario[X] < 1000:
                        mario[X] = 350
                    elif mario[X] <2000:
                        mario[X] = 900
                    elif mario[X] < 3000:
                        mario[X] = 2000
                    elif mario[X] < 4000:
                        mario[X] = 2070
                    elif mario[X] < 6000:
                        mario[X] = 5170
                    mario[Y] = 300
                    mario[VY] = 0
                mario[HEARTS]-=1


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
    if page == "level2":
        page=level2()
    if page == "level3":
        page=level3()
    if page == "deadpage":
        page=deadpage()
quit()
