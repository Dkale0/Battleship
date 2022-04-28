import random
import copy
import numpy
import matplotlib.pyplot as plt

gridPlayerA = [0] * 100 #IA's grid
gridPlayerB = [0] * 100 #Player's grid
gridPlayerC = [0] * 100 #Player's grid


gridGamePlayerA = [0] * 100 # just create a copy of the IA boards and only show the empty board
gridGamePlayerB = [0] * 100 
gridGamePlayerC = [0] * 100 


OnGame = True # turn on the game

PrevPlayerShoots = []
PrevIAShoots = []


def main():
  strategyOne = []
  for a in range(10000):
    clear_board(gridPlayerA) 
    clear_board(gridPlayerB)
    clear_board(gridPlayerC)
    clear_board(gridGamePlayerA) 
    clear_board(gridGamePlayerB)
    clear_board(gridGamePlayerC)
    PrevPlayerShoots = []
    PrevIAShoots = [] 

    
    put_boats(gridPlayerA)#put IA's boats randomly
    while sum(gridPlayerA) != 14:
      clear_board(gridPlayerA) 
      put_boats(gridPlayerA)

    gridPlayerB = copy.deepcopy(gridPlayerA)
    gridPlayerC = copy.deepcopy(gridPlayerC)
    result = RandomStrategy(gridPlayerA=gridPlayerA)
    result = RandomStrategy(gridPlayerB)
    result = RandomStrategy(gridPlayerC)

    #print(result)
    strategyOne.append(result)

  strategyOne = numpy.asarray(strategyOne)
  print(numpy.mean(strategyOne, axis=0))
  #print(result)

def SingleMatch():
    BoatTouchedByPlayer = 0
    BoatTouchedByIA = 0
      
    PrevPlayerShoots = []
    PrevIAShoots = [] 
    clear_board(gridPlayerA)
    put_boats(gridPlayerA)#put IA's boats randomly

    while sum(gridPlayerA) != 14:
      clear_board(gridPlayerA) 
      put_boats(gridPlayerA)
      #print(sum(gridPlayerA))

    # deepcopy grid A to grid B (so boats orientations are that same on both grids)
    gridPlayerB = copy.deepcopy(gridPlayerA) 
    temp = 0
    # for i in range(10):
    #   print(gridPlayerA[i*10:i*10+10]) # print the IA's grid (with no boats)
    # print("SUM: ", sum(gridPlayerA))

    while (BoatTouchedByIA < 14) and (BoatTouchedByPlayer < 14):
        # for i in range(10):
        #   print(gridGamePlayerA[i*10:i*10+10]) 
        Player_Shoot = temp
        if can_shoot(PrevPlayerShoots, Player_Shoot) == True: 
            #print(Player_Shoot)
            if gridPlayerA[Player_Shoot] == 1: 
                shoot_Touched(gridGamePlayerA, Player_Shoot) # call the shoot function that replace the coord by an F on the empty board
                #print("touched")
                BoatTouchedByPlayer = BoatTouchedByPlayer + 1 # count until 14 (number of boat "parts")
 
            else:
                shoot(gridGamePlayerA, Player_Shoot)
                #print("missed, IA's turn : ")
                IA_shot = random.randint(0, 99) 
                while can_shoot(PrevIAShoots, IA_shot) == False:
                  IA_shot = random.randint(0, 99)


                if gridPlayerB[IA_shot] == 1:
                    #print("IA touched one of your boat")
                    shoot_Touched(gridGamePlayerB, IA_shot) 
                    #print(gridPlayerB)
                    BoatTouchedByIA = BoatTouchedByIA + 1 

                else:
                    shoot(gridGamePlayerB, IA_shot) # replace the shoot by an X
                    #print("Lucky, IA missed !")
        temp += 1
    #     print("temp, BoatTouched: ", temp, BoatTouchedByPlayer, BoatTouchedByIA)
    # for i in range(10):
    #   print(gridGamePlayerA[i*10:i*10+10])
    return temp, BoatTouchedByPlayer, BoatTouchedByIA
       

