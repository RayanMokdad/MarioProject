##### HEADER COMMENTS #####
## Project by: Rayan Mokdad and Vicky Chen ##
# This project is a replica of Super Mario Bros. 
# This is a one player game where the user is mario and they can select to play one of two levels.
# Each with their own enemies like Goomba and Koopa.
# There is an instruction screen and a credits that users can access. 
# The score is kept track of by the amount of
# coins collected as well as the amount of enemies defeated.The score is then displayed on
# the level screen once the level is completed.
# The arrow keys are used to move left and right, and the space bar is used to jump.
# The down arrow key is used to speed up mario's gravitational force (velocity downwards).
# Enemies are killed by jumping on their heads, the Koopas(turtles) are turned into shells that move sideways
# for a few seconds until they disappear. 
# There is a timer set so if it runs out mario dies.
# There are coinboxes with question marks that produce more coins when hit from the bottom.
# Sounds are used:
#   To warn users when timer begins to run out
#   When mario dies
#   When mario hits enemies
#   When coins are collected
#   When mario jumps
#   When end of the level is reached

#For scaling purposes, a new file was created called "scale.py" to scale any photos

#Funny stuff
#In the first level on one of the tubes, there is a secret article that appears when the user stands on it
#and presses the down arrow key
#For scaling purposes, a new file was created called "scale.py" to scale any photos
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
scores=[]


#these are constants variable that is a pos in the list

#MARIO
VY=2 #Velocity
ONGROUND=3 #checks if mario is on the ground
direction = 5 #checks direction
still = 4 #if hes standing still
HEARTS=6 #the amount of hearts

#enemy
SPEED = 2 
MAX = 3 #maz pos it can go 
MIN = 4 #vice versa

#universal
X=0
Y=1
frame=0 #counter for sprites
DELAY=5 #to delay frames so it looks smoother

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
leveloneshotRect= Rect(30,246,310,100)

leveltwoshot=image.load("Title Page/leveltwoshot.png")
leveltwoshotRect= Rect(450,250,295,95)


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

#clock
clockPic=image.load("clock.png")

#bricks
brickPic = image.load("brick.png")

#back
backPic = image.load("back.png")
backPic = transform.scale(backPic,(70,60))
backRect= Rect(10,20,70,60)

###credits
creditpage = image.load("credits.jpeg")
creditspic = image.load("credits.png")
creditspic = transform.scale(creditspic,(300,400))
creditRect = Rect(330,255,130,35)

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
deadkoopaPics=pics('koopashell',0,3)
for i in range (len(deadkoopaPics)):
    deadkoopaPics[i]=transform.scale(deadkoopaPics[i],(40,35))

####sounds
coineffect=mixer.Sound("sounds/coin.wav") 
flagpole=mixer.Sound("sounds/flagpole.wav") 
jumpeffect=mixer.Sound("sounds/jump.wav") 
stompeffect=mixer.Sound("sounds/stomp.wav") 
deatheffect=mixer.Sound("sounds/death.wav")
timewarning = mixer.Sound("sounds/timewarning.wav")

mixer.music.load("sounds/Theme.mp3")
mixer.music.play(-1) #-1 plays the music again when the song finishes
mixer.music.set_volume(.1)

#plumbing
plumbingpic= image.load("plumbing.png")
plumbingpic = transform.smoothscale(plumbingpic,(800,500))

#material
material = image.load("material.png")
material = transform.smoothscale(material,(800,500))
        
'''
This is where the game starts
'''

def menu():
    x=0 #where the background is blit
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
            return "levels" #takes us to level page
        if mb[0]==1 and instructionRect.collidepoint(mx,my):
            return "instruction" #takes us to instruction  page
        if mb[0] == 1 and creditRect.collidepoint(mx,my):
            return "credits"
       
        titlepage(x,marioPics)
        if x ==-1200: #checking where the background is currently blitting
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
    screen.blit(creditspic,(220,80))
    frame+=1 
    f = int(frame) // DELAY % (len(marioPics)-2)
    #takes the frame and delays each frame by 5, blits the frame it is on currently
    screen.blit(marioPics[f], (350,365))
    f = frame // DELAY % (len(goombaPics)-1) 
    screen.blit(goombaPics[f], (410,390))
    f = frame // DELAY % len(koopaPics)
    screen.blit(koopaPics[f], (310,375))    
