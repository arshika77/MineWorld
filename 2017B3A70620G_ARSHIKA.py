#!/usr/bin/env python3
from Agent import * # See the Agent.py file
from pysat.solvers import Glucose3
import itertools
from collections import deque
import copy
from time import sleep
#### All your code can go here.

#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.

rowNum = [-1, 0, 0, 1]
colNum = [0, -1, 1, 0]                    
actionToTake = ['Left','Down','Up','Right']
 
# A data structure for queue used in BFS
class queueNode:
    def __init__(self,pt, dist, dirn):
        self.pt = pt  # The cordinates of the cell
        self.x = pt[0]
        self.y = pt[1]
        self.dist = dist  # Cell's distance from the source
        self.dirn = dirn

def generateNeighbours(currValue):
    nbrs = []
    i = currValue[0]
    j = currValue[1]

    iu = i
    ju =j+1

    idw = i
    jdwn = j-1

    il = i-1
    jl = j

    ir = i+1
    jr = j

    if (ju<=4):
        nbrs.append([iu,ju])
    if (jdwn>0):
        nbrs.append([idw,jdwn])
    if (il>0):
        nbrs.append([il,jl])
    if (ir<=4):
        nbrs.append([ir,jr])

    return nbrs

def checkCords(x,y):
    if (x>0 and x<=4 and y>0 and y<=4):
        return True
    else:
        return False

def bfs(safe_spaces,curr_loc,next_loc):
    visited = [0]*17
    index_src = 4*(curr_loc[0]-1)+curr_loc[1]

    visited[index_src] = 1
    q = deque()

    node = queueNode(curr_loc,0,None)
    q.append(node)

    cordList = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]
    moves_dict = dict.fromkeys(cordList,[None,None])
    moves_dict = {(node.x,node.y):[node.dirn,None]}

    while q:
        curr_node = q.popleft()
        curr_cords = curr_node.pt

        if (curr_cords == next_loc):
            break

        for i in range(4):
            row = curr_node.x + rowNum[i]
            col = curr_node.y + colNum[i]

            if (checkCords(row,col)):
                if (safe_spaces[row-1][col-1]==1 and visited[4*(row-1)+col]==0):
                    visited[4*(row-1)+col]=1
                    Adjcell = queueNode([row,col], curr_node.dist+1,actionToTake[i])
                    q.append(Adjcell)
                    moves_dict[(Adjcell.x,Adjcell.y)] = [Adjcell.dirn,(curr_node.x,curr_node.y)]

    target_moves = []
    target = next_loc
    while target != curr_loc :
        target_moves.append(moves_dict[(target[0],target[1])][0])
        if (moves_dict[(target[0],target[1])][1] != None):
            target = moves_dict[(target[0],target[1])][1]
        else:
            break

    target_moves.reverse()
    return target_moves


def generateIndex(x,y):
    return 4*(x-1)+y