def ConseqStrategy(gridPlayerA):
    BoatTouchedByPlayer = 0      
    PrevPlayerShoots = []
    # clear_board(gridPlayerA)
    # put_boats(gridPlayerA)#put IA's boats randomly

    # while sum(gridPlayerA) != 14:
    #   clear_board(gridPlayerA) 
    #   put_boats(gridPlayerA)

    temp = 0
    while (BoatTouchedByPlayer < 14):
        Player_Shoot = temp
        if can_shoot(PrevPlayerShoots, Player_Shoot) == True: 
            if gridPlayerA[Player_Shoot] == 1: 
                shoot_Touched(gridGamePlayerA, Player_Shoot) # call the shoot function that replace the coord by an F on the empty board
                BoatTouchedByPlayer = BoatTouchedByPlayer + 1 # count until 14 (number of boat "parts")
            else:
                shoot(gridGamePlayerA, Player_Shoot)
        temp += 1
        print("temp, BoatTouched: ", temp, BoatTouchedByPlayer)
    # for i in range(10):
    #   print(gridGamePlayerA[i*10:i*10+10])
    return temp, BoatTouchedByPlayer



def RandomStrategy(gridPlayerA):
    BoatTouchedByPlayer = 0      
    PrevPlayerShoots = []
    temp = 0
    
    while (BoatTouchedByPlayer< 14):
        Player_Shoot = random.randint(0, 99) 
        while can_shoot(PrevPlayerShoots, Player_Shoot) == False:
            Player_Shoot = random.randint(0, 99)


        if gridPlayerA[Player_Shoot] == 1:
            #print("IA touched one of your boat")
            shoot_Touched(gridGamePlayerA, Player_Shoot) 
            #print(gridPlayerB)
            BoatTouchedByPlayer = BoatTouchedByPlayer + 1 

        else:
            shoot(gridGamePlayerA, Player_Shoot) # replace the shoot by an X
            #print("Lucky, IA missed !")
        temp += 1
    return temp, BoatTouchedByPlayer

def PlotStuff(G1, G2, G3):
    plt.hist(G1, bins = np.arange(0,100), label="Hunt: Random Search", alpha=0.5)
    plt.hist(G2, bins = np.arange(0,100), label="Hunt: Chessboard Search", alpha=0.5)
    plt.hist(G3, bins = np.arange(0,100), label="Random Search", alpha=0.5)
    plt.legend()