def instruction(): #the instruction manual
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

def credit():
    running = True
    while running:
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()
        screen.blit(creditpage,(0,0))
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
        screen.blit(levelonepic,(-10,30))
        screen.blit(leveltwopic,(460,30))
        screen.blit(leveloneshot,(30,250))
        screen.blit(leveltwoshot,(450,250))
        screen.blit(backPic,(20,20))
        
        #Aesthetics
        draw.rect(screen,(255,255,255),leveloneshotRect,6)
        draw.rect(screen,(255,255,255),leveltwoshotRect,6)
        draw.rect(screen,(255,0,0),leveloneshotRect,2)
        draw.rect(screen,(255,0,0),leveltwoshotRect,2)

        #SHOWS SCORE ONCE LEVEL ONE COMPLETED
        if len(scores)>0:
            score1Pic = fnt.render(str(scores[0]),True,(255,255,255))
            screen.blit(score1Pic,(210,350))
            score = fnt.render(("SCORE"),True,(255,255,255))
            screen.blit(score,(90,350))

        #SHOWS SCORE AFTER LEVEL TWO COMPLETED
        if len(scores)>1:
            score2Pic = fnt.render(str(scores[1]),True,(255,255,255))
            screen.blit(score2Pic,(630,350))
            score = fnt.render(("SCORE"),True,(255,255,255))
            screen.blit(score,(500,350))
            
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
                return "level1" #starts level one
            elif leveloneshotRect.collidepoint(mx,my):
                return "level1"#starts level one
            elif leveltwoRect.collidepoint(mx,my):
                return "level2"#starts level two
            elif leveltwoshotRect.collidepoint(mx,my):
                return "level2"#starts level one
           

##################################        LEVEL ONE      #######################################
def level1():
    global frame
    once = False
    ### sets everyone in place for level one ###
    
    mario=[350,250,0,True,True,"right",5] #the positions specifically for level one
    
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
    brick= []
    
    timer = 200 #timer for level 1
    running = True
    score=0
    #goomba timer
    gt=0
    #koopa timer 
    kt=0
    flagRect=Rect(6600,80,20,450) #flag at the end
    gamelock = "OFF" #Locks user from controlling mario
    times ="" #limits user from using the flag more than once

    #Higher difficulty gives user less "hearts" or lives
    rec= difficulty()
    if rec == "levels": #allows the user to exit this page without crashing
        return "levels"
    mario[HEARTS] = rec

        

    while running:
        offset = 350 -mario[X] #offset allows background to move giving illusion of mario moving
        frame+=1 #constantly adding to make frames move
        keys=key.get_pressed()
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()

            
####Function that draws level one####
        drawlevelone(screen,mario,goombas,koopas,coinRects,coinboxs,brick,score,timer)

