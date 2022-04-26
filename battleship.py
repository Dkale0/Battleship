import random
import copy
import numpy

gridPlayerA = [0] * 100 #IA's grid
gridPlayerB = [0] * 100 #Player's grid


gridGamePlayerA = [0] * 100 # just create a copy of the IA boards and only show the empty board
gridGamePlayerB = [0] * 100 


OnGame = True # turn on the game

PrevPlayerShoots = []
PrevIAShoots = []


def main():
  strategyOne = []
  for a in range(1):
    clear_board(gridPlayerA) 
    clear_board(gridPlayerB)
    clear_board(gridGamePlayerA) 
    clear_board(gridGamePlayerB)
    PrevPlayerShoots = []
    PrevIAShoots = [] 

    
    put_boats(gridPlayerA)#put IA's boats randomly
    while sum(gridPlayerA) != 14:
      clear_board(gridPlayerA) 
      put_boats(gridPlayerA)

    result = ConseqStrategy(gridPlayerA=gridPlayerA)

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
        #print("temp, BoatTouched: ", temp, BoatTouchedByPlayer)
    for i in range(10):
      print(gridGamePlayerA[i*10:i*10+10])
    return temp, BoatTouchedByPlayer

# def RandomStrategy():
#     BoatTouchedByIA = 0
#     PrevIAShoots = []
#     clear_board
#     while (BoatTouchedByIA < 14):
#         IA_shot = random.randint(0, 99) 
#             while can_shoot(PrevIAShoots, IA_shot) == False:
#                 IA_shot = random.randint(0, 99)


#             if gridPlayerB[IA_shot] == 1:
#                 #print("IA touched one of your boat")
#                 shoot_Touched(gridGamePlayerB, IA_shot) 
#                 #print(gridPlayerB)
#                 BoatTouchedByIA = BoatTouchedByIA + 1 

#             else:
#                 shoot(gridGamePlayerB, IA_shot) # replace the shoot by an X
#                 #print("Lucky, IA missed !")


def HuntDestroy():
    BoatTouchedByPlayer = 0
    BoatTouchedByIA = 0
      
    PrevPlayerShoots = []
    PrevIAShoots = [] 
    clear_board(gridPlayerA)
    put_boats(gridPlayerA)#put IA's boats randomly

    total_shots = 0
    while sum(gridPlayerA) != 14:
      clear_board(gridPlayerA) 
      put_boats(gridPlayerA)
      #print(sum(gridPlayerA))

    # deepcopy grid A to grid B (so boats orientations are that same on both grids)
    gridPlayerB = copy.deepcopy(gridPlayerA) 
    mode = "hunt"
    # for i in range(10):
    #   print(gridPlayerA[i*10:i*10+10]) # print the IA's grid (with no boats)
    # print("SUM: ", sum(gridPlayerA))
    firstHuntSquare = []
    d_index = 0
    dFirstShot = False
    d_list = [-1, -10, 1, 10]
    dOpposite = False
    while (BoatTouchedByIA < 14) and (BoatTouchedByPlayer < 14):
        # for i in range(10):
        #   print(gridGamePlayerA[i*10:i*10+10]) 
        Player_Shoot = random.randint(0, 99)
        while can_shoot(PrevPlayerShoots, Player_Shoot) == False:
            Player_Shoot = random.randint(0, 99)

        if mode == "hunt":
            if gridPlayerA[Player_Shoot] == 1:
                #print("IA touched one of your boat")
                shoot_Touched(gridGamePlayerA, Player_Shoot) 
                firstHuntSquare.append(Player_Shoot)
                dFirstShot = True
                d_index = 0
                #print(gridPlayerB)
                BoatTouchedByPlayer = BoatTouchedByPlayer + 1

                mode = "destroy"

            else:
                shoot(gridGamePlayerA, Player_Shoot)

                ## IA STEP

                #TODO: IA SHIT

        if mode == "destroy":
            if dFirstShot == True: # FIRST SHOT
                current_square = firstHuntSquare[-1]
                
                Player_Shoot = d_list[d_index] + current_square
                while can_shoot(PrevPlayerShoots, Player_Shoot) == False:
                    d_index += 1
                    Player_Shoot = d_list[d_index] + current_square
                if gridPlayerA[Player_Shoot] == 1:
                    shoot_Touched(gridGamePlayerA, Player_Shoot) 
                    BoatTouchedByPlayer = BoatTouchedByPlayer + 1
                else:
                    shoot(gridGamePlayerA, Player_Shoot)

                    ## IA STEP

                    #TODO: IA SHIT



            else: # Shots after the first
                base_square = firstHuntSquare[-1]
                current_square = PrevPlayerShoots[-1]
                if dOpposite == False:
                    Player_Shoot = current_square + d_list[d_index]

                else:
                    Player_Shoot = 6
                    if can_shoot(PrevPlayerShoots, Player_Shoot) == False:
                        a = 3
                
            

            
            


            

                

    total_shots = 1

    return total_shots, BoatTouchedByPlayer, BoatTouchedByIA
    
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