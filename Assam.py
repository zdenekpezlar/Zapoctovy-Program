import random
import time
import sys













#### Variables


EndCondition = 0
AssamOrientation = 2   #position in array ['w','d','s','a']   ['^','<','v','>']
AssamX = 3
AssamY = 3

Rugs = [24,24]
Money = [30,30]



def Valid(a):   #check if square is valid
    if a<=6 and a>=0:
        return True
    else:
        return False

def Valid2(x):
    if Valid(x[0]) and Valid(x[1]):
        return True
    else:
        return False


Moves = {'w' : [0,-1],   #epicky slovnik
         'a' : [-1,0],
         's' : [0,1],
         'd' : [1,0]}

Orientation = {'w' : 0,   #epicky slovnik2
         'a' : 1,
         's' : 2,
         'd' : 3}

board = [["*" for i in range(7)] for i in range(7)]


def EndGame(): #check if game has ended
    if Money[0] <= 0:
        print("První hráč vyhrává.")
        EndCondition = 1
    else:

        if Money[1] <= 0:
            print("Druhý hráč vyhrává.")
            EndCondition = 1
        else:
            if Rugs[1] == 0:
                
                if Money[0] > Money[1]:
                    print("První hráč vyhrává.")
                else:
                    if Money[0] == Money[1]:
                        print("Remíza.")
                    else:
                        print("Druhý hráč vyhrává.")

    


def Add(couple1,couple2):
    #return [min(max(couple1[0]+couple2[0],0),6), min(max(couple1[1]+couple2[1],0),6)]
    return couple1[0]+couple2[0], couple1[1]+couple2[1]

#print(Add([1,2],Moves[['w','d','s','a'][(Orientation['s'])%4]]))   Moves[['w','d','s','a'][(Orientation['s'])%4]] znaci, kam by se mel posunout

def PrintBoard(AssamX,AssamY): #ok
    print("")
    temp = board[AssamX][AssamY]
    board[AssamX][AssamY] = ['^','<','v','>'][AssamOrientation]
    for j in range(7):
        for i in range(7):
            print(board[i][j],end='')
        print("")
    board[AssamX][AssamY] = temp
    print("")


def DiceRoll(): #ok
    r = random.randint(0,5)
    return([1,2,2,3,3,4][r])




def Move(player): #should be ok, with printin
    
    global AssamOrientation
    global AssamX
    global AssamY
    

    while True:
        print("Můžeš otočit Assama. Zvol směr:")
        dir = sys.stdin.readline().strip()
        if dir in ['w','d','a']:
            break
    #print(AssamOrientation, dir,  Orientation[dir])

    AssamOrientation += Orientation[dir]
    AssamOrientation = (AssamOrientation)%4

    print("Házím kostkou")

    time.sleep(0.8)
    res = DiceRoll()
    print("Padlo: ", res)  
    time.sleep(0.8)
    for j in range(res): 
        #print([AssamX,AssamY],Moves[['w','d','s','a'][AssamOrientation]])
        #PrintBoard(AssamX,AssamY)
        if Add([AssamX,AssamY],Moves[['w','a','s','d'][AssamOrientation]])[0] not in [-1,7] and Add([AssamX,AssamY],Moves[['w','a','s','d'][AssamOrientation]])[1] not in [-1,7] : #posune a pripadne zastavi o kraj
            AssamX = Add([AssamX,AssamY],Moves[['w','a','s','d'][AssamOrientation]])[0]
            AssamY = Add([AssamX,AssamY],Moves[['w','a','s','d'][AssamOrientation]])[1]
        else: #pokud narazi na zed, odrazi se
            #print("odraz bejby")
            AssamOrientation += 2
            AssamOrientation = AssamOrientation%4


    AX = AssamX
    AY = AssamY


    

 
    PrintBoard(AX,AY)
    col = Collect(AX,AY,player)
    #print("vydelek ",col)
    if player != board[AssamX][AssamY] and board[AssamX][AssamY] != '*':
        Money[turn] -= col
        Money[(turn+1)%2] += col
        #if player == 1:
        #    Money1 -= col
        #    Money2 += col
        #else:
        #    Money1 += col
        #    Money2 -= col

    print(end='')
    
    Dummy = 1
    Dummy2 = 1
    print("Polož první část koberce.")
    while(Dummy==1): 

        dir1 = sys.stdin.readline().strip() ###Poklada koberec, orientace global
        
        if dir1 in ['w','d','s','a'] and Valid2(Add([AssamX,AssamY],Moves[dir1])):        
            #dir1 = ['w','d','s','a'][(Orientation[dir1]+2)%2]        #####################  D,A davaji to SAMY
            mov1 = Moves[dir1]
            kob1 = [Add([AssamX,AssamY],Moves[dir1])[0],Add([AssamX,AssamY],Moves[dir1])[1]]
            if board[kob1[0]][kob1[1]]  != player:
                Money[turn] += 1
                if board[kob1[0]][kob1[1]]  != '*':
                    Money[(turn+1)%2] -= 1 ##### PRELITY Money
            
            board[kob1[0]][kob1[1]] = player #prvni koberec polozen
            Dummy = 0
        else:
            print("Zvol validní první půlku koberce.") 
            
            
            
            
    print("Polož druhou část koberce.")         
    while(Dummy2 == 1):
        

        dir2 = sys.stdin.readline().strip() 
        if dir2 in ['w','d','s','a'] and Valid2(Add(kob1,Moves[dir2])) and Add(Moves[dir1],Moves[dir2]) != [0,0]:
            #dir2 = ['w','d','s','a'][(Orientation[dir2]+2)%2]
            mov2 = Moves[dir2]
            kob2 = [Add(kob1,Moves[dir2])[0],Add(kob1,Moves[dir2])[1]]
            if board[kob1[0]][kob1[1]]  != player:
                Money[turn] += 1
                if board[kob1[0]][kob1[1]]  != '*':
                    Money[(turn+1)%2] -= 1 
            
            board[kob2[0]][kob2[1]] = player 
            Dummy2 = 0
        else:
            print("Zvol validní druhou půlku Rugs.") 
    
                

    
        
    
    
    
    PrintBoard(AssamX,AssamY)
    

    