## If timer ends, mario dies ##
        if timer<=0:
            return "deadpage"
        else:
            timer-=.01 #counts down
        if round(timer) == 30:
            timewarning.play()
        
        #If mario loses all his hearts he dies and goes to a dead page
        if mario[HEARTS]==0: 
            return "deadpage"
        #Once mario falls through the ground he dies
        rec = moveMario(mario,mask,gamelock,once)
        if rec == "deadpage":
            return "deadpage"
        #this is a secert level page
        if mario[X] > 930 and mario[X] < 980 and mario[ONGROUND] == True and keys[K_DOWN]:
            plumbing()        
        ###   GOOMBA MOVING   ###
        for goomba in goombas:
            moveEnemy(goomba)
            hitMario(mario,goomba)
            if jumpEnemy(mario,goomba)==True: #if mario kills a goomba it removes goomba from the list
                score +=1 #adds a point to the coin count
                
                goombas.remove(goomba)
                deadGoombas.append((goomba[X],goomba[Y]+35)) #returns it to a dead picture of goomba
        for goomba in deadGoombas:
            if gt>=3: #timer for removing the goombas
                deadGoombas.remove(goomba)
                gt=0                    
            else:
                gt+=.2


        ###   KOOPA MOVING   ###
        for koopa in koopas:
            hitMario(mario,koopa)
            moveEnemy(koopa)
            if jumpEnemy(mario,koopa)==True:
                score +=1
                koopas.remove(koopa)
                deadKoopas.append(koopa)
                
        for deadkoopa in deadKoopas:
            moveEnemy(deadkoopa)
            hitMario(mario,deadkoopa)
            #sets timer for how long a koopa stays a shell
            if kt>=40:
                deadKoopas.remove(deadkoopa)
                kt=0                
            else:
                kt+=.1
            #makes sure mario can hit shell without removing it too early
            if kt>=3:
                if jumpEnemy(mario,deadkoopa)==True:
                    deadkoopa[SPEED]=0  
            else:
                kt+=.1
                
        #When mario reaches the end of the level it returns to level choosing screen
        #With final score
        if mario[X] >= 6770:
            scores.append(score)
            return "levels"
        

        marioRect=Rect(mario[X],mario[Y],50,70)
        offset = 350 - mario[X]
        hitbox=Rect(mario[X]+15,mario[Y],20,5)
        
        if flagRect.colliderect(marioRect):
            if times != "once": #makes sure mario only collides once
                mario[X] = 6590
                once = True
            times = "once"
            gamelock = "ON" #moves mario on its own. 
            flagpole.play()
            flagpole.set_volume(0.1)
            
            
        for coinbox in coinboxs:
            t=coinbox
            coinbox=Rect(coinbox[X],coinbox[Y],27,15)
            if coinbox.colliderect(hitbox):
                coinRects.append(Rect(coinbox[X]-5,coinbox[Y]-55,40,30))
                brick.append((coinbox[X]-3,coinbox[Y]-18)) #turns question boxes into unusable boxes
                coinboxs.remove(t)
                break
        
        
        for coin in coinRects:
            if coin.colliderect(marioRect):
                coineffect.play()
                score +=1 #adds one coin to the score
                coinRects.remove(coin)
                break
            
        

        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "levels"

def plumbing():
    running = True
    while running:
        screen.blit(plumbingpic,(0,0))
        display.flip()
        for evt in event.get():
            if evt.type == QUIT:
                return "level1"
    
###    Draws level one    ###
def drawlevelone(screen,mario,goombas,koopas,coinRects,coinboxs,brick,score,timer):
    offset = 350 - mario[X]
    screen.blit(background1, (offset,0))

    ## blits hearts ##
    if mario[HEARTS] != "levels":
        for h in range(mario[HEARTS]):#makes sure hearts are spaced correctly
            screen.blit(heart,(750-50*h,15))

    ## Blits text like the score, and timer on the screen ##
    txtPic = fnt.render(str(score),True,(255,255,255))
    xPic = fnt.render("x",True,(255,255,255))
    screen.blit(coinPic,(10,10))
    screen.blit(txtPic,(80,5))
    screen.blit(xPic,(55,5))
    timerPic = fnt.render(str(round(timer)),True,(255,255,255))
    screen.blit(timerPic,(60,45))
    screen.blit(clockPic,(10,50)) 

    ## blits coins ##
    for c in coinRects:
        screen.blit(coinPic, (c[X]+offset,c[Y]))
    ## blits bricks ##
    for b in brick:
        screen.blit(brickPic,(b[0]+offset,b[1]))

    ## GOOMBAS ##
    f = frame // DELAY % (len(goombaPics)-1)
    for goomba in goombas:
        #moving right
        if goomba[SPEED]>0: 
            screen.blit(goombaPics[f], (goomba[X]+offset,goomba[Y]))
        #moving left
        else: 
            screen.blit((transform.flip(goombaPics[f],True,False)), (goomba[X]+offset,goomba[Y]))
    #blits flat version of goomba
    for goomba in deadGoombas:
        screen.blit(goombaPics[11], (goomba[X]+offset,goomba[Y]))
        
    ## KOOPAS ##
    f = frame // DELAY % len(koopaPics)
    for koopa in koopas:
        if koopa[SPEED]>0:
            screen.blit(koopaPics[f], (koopa[X]+offset,koopa[Y]))
        else:
            screen.blit((transform.flip(koopaPics[f],True,False)), (koopa[X]+offset,koopa[Y]))

    f = frame // 3 % len(deadkoopaPics) #i used three for delay so it has quicker frames
    for koopa in deadKoopas:
        screen.blit(deadkoopaPics[f], (koopa[X]+offset,koopa[Y]+20))
        
    ## MARIO ##
    f = frame // DELAY % (len(marioPics)-2)

    #mario facing left direction
    if mario[direction]=="left":
        if mario[ONGROUND]==False: #in air
            screen.blit(marioPics[9], (350,mario[Y]))
        elif mario[still]:
            screen.blit((transform.flip(marioPics[0],True,False)), (350,mario[Y]))
        else:
            screen.blit((transform.flip(marioPics[f],True,False)), (350,mario[Y]))
            
    #mario facing right direction
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
    gamelock = "OFF"
    flagRect=Rect(6660,95,20,200)
    times = ""
    timer=200
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
        keys=key.get_pressed()
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()

        frame+=1
        
        rec = moveMario(mario,mask,gamelock,once)
        if rec == "deadpage":
            return "deadpage"
        
        if mario[HEARTS]==0:
            return "deadpage"

        if timer<=0:
            return "deadpage"
        elif timer == 30:
            timewarning.play()
            timer -= 0.5
        else:
            timer-=.05
        if round(timer) == 30:
            timewarning.play()

        if mario[X] > 3660 and mario[X] < 3720 and mario[ONGROUND] == True and keys[K_DOWN]:
            materials()
            
        for goomba in goombas:
            moveEnemy(goomba)
            hitMario(mario,goomba)
            if jumpEnemy(mario,goomba)==True:
                score +=1
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
                score +=1
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

        drawlevel2(mario,mask,coinboxs,brick,coinRects,goombas,koopas,score,timer)
        
        if mario[X] >= 6930:
            scores.append(score)
            return "levels"
        
        marioRect=Rect(mario[X],mario[Y],50,70)
        hitbox=Rect(mario[X]+15,mario[Y],20,5)
        
        for coinbox in coinboxs:
            t=coinbox
            coinbox=Rect(coinbox[X],coinbox[Y],27,15)
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
            flagpole.play()
            flagpole.set_volume(0.1)
            
        display.flip()
        for evt in event.get():
            if evt.type==QUIT:
                return "levels"