def navigateMineWorld(verbose,kb,ag):

    if (verbose==True):
        print("Initiaization of the knowledge base is complete. Starting the simulation...\n")
        sleep(2.5)

    safeCells = [[1,1]] # List to store all the safe cells while traversing
    safe_spaces = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    safe_spaces[0][0] = 1 # Mark the start as safe
    safe_spaces[3][3] = 1 # Mark the exit as safe

    visited = [0]*17
    visited[1] = 1

    path_taken = [[1,1]]

    while(ag.FindCurrentLocation()!=[4,4]):

        curr_loc = safeCells.pop()
        if (verbose==True):
            print("\nCurrent location: ",curr_loc)
            sleep(2.5)
        # Perceive the environment of the current cell and add it to the knowledge base
        percept = ag.PerceiveCurrentLocation()
        if (verbose==True):
            print("\nPercept at the current location: ",percept)
            sleep(2.5)
        # percept0 => NoMineL & NoMineR & NoMineU & NoMineD
        # percept1 => MineL or MineR or MineU or MineD; MineL => NoMineR & NoMineU & NoMineD (Similary for all 4)
        # percept>1 => MineL or MineR or MineU or MineD; MineL => MineR or MineU or MineD (Similary for all 4)

        # ~p0 or NoMineL, ~po or NoMineR, ~po or NoMineU, ~po or NoMineD
        # ~p1 or MineL or MineR or MineU or MineD; NoMineL or NoMineR; NoMineL or NoMineU; NoMIneL or NoMineD;...
        # ~p>1 or MineL or MineR or MineU or MineD; NoMineL or MineR or MineU or MineD;...
        
        nbrs = generateNeighbours(curr_loc)
        if (verbose==True):
            print("\nNeighbouring locations: ")
            print(*nbrs,sep=' & ')
            sleep(2.5)

        if (percept == '=0'):
            clause_num = 16 + 4*(curr_loc[0]-1) + curr_loc[1]
            kb.add_clause([clause_num])

            # ~p0 or NoMineL, ~po or NoMineR, ~po or NoMineU, ~po or NoMineD
            neg_clause = -1 * clause_num
            for nbr in nbrs:
                new_clause = [neg_clause]
                index = generateIndex(nbr[0],nbr[1])
                new_clause.append(index)
                kb.add_clause(new_clause)

        elif (percept == '=1'):
            clause_num = 32 + 4*(curr_loc[0]-1) + curr_loc[1]
            kb.add_clause([clause_num])

            # ~p1 or MineL or MineR or MineU or MineD; NoMineL or NoMineR; NoMineL or NoMineU; NoMIneL or NoMineD;...
            neg_clause = -1 * clause_num
            new_clause = [neg_clause]
            for nbr in nbrs:
                index = -1 * generateIndex(nbr[0],nbr[1])
                new_clause.append(index)
            kb.add_clause(new_clause)
            if (len(nbrs)==2):
                kb.add_clause([generateIndex(nbrs[0][0],nbrs[0][1]),generateIndex(nbrs[1][0],nbrs[1][1])])
            elif (len(nbrs)==3):
                kb.add_clause([generateIndex(nbrs[0][0],nbrs[0][1]),generateIndex(nbrs[1][0],nbrs[1][1])])
                kb.add_clause([generateIndex(nbrs[0][0],nbrs[0][1]),generateIndex(nbrs[2][0],nbrs[2][1])])
                kb.add_clause([generateIndex(nbrs[1][0],nbrs[1][1]),generateIndex(nbrs[2][0],nbrs[2][1])])
            elif (len(nbrs)==4):
                kb.add_clause([generateIndex(nbrs[0][0],nbrs[0][1]),generateIndex(nbrs[1][0],nbrs[1][1])])
                kb.add_clause([generateIndex(nbrs[0][0],nbrs[0][1]),generateIndex(nbrs[2][0],nbrs[2][1])])
                kb.add_clause([generateIndex(nbrs[0][0],nbrs[0][1]),generateIndex(nbrs[3][0],nbrs[3][1])])
                kb.add_clause([generateIndex(nbrs[1][0],nbrs[1][1]),generateIndex(nbrs[2][0],nbrs[2][1])])
                kb.add_clause([generateIndex(nbrs[1][0],nbrs[1][1]),generateIndex(nbrs[3][0],nbrs[3][1])])
                kb.add_clause([generateIndex(nbrs[2][0],nbrs[2][1]),generateIndex(nbrs[3][0],nbrs[3][1])])

        elif (percept == '>1'):
            clause_num = 48 + 4*(curr_loc[0]-1) + curr_loc[1]
            kb.add_clause([clause_num])

            # ~p>1 or MineL or MineR or MineU or MineD; NoMineL or MineR or MineU or MineD;...
            neg_clause = -1 * clause_num
            new_clause = [neg_clause]
            for nbr in nbrs:
                index = -1 * generateIndex(nbr[0],nbr[1])
                new_clause.append(index)
            kb.add_clause(new_clause)

            for nbr in nbrs:
                index = generateIndex(nbr[0],nbr[1])
                supp_clause = [index]
                for othernbrs in nbrs:
                    if (nbr==othernbrs):
                        continue
                    supp_index = -1 * generateIndex(othernbrs[0],othernbrs[1])
                    supp_clause.append(supp_index)
                kb.add_clause(supp_clause)

        # Analyse all the nbrs of the current location and determine if a mine is present in any of them 
        if (verbose==True):
            print("\nAnalysing all the non-visited neighbours and determining if a mine is present in any of them")
            sleep(0.5)
        for nbr in nbrs:
            index = 4*(nbr[0]-1) + nbr[1]
            if (visited[index]==1):
                continue
            if (verbose==True):
                print("\nAnalyzing neighbour: ",nbr)
                sleep(1.0)
            visited[index] = 1
            neg_index = -1 * index

            # clause index => no mine in nbr
            # kb |= index iff kb & ~index is a contradiction
            if (verbose==True):
                print("\nKB and not(\"No mine in this neighbour\")?: ",kb.solve(assumptions=[neg_index]))
                sleep(1.0)
            if(kb.solve(assumptions=[neg_index])==False):
                # No mine in this neighbour
                # Mark this neighbour as safe
                if (verbose==True):
                    print("\nNo mine in this neighbour")
                    sleep(0.5)
                safeCells.append(nbr)
                safe_spaces[nbr[0]-1][nbr[1]-1] = 1
                kb.add_clause([index])
            elif(kb.solve(assumptions=[neg_index])==True):
                # The knowledge based cannot eliminate a mine in this cell
                # clause neg_index => A mine in nbr
                # kb |= neg_index iff kb & index is a contradiction
                if(kb.solve(assumptions=[index])==False):
                    # There is a mine in this neighbour
                    # Mark this neighbour as unsafe
                    safe_spaces[nbr[0]-1][nbr[1]-1] = -1
                    kb.add_clause([neg_index])
                    # If true, we cannot do any analysis at this point about this neighbour

        if len(safeCells)==0:
            if (verbose==True):
                    print("\nAll available safe cells explored. Backtracking to the starting location...\n")
                    sleep(0.5)                                              
            safeCells.append([1,1])
            visited = [0]*17

        if ([4,4] in nbrs):
            next_loc = [4,4]
        else:
            next_loc = safeCells[-1]
        route = bfs(safe_spaces,curr_loc,next_loc) # This will return the sequence of actions the agent should take to go to the new location
        
        for step in route:
            if (step==None):
                continue
            ag.TakeAction(step)
            print("\n")
            path_taken.append(ag.FindCurrentLocation())

    print("Path taken by the agent is: ")
    print(*path_taken,sep='-->')   