def Strat1(gridPlayerA):
    BoatTouchedByPlayer = 0     
    PrevPlayerShoots = []
    total_shots = 0
    mode = "hunt"
    firstHuntSquare = []
    d_index = 0
    dFirstShot = False
    d_list = [-1, -10, 1, 10]
    base_square = 0
    current_square = 0
    dOpposite = False
    dSpecialOp = False # when first square hit is an edge case

    last_shot = 0

    print("INITIAL BOARD")
    for i in range(10):
        print(gridPlayerA[i*10:i*10+10])

    while (BoatTouchedByPlayer < 14):
        # for i in range(10):
        #   print(gridGamePlayerA[i*10:i*10+10]) 
        Player_Shoot = random.randint(0, 99)
        while can_shoot(PrevPlayerShoots, Player_Shoot) == False:
            Player_Shoot = random.randint(0, 99)
        #last_shot = Player_Shoot
        if mode == "hunt":
            print("mode = Hunt")
            if gridPlayerA[Player_Shoot] == 1:
                #print("IA touched one of your boat")
                shoot_Touched(gridGamePlayerA, Player_Shoot) 
                firstHuntSquare.append(Player_Shoot)
                dFirstShot = True
                d_index = 0
                dOpposite = False
                #print(gridPlayerB)
                BoatTouchedByPlayer = BoatTouchedByPlayer + 1

                mode = "destroy"

            else:
                shoot(gridGamePlayerA, Player_Shoot)


        else: ## ELSE if mode is DESTROY
            print("mode = DESTROY")
            print("FIRST SHOT: ", dFirstShot)
            if dFirstShot == True: # FIRST SHOT
                base_square = firstHuntSquare[-1]
                
                Player_Shoot = d_list[d_index] + base_square
                while can_shoot(PrevPlayerShoots, Player_Shoot) == False:
                    print(d_index)
                    d_index += 1
                    Player_Shoot = d_list[d_index] + base_square
                if gridPlayerA[Player_Shoot] == 1:
                    shoot_Touched(gridGamePlayerA, Player_Shoot) 
                    BoatTouchedByPlayer = BoatTouchedByPlayer + 1
                    dFirstShot = False
                else:
                    shoot(gridGamePlayerA, Player_Shoot)
                



            else: # Shots after the first
                
                print("dOpp", dOpposite)
                base_square = firstHuntSquare[-1]
                current_square = PrevPlayerShoots[-1]
                print("current b4: ", current_square)
                if dOpposite == False:
                    Player_Shoot = current_square + d_list[d_index]
                    if can_shoot(PrevPlayerShoots, Player_Shoot) == False:
                        d_index *= -1  # attacks in opposite direction
                        dOpposite = True
                        total_shots -= 1 # reduce a turn
                        
                    else:
                        if gridPlayerA[Player_Shoot] == 1:
                            shoot_Touched(gridGamePlayerA, Player_Shoot) 
                            BoatTouchedByPlayer = BoatTouchedByPlayer + 1
                        else:
                            d_index *= -1  # attacks in opposite direction
                            dOpposite = True
                            shoot(gridGamePlayerA, Player_Shoot)

                else: # if dopposite is true
                    
                    Player_Shoot = current_square + d_list[d_index]
                    if can_shoot(PrevPlayerShoots, Player_Shoot) == False:
                        mode = "hunt"
                    else:
                        if gridPlayerA[Player_Shoot] == 1:
                            shoot_Touched(gridGamePlayerA, Player_Shoot) 
                            BoatTouchedByPlayer = BoatTouchedByPlayer + 1
                        else:
                            shoot(gridGamePlayerA, Player_Shoot)
                            mode = "hunt"

        print("base, current: ", base_square, PrevPlayerShoots[-1])
        for i in range(10):
            print(gridGamePlayerA[i*10:i*10+10])

        print("==============================================================================================================================")
        total_shots += 1        


    return total_shots, BoatTouchedByPlayer