def Collect(AssamX,AssamY,colour): #BFS  #colour je hrac na tahu 
    s=0
    bot = 0
    if board[AssamX][AssamY] in [colour, '*']: #skoci na svoje policko/volny
        return 0
        
    Stack = [AssamX + 10*AssamY]
    Disc = []
    s=1
    while Stack != Disc and bot < len(Stack): 
        

        
        tile = Stack[bot]
        #print("bere ",tile)
        x = tile%10
        y = tile//10
        #Disc.append(x + 10*y)
        if x+1 <= 6 and board[x+1][y] not in [colour,'*'] and (x+1 + 10*y) not in Disc and [AssamX,AssamY] != [x+1,y]:            
            Stack.append(x+1 + 10*y)
            Disc.append(x+1 + 10*y)
            s+=1


        if x-1 >=0 and board[x-1][y] not in [colour,'*'] and (x-1 + 10*y) not in Disc and [AssamX,AssamY] != [x-1,y]:
            Stack.append(x-1 + 10*y)
            Disc.append(x-1 + 10*y)
            s+=1



        if y+1 <= 6 and board[x][y+1] not in [colour,'*'] and (x + 10*(y+1)) not in Disc and [AssamX,AssamY] != [x,y+1]:
            Stack.append(x + 10*(y+1))
            Disc.append(x + 10*(y+1))
            s+=1
         

        if y-1 >=0 and board[x][y-1] not in [colour,'*'] and (x + 10*(y-1)) not in Disc and [AssamX,AssamY] != [x,y-1]:
            Stack.append(x + 10*(y-1))
            Disc.append(x + 10*(y-1))
            s+=1


        bot+=1
        
    return s


