def bfs(current,target):                    #### used for going from one safe path to another 
    # print(safe_spaces)                 #### using the safe_spaces list which keeps track of all the safe paths
    visited = []
    for i in range(4):                                      #maintaining the visited list 
        visited.append([False,False,False,False])
    q = []
    cordList = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]
    dirn = dict.fromkeys(cordList,(None,None))
    dirn = {(current[0],current[1]):(None,None)}             #used for keeping track of the dirnections moved
    q.append((current[0],current[1]))
    visited[current[0]][current[1]]=True                    
    while q:
        s = q.pop(0)
        # print(s)
        # time.sleep(1)
        target_moves = []
        if s[0]==target[0] and s[1]==target[1]:             #checking if target has been reached 
            break
        for i in range(4):
            newr = s[0]+allowed_moves[i][0]
            newc = s[1]+allowed_moves[i][1]
            if checkCords(newr,newc) and safe_spaces[newr][newc]==1 and visited[newr][newc]==False:   #checking if next move is checkCords
                visited[newr][newc]=True                    #update the visited list 
                q.append((newr,newc))
                target_moves.append(moves[i])
                #dirn[(newr,newc)]=((s[0],s[1]),moves[i])

    
    top = (target[0],target[1])
    #while top!=(current[0],current[1]):
        #print(dirn[(current[0],current[1])])                                #adding the moves taken to reach the target
        #target_moves.append(dirn[top][1])
        #top = dirn[top][0]
    
    target_moves.reverse()                                  #reversing the list to get the correct order 
    return target_moves