def initializeKB(verbose,kb,ag):

    if (verbose==True):
        print("Initializing the knowledge base\n")
        sleep(2.5)

    # The agent is at location [1,1] right now

    # There is no mine in [1,1] and [4,4] (Trivially true since an exit is always guaranteed)
    if (verbose==True):
        print("We first add the \"No mine in [1,1]\" clause and \"No mine in [4,4]\" clause to our knowledge base since these clauses are trivially true\n")
        sleep(2.5)
    kb.add_clause([1])
    kb.add_clause([16])

#    # There are atleast two mines
    if (verbose==True):
        print("Adding the clause \"Atleast two mines\" to the knowledge base\n")
        sleep(2.5)
    for i in range(1,5):
        for j in range(1,5):
            # If there is a mine in coordinate [i,j] (-x), then there is a mine in either [1,1] or [1,2] or ... [4,4]
            # -x => (-1 or -2 or -3 ... or -16) {Conclusion does not contain -x}
            # x or -1 or -2 or -3 ... or -16 
            first_mine = 4*(i-1)+j
            clause_list = []
            for i in range(1,17):
                if (i != first_mine):
                    clause_list.append(-1 * i)
            clause_list.append(first_mine)
            kb.add_clause(clause_list)

    # There are atmost 5 mines
    # -1 & -2 & -3 & -4 & -5 => 6 & 7 & 8 & 9 & .. 15
    # 1 or 2 or 3 or 4 or 5 or 6, 1 or 2 or 3 or 4 or 5 or 7 ...
    if (verbose==True):
        print("Adding the clause \"Atmost five mines\" to the knowledge base\n")
        sleep(2.5)
    comb = itertools.combinations([1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15,16], 6)
    for i in list(comb):
        clause_list = list(i)
        kb.add_clause(clause_list)

    # We have now perceived all background knowledge.
    if (verbose==True):
        print("We have now perceived all background knowledge\n")
        sleep(2.5)
    #print("Solvable?: ",kb.solve())
    #print(kb.get_model())
    if (verbose==True):
        print("The agent is at location [1,1] right now\n")
        sleep(2.5)

def main():

    print("\n")
    print("         OOO        ")
    print(" -------------------")
    print(" -   @           @ -")
    print(" -                 -")
    print(" -    ----------   -")
    print(" -   \\          /  -")
    print(" -    ----------   -")
    print(" -------------------")
    print("\nWelcome to the simulation for the mine world. This program will attempt to help this robot navigate a dangerous mine world and exit it safely!\n")

    print("Do you wish to run the bare-bones version of the program or the verbose version?[Note: Choosing the verbose version will significantly slow down the program to facilitate a step-by-step simulation]")
    userinput =input("Enter b for the basic version and v for the verbose version [b\\v]: \n")
 
    if (userinput=='v'):
        verbose = True
    else:
        verbose = False

    print("You have set the verbose setting in the program as",verbose)
    confirmChoice = input("CONFIRM CHOICE: Do you wish to change your choice? [y\\n]: \n")

    if (confirmChoice=='y'):
        if (userinput=='v'):
            userinput='b'
            verbose = False
        else:
            userinput ='v'
            verbose = True
        print("Choice changed. Verbose set to",verbose)
    else:
        print("Choice confirmed")

    print("\nProceeding with the simulation...\n")

    # [Mine,Percept 0, Percept 1, Percept >1]
    # No mine in cell [i,j] = 4*(i-1) + j
    # Percept 0 in cell [i,j] = 16 + 4*(i-1) + j
    # Percept 1 in cell [i,j] = 32 + 4*(i-1) + j
    # Percept >1 in cell [i,j] = 48 + 4*(i-1) + j
    # Number of literals = 64 positive literals + 64 negative literals = 128 literals

    kb = Glucose3()
    ag = Agent()
    initializeKB(verbose,kb,ag)
    navigateMineWorld(verbose,kb,ag)

if __name__=='__main__':
    main()