def BotMove(col):

    
    global AssamOrientation
    global AssamX
    global AssamY
 
    ValidMoves = [
        Moves[['w','d','s','a'][AssamOrientation]],
        Moves[['w','d','s','a'][(AssamOrientation+1)%4]],
        Moves[['w','d','s','a'][(AssamOrientation-1)%4]]
    ]
    RandVar = random.randint(0,2)

    NumInDir = [0,0,0]

    for i in range(3):
        x = AssamX 
        y = AssamY
        for j in range(4):
            x += ValidMoves[i][0]
            y += ValidMoves[i][1]

            #heuristika pocet dobrych policek - pocet spatnych policek
            if Valid2([x,y]) and board[x][y] == col:
                NumInDir[i] += 1
            if Valid2([x,y]) and board[x][y] not in [col,'*']:
                NumInDir[i] -= 1 

                #print(x,y,Valid2([x,y]))

    
    
     
    RandVar = random.randint(0,2)
    MaxMove = RandVar
    
    for j in range(3):
        if NumInDir[j] > NumInDir[MaxMove]:
            MaxMove = j
            
             #táhne ve směru , co se "nejvíc vyplatí", jinak náhodně

    time.sleep(0.8)
    
    dir = ['w','a','s','d'][(AssamOrientation + MaxMove - 1)%4] ##WOAH WOAH WOAH
    if MaxMove == 1:
        print("Bot Assáma neotočil")
    else:
        print("Bot otočil Assáma")
    print('')
    time.sleep(0.8)
    AssamOrientation = (AssamOrientation + MaxMove - 1)%4
    print("Bot hází kostkou")
    
    time.sleep(0.8)
    r = DiceRoll()

    #print(AssamX,AssamY)
    for j in range(r):
        if Valid2(Add([AssamX,AssamY],Moves[['w','a','s','d'][AssamOrientation]])):
            AssamX = Add([AssamX,AssamY],Moves[['w','a','s','d'][AssamOrientation]])[0]
            AssamY = Add([AssamX,AssamY],Moves[['w','a','s','d'][AssamOrientation]])[1]
        else:
            #print("boing")
            AssamOrientation += 2
            AssamOrientation = AssamOrientation%4
            
    print("Bot hodil ", r)
    time.sleep(0.8)
    PrintBoard(AssamX,AssamY)
    
    time.sleep(0.8)
    
    print("Bot pokládá koberec")
    
    time.sleep(0.8)
    
    
    while True:
        
        RandVar = random.randint(0,3)
        if Valid2(Add([AssamX,AssamY],Moves[['w','a','s','d'][RandVar]])):
            move1 = RandVar
            break
    

    for j in range(4):
        if Valid2(Add([AssamX,AssamY],Moves[['w','a','s','d'][j]])):
            if board[ Add([AssamX,AssamY],Moves[['w','a','s','d'][j]])[0] ][ Add([AssamX,AssamY],Moves[['w','a','s','d'][j]])[0] ] not in ['*',col]:
                move1 = j

                Money[(turn +1)%2] -= 1
                break
            else:
                if board[ Add([AssamX,AssamY],Moves[['w','a','s','d'][j]])[0] ][ Add([AssamX,AssamY],Moves[['w','a','s','d'][j]])[0] ] == '*':
                    move1 = j
                
                
        
    kob1 = [Add([AssamX,AssamY],Moves[['w','a','s','d'][move1]])[0], Add([AssamX,AssamY],Moves[['w','a','s','d'][move1]])[1]]
    
    
    while True:
        
        RandVar = random.randint(0,3)
        if Valid2(Add(kob1,Moves[['w','a','s','d'][RandVar]])) and Add(kob1,Moves[['w','a','s','d'][RandVar]]) != [AssamX,AssamY]:
            move2 = RandVar
            break
    

    for j in range(4):
        if Valid2(Add(kob1,Moves[['w','a','s','d'][j]])):

        
            if Add(kob1,Moves[['w','a','s','d'][j]]) != [AssamX,AssamY]:
                if board[ Add(kob1,Moves[['w','a','s','d'][j]])[0] ][ Add(kob1,Moves[['w','a','s','d'][j]])[0] ] not in ['*',col]:
                    move2 = j
            
                    Money[(turn +1)%2] -= 1
                    break
                else:
                    if board[ Add(kob1,Moves[['w','a','s','d'][j]])[0] ][ Add(kob1,Moves[['w','a','s','d'][j]])[0] ] == '*':
                        move2 = j
        
    kob2 = [Add(kob1,Moves[['w','a','s','d'][move2]])[0] , Add(kob1,Moves[['w','a','s','d'][move2]])[1]]
    #print(AssamX,AssamY,kob1,kob2)

    if board[kob1[0]][kob1[1]] != col: 
        board[kob1[0]][kob1[1]] = col
        Money[turn] +=1
        
    if board[kob2[0]][kob2[1]] != col: 
        board[kob2[0]][kob2[1]] = col
        Money[turn] +=1
    
    
    
    
    PrintBoard(AssamX,AssamY)
        
            
               