def materials():
    running = True
    while running:
        screen.blit(material,(0,0))
        display.flip()
        for evt in event.get():
            if evt.type== QUIT:
                return "level2"
def drawlevel2(mario,mask,coinboxs,brick,coinRects,goombas,koopas,score,timer):
    offset = 350 - mario[X]
    screen.blit(background2, (offset,0))

    txtPic = fnt.render(str(score),True,(255,255,255))
    xPic = fnt.render("x",True,(255,255,255))
    screen.blit(coinPic,(10,10))
    screen.blit(txtPic,(80,5))
    screen.blit(xPic,(55,5))
    timerPic = fnt.render(str(round(timer)),True,(255,255,255))
    screen.blit(timerPic,(10,40))

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
    if mario[direction]=="left":
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
                return 5
            if Rect(250,230,280,60).collidepoint(mx,my):
                return 3
            if Rect(250,300,280,60).collidepoint(mx,my):
                return 1
        display.flip()
        for evt in event.get():
            if evt.type==QUIT:
                return "levels"
    
def deadpage():
    deatheffect.play()
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
        mario[still] = False #indication that he is not moving
        
        moveleft(mario,mask) #brnigs it to the moving left function
    elif keys[K_RIGHT] and mario[X] < 7000 and gamelock == "OFF":
        mario[direction] = "right" #WHAT DIRECTION MARIO IS FACING IN ORDER TO BLIT
        mario[still] = False
        
        moveright(mario,mask,gamelock) #moving right function where mario is moved
    else:
        mario[still] = True #indicates that he is moving
    if keys[K_SPACE] and mario[ONGROUND] == True and gamelock == "OFF":
        #if mario is on the ground and the lock is off than VY is added so mario will jump
        jumpeffect.play()
        mario[VY] =-14
        mario[ONGROUND] = False #so we dont keep adding to VY
    hitup(mario,mask) #this function stop mario from jumping pass the bricks
    rec = hitdown(mario,mask,gamelock,once) #check if mario is hitting the mask
    if rec == "deadpage": #this is if mario falls through the ground 
        return "deadpage" 
    if keys[K_DOWN] and mario[ONGROUND] == False and gamelock == "OFF":
        mario[VY] +=3 #this allows user to mark mario drop down faster        