def Strat2(gridPlayerA):
    BoatTouchedByPlayer = 0     
    PrevPlayerShoots = []
    total_shots = 0
    mode = "hunt"
    firstHuntSquare = []
    d_index = 0
    dFirstShot = False
    d_list = [-1, -10, 1, 10]
    base_square = 0
    current_square = 0
    dOpposite = False
    dSpecialOp = False # when first square hit is an edge case

    last_shot = 0

    print("INITIAL BOARD")
    for i in range(10):
        print(gridPlayerA[i*10:i*10+10])

    while (BoatTouchedByPlayer < 14):
        # for i in range(10):
        #   print(gridGamePlayerA[i*10:i*10+10]) 
        Player_Shoot = random.randint(0, 99)
        while can_shoot(PrevPlayerShoots, Player_Shoot) == False:
            Player_Shoot = random.randint(0, 99)
        #last_shot = Player_Shoot
        if mode == "hunt":
            print("mode = Hunt")
            if gridPlayerA[Player_Shoot] == 1:
                #print("IA touched one of your boat")
                shoot_Touched(gridGamePlayerA, Player_Shoot) 
                firstHuntSquare.append(Player_Shoot)
                dFirstShot = True
                d_index = 0
                dOpposite = False
                #print(gridPlayerB)
                BoatTouchedByPlayer = BoatTouchedByPlayer + 1

                mode = "destroy"

            else:
                shoot(gridGamePlayerA, Player_Shoot)


        else: ## ELSE if mode is DESTROY
            print("mode = DESTROY")
            print("FIRST SHOT: ", dFirstShot)
            if dFirstShot == True: # FIRST SHOT
                base_square = firstHuntSquare[-1]
                
                Player_Shoot = d_list[d_index] + base_square
                while can_shoot(PrevPlayerShoots, Player_Shoot) == False:
                    print(d_index)
                    d_index += 1
                    Player_Shoot = d_list[d_index] + base_square
                if gridPlayerA[Player_Shoot] == 1:
                    shoot_Touched(gridGamePlayerA, Player_Shoot) 
                    BoatTouchedByPlayer = BoatTouchedByPlayer + 1
                    dFirstShot = False
                else:
                    shoot(gridGamePlayerA, Player_Shoot)
                



            else: # Shots after the first
                
                print("dOpp", dOpposite)
                base_square = firstHuntSquare[-1]
                current_square = PrevPlayerShoots[-1]
                print("current b4: ", current_square)
                if dOpposite == False:
                    Player_Shoot = current_square + d_list[d_index]
                    if can_shoot(PrevPlayerShoots, Player_Shoot) == False:
                        d_index *= -1  # attacks in opposite direction
                        dOpposite = True
                        total_shots -= 1 # reduce a turn
                        
                    else:
                        if gridPlayerA[Player_Shoot] == 1:
                            shoot_Touched(gridGamePlayerA, Player_Shoot) 
                            BoatTouchedByPlayer = BoatTouchedByPlayer + 1
                        else:
                            d_index *= -1  # attacks in opposite direction
                            dOpposite = True
                            shoot(gridGamePlayerA, Player_Shoot)

                else: # if dopposite is true
                    
                    Player_Shoot = current_square + d_list[d_index]
                    if can_shoot(PrevPlayerShoots, Player_Shoot) == False:
                        mode = "hunt"
                    else:
                        if gridPlayerA[Player_Shoot] == 1:
                            shoot_Touched(gridGamePlayerA, Player_Shoot) 
                            BoatTouchedByPlayer = BoatTouchedByPlayer + 1
                        else:
                            shoot(gridGamePlayerA, Player_Shoot)
                            mode = "hunt"

        print("base, current: ", base_square, PrevPlayerShoots[-1])
        for i in range(10):
            print(gridGamePlayerA[i*10:i*10+10])

        print("==============================================================================================================================")
        total_shots += 1        


    return total_shots, BoatTouchedByPlayer
    
def shoot_Touched(grid, shot):
    grid.pop(shot)
    grid.insert(shot, 'F')


def shoot(grid, shot):
    grid.pop(shot)
    grid.insert(shot, 'X')
    

def End_Game(grid):
    if grid == "IA":
        if grid == 14: # if IA has touched all the player's boat
            OnGame = False #turn off the game
            print("Too bad, IA has won !")
        
    elif grid == "Player":    
        if grid == 14:
            OnGame = False #turn off the game
            print("Wow, you have won !")



def can_shoot(List, shot):
    for x in range(len(List)):#check if the shoot didnt already done
        if List[x] == shot:
            #print("you've already shoot here !")
            return False
    List.append(shot)        
    return True


def put_boats(grid):
    for n in range(2,6):
        x, y, direction = random.randint(0,9), random.randint(0,9), random.randint(0,1)
        while cant_put_boat(n, x, y, direction, grid):
            x, y, direction = random.randint(0,9), random.randint(0,9), random.randint(0,1)
        put_boat(n, x, y, direction, grid)
            


def put_boat(length, x, y, direction, grid):
    if direction == 0: # HORIZ direction
        for i in range(length):
            position = x+i + 10*y
            grid[position] = 1
            

    if direction == 1: # VERT direction
        for i in range(length):
            position = x + 10*(y+i)
            grid[position] = 1
  
def clear_board(grid):
  for i in range(100):
    grid[i] = 0
            

def cant_put_boat(length, x, y, direction, grid):
    return direction == 0 and x + length >= 10 or direction == 1 and y + length >= 10


main()