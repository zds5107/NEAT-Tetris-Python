from game import Game

def calculate_features(board):
    columns = []
    for i in range(len(board[0])):
        col = [row[i] for row in board]
        columns.append(col)
    
    #Max Height
    height_data=[]
    for col in range(len(columns)):
        for elm in range(len(columns[0])):
            if columns[col][elm] != 0:
                height_data.append(20-elm)
                break

            if elm == 19:
                height_data.append(0)

    agHeight = sum(height_data)

    #Height Differential
    hd=0
    
    for i in range(len(height_data)-1):
        hd += abs(height_data[i]-height_data[i+1])
    
    height_data.insert(0,20)
    height_data.append(20)
    wells =0
    for i in range(1, len(height_data)-1):
        if min(height_data[i-1] , height_data[i+1]) - height_data[i] >= 3:
            wells+=1

    #Holes
    holes = 0
    for col in columns:
        capped=False
        for elm in col:
            if elm !=0:
                capped = True
            else:
                if capped:
                    holes+=1

    return (holes, 0, hd, agHeight, 0, wells)


def calculate_moves(board, piece_id):
    
    starting_locations = {
       1 : [[[1,0], [1,1], [2,1],[0,0]],
            [[1,0], [1,1], [0,1],[0,2]]],
       
       2 : [[[0,0], [1,0], [2,0], [0,1]],
            [[0,0], [1,0], [1,1], [1,2]],
            [[0,1], [1,1], [2,0], [2,1]],
            [[0,0], [0,1], [0,2], [1,2]]],
       
       3 : [[[0,0], [1,0], [2,0], [3,0]],
            [[0,0], [0,1], [0,2], [0,3]]],
       
       4 : [[[0,0], [1,0], [2,0], [2,1]],
            [[0,2], [1,0], [1,1], [1,2]],
            [[0,0], [0,1], [1,1], [2,1]],
            [[0,0], [0,1], [0,2], [1,0]]],
       
       5 : [[[0,0], [1,0], [2,0], [1,1]],
            [[1,0], [0,1], [1,1], [1,2]],
            [[1,0], [0,1], [1,1], [2,1]],
            [[0,0], [0,1], [1,1], [0,2]]],
       
       6 : [[[0,0], [1,0], [0,1], [1,1]]],
       
       7 : [[[0,1], [1,1], [1,0], [2,0]],
            [[0,0], [0,1], [1,1], [1,2]]]
    }

    shift_ranges = {
        1 : [8,9],
        2 : [8,9,8,9], 
        3 : [7,10],
        4 : [8,9,8,9],
        5 : [8,9,8,9],
        6 : [9],
        7 : [8,9]
    }

    boards = []
    feature_sets = []
    moves = []
    rotational_starts = starting_locations[piece_id]
    shifts = shift_ranges[piece_id]

    initial_features = calculate_features(board)
    
    #for each possible rotation given the current piece
    for i in range(len(rotational_starts)):
        
        #for each possible shift
        for j in range(shifts[i]):
            possible = [[cord[0]+j,cord[1]] for cord in rotational_starts[i]]
            

            if not all(board[cord[1]][cord[0]] == 0 for cord in possible):
                continue


            #drop piece into the current slot
            while all(cord[1]+1 <= 19 for cord in possible) and all(board[cord[1]+1][cord[0]] == 0 for cord in possible):
                for k in range(len(possible)):
                    possible[k][1] = possible[k][1] +1

            lowest = possible[0][1]
            for cord in possible:
                if cord[1] < lowest:
                    lowest = cord[1]



            #set piece to the board
            bc = [row[:] for row in board]
            for l in range(len(possible)):
                 bc[possible[l][1]][possible[l][0]] = piece_id

            #clear lines if possible
            count=0
            for m in range(19,-1,-1):
                if all(element != 0 for element in bc[m]):
                    count+=1
                    bc[m] = [0 for j in range(10)]  
                else:
                    if count > 0:
                        bc[m+count] = bc[m]
                        bc[m] = [0 for j in range(10)]
                
            feature_set = calculate_features(bc)
            boards.append([row[:] for row in bc]) 
            moves.append([i,j])

            feature_sets.append(((feature_set[0]-initial_features[0]), 
                                 count, 
                                 (feature_set[2]-initial_features[2]), 
                                 (feature_set[3]),
                                 lowest,
                                 (feature_set[5])))
    
    return feature_sets, moves, boards