def moveleft(mario,mask):
    if mario[Y] <=0:
        #if mario is out of the screen we use this becuase mask.get_at would crash
        mario[X] -= 7
    else:
        for i in range(7):
            #outting for i in range checks each pixel before we move mario
            if mask.get_at((mario[X]+5,int(mario[Y]+5))) != WALL\
                and mask.get_at((mario[X],int(mario[Y]+60))) != WALL:
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
    if gamelock == "OFF": #if the user lock is off than mario will jump down normal
        if mario[VY] == -14: #this only runs once (when mario first jump)
            mario[Y] += mario[VY]

        if mario[Y]+ 75 >= 490: #if mario is out of the screen
            mario[VY] = 0 #stops mario from moving down
            mario[HEARTS] = 0 #this makes mario dies
            return "deadpage"
        
        elif mario[Y]+ 75 > 0 and mario[Y] +75 < 500: #if mario is in the map
            if mask.get_at((mario[X]+10,int(mario[Y]+75))) != WALL\
               and mask.get_at((mario[X]+30,int(mario[Y]+75))) != WALL: #if these poins
                #on mario is not hitting any point on the mask Than 
                mario[Y] += mario[VY] #mario will continue to fall
                mario[VY] += 0.7 #and this maks mario fall faster and faster


            elif (mask.get_at((mario[X]+10,int(mario[Y]+75))) == WALL or mask.get_at((mario[X]+30,int(mario[Y]+75))) == WALL) and mario[2]>=0:
                # move mario out of the ground so he doesn't get dirty
                while((mask.get_at((mario[X]+10,int(mario[Y]+75))) == WALL or mask.get_at((mario[X]+30,int(mario[Y]+75))) == WALL))and mario[2]>=0:
                    mario[Y]-=1 #some times mario[Y] + mario[VY] will make mario fall a bit pass
                mario[Y]+=1     # put him 1 pixel in, for friction reasons
                mario[VY] = 0 #set it to zero so mario stop falling
                mario[ONGROUND] = True #indicates mario that he is on the ground
                
            else:
                mario[Y] += mario[VY] 
                mario[VY] += 0.7
                
    elif gamelock =="ON" and mask.get_at((mario[X]+10,int(mario[Y]+75))) != WALL\
        and mask.get_at((mario[X]+30,int(mario[Y]+75))) != WALL: #if the user hits the flag the computer moves mario on its on
        if mario[VY] >0: #if there is still VY than set it to zero first
            mario[VY] == 0
        mario[VY] = -5 #than adds this constantly to mario to move him down the flag
        mario[Y] -= mario[VY]

    else:
        mario[X] += 7

def hitup(mario,mask):
    if mario[Y] <=0: #make sure mario is in the mask first
        pass
    elif mask.get_at((mario[X]+10,int(mario[Y]))) == WALL or mask.get_at((mario[X]+30,int(mario[Y]))) == WALL:
        if mario[VY] < 0: #if mario is still jumping up
            mario[VY] = 0 #stop him
            
### function to check if mario hits an enemy by jumping ###
def jumpEnemy(mario,enemy):    
    enemy= Rect(enemy[X],enemy[Y],50,5)
    for x in range(0,52): #the width of mario
        for y in range(60,70):#checks a rect at the bottom of mario
            if enemy.collidepoint(mario[X]+x,mario[Y]+y): #if mario hits the enemy
                stompeffect.play() #play the sound feet
                mario[VY] =-5
                mario[ONGROUND] = False
                return True
            
### function created to check if mario is hit ###    
def hitMario(mario,enemy):
    enemy= Rect(enemy[X],enemy[Y],40,5) 
    for x in range(0,52):
        for y in range(0,55):
            ### makes checkpoints for mario, when he dies ###
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

### function to move enemies ###
def moveEnemy(enemy):
    enemy[X] += enemy[SPEED] # increases by their speed
    #sets barriers for goombas
    if enemy[X]>=enemy[MAX]: 
        enemy[SPEED]*= -1
    if enemy[X]<=enemy[MIN]:
        enemy[SPEED]*= -1


page="menu"
while page!= "exit":
    if page == "menu":
        page=menu()
    if page == "instruction":
        page=instruction()
    if page == "credits":
        page=credit()
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