def GameVsP():
    global EndCondition
    global turn 
    AX = 3
    AY = 3
    turn = 0
    PrintBoard(AX,AY)
    
    while EndCondition == 0:

        Move('r')
        
        #print(AX,AY)
        Rugs[0] -= 1
        
        print("První hráč má ", Money[0], " peněz a ", Rugs[0], " koberců. Druhý hráč má", Money[1], "peněz a ",Rugs[1]," koberců.")
        print('')
        turn = 1-turn

        if  Money[0] <= 0 or Money[1] <= 0:
            EndCondition = 1

            break
        time.sleep(1)

        Move('b')
        
        Rugs[1] -= 1
        
        #print(AX,AY)
        turn = 1-turn
        #Rugs2 -= 1

        print("První hráč má ", Money[0], " peněz a ", Rugs[0], " koberců. Druhý hráč má", Money[1], "peněz a ",Rugs[1]," koberců.")
        print('')
        if Rugs[1] == 0 or Money[0] <= 0 or Money[1] <= 0:
            EndCondition = 1
            break
            
        time.sleep(1)

    EndGame()


def GameVsBot():

    print("Hraješ jako první.")
    global EndCondition
    global turn
    AX = 3
    AY = 3
    turn = 0
    
    PrintBoard(AX,AY)
    while EndCondition == 0: #winning podminku
        
        
        Move('r')
        Rugs[0] -= 1
        print("První hráč má ", Money[0], " peněz a ", Rugs[0], " koberců. Druhý hráč má", Money[1], "peněz a ",Rugs[1]," koberců.")
        
        
        if Rugs[0] == 0 or Money[0] <= 0 or Money[1] <= 0:
            EndCondition = 1
            break
    
        turn = 1-turn
       
        
        
        BotMove('b')
        Rugs[1] -= 1
        print("První hráč má ", Money[0], " peněz a ", Rugs[0], " koberců. Druhý hráč má", Money[1], "peněz a ",Rugs[1]," koberců.")
        
        
        

        if Money[0] <= 0 or Money[1] <= 0:
            EndCondition = 1
            break
        
        turn = 1-turn
    
    EndGame()



        

def GameBotVsBot():
    global EndCondition
    global turn
    AX = 3
    AY = 3
    PrintBoard(AX,AY)
    turn = 0
    while EndCondition == 0: 
        
        BotMove('r')
        Rugs[0] -= 1
        print("První hráč má ", Money[0], " peněz a ", Rugs[0], " koberců. Druhý hráč má", Money[1], "peněz a ",Rugs[1]," koberců.")
        
        if Money[0] <= 0 or Money[1] <= 0:
            EndCondition = 1
            break
        
        turn = 1-turn
        
        BotMove('b')
        Rugs[1] -= 1
        print("První hráč má ", Money[0], " peněz a ", Rugs[0], " koberců. Druhý hráč má", Money[1], "peněz a ",Rugs[1]," koberců.")

        if Rugs[0] == 0 or Money[0] <= 0 or Money[1] <= 0:
            EndCondition = 1

        turn = 1-turn
    EndGame()





print("Hra Marrakech")
print("Pro hru 1v1 stiskni 1. Pro hru vs. bot stiskni 2. Pro hru bot vs. bot stiskni 3. Pro pravidla stiskni 4.")

while True:
    inp = sys.stdin.readline().strip()
    if inp not in ['1','2','3','4']:
        print("Pro hru 1v1 stiskni 1. Pro hru vs. bot stiskni 2. Pro hru bot vs. bot stiskni 3. Pro pravidla stiskni 4.")
        continue
    
    if inp == '1':
        GameVsP()
    if inp == '2':
        GameVsBot()
    if inp == '3':
        GameBotVsBot()
    if inp == '4':
        print("Pravidla této krásné hry:")
        print(end='')
        print("Dva hráči začínající s 30 drahmami, 24 koberci a střídají se v tazích. Ve svém tahu hráč nejprve může otočit figurku Assáma doprava, doleva nebo nechat -- zadá písmena 'd', 'a', resp. 'w'. Poté hodí kostkou a o tolik polí se pohne.")
        print("Pokud hráč skončí svůj pohyb na koberci protihráče, přelijí se peníze mezi hráči. Počet přelitých drahem je roven obsahu největší souvislé plochy protihráčových koberců, na kterých právě Assám stojí.")
        print("Poté hráč položí koberec 1x2 vedle figurky Assama pomocí zkratek 'w', 'a', 's', 'd', tentokrát globálně vůči hrací ploše. Pokud se tímto nějaké koberce protihráče překryjí, počet takových překrytí se přelije mezi hráči. Tím tah hráče končí.")
        print("Hra končí, má-li počet peněz nějakého hráče klesnout pod jedna nebo pokud dojdou koberece. Vítězí hráč s více drahmami na konci hry.")


    
