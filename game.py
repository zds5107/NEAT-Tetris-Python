from board import Board
from pieces import *
from board import Board
import random

class Game:
    def __init__(self):
        self.board = Board()
        self.bag = [IPiece(), JPiece(), LPiece(), OPiece(), TPiece(), SPiece(), ZPiece()]
        self.cur_piece = random.choice(self.bag)
        self.state = 1
        self.score = 0

    def rotate(self):
        newcords = self.cur_piece.rotate()

        if newcords != None and not self.blocked(newcords):
            self.cur_piece.cords = newcords 
            if isinstance(self.cur_piece, IPiece):
                self.cur_piece.state *= -1

    def down(self):
        newcords = self.cur_piece.cords[:]
        for i in range(len(newcords)):
            newcords[i] = [newcords[i][0], newcords[i][1]+1] 

        if not self.blocked(newcords):
            self.cur_piece.cords = newcords
        else:
            self.lock()
        
    def left(self):
        newcords = self.cur_piece.cords[:]
        for i in range(len(newcords)):
            newcords[i] = [newcords[i][0]-1, newcords[i][1]]

        if not self.blocked(newcords):
            self.cur_piece.cords = newcords     

    def right(self):
        newcords = self.cur_piece.cords[:]
        for i in range(len(newcords)):
            newcords[i] = [newcords[i][0]+1, newcords[i][1]]

        if not self.blocked(newcords):
            self.cur_piece.cords = newcords   

    def blocked(self, newcords):
        for cord in newcords:
            if cord[1] > 19 or cord[0] < 0 or cord[0] > 9:
                return True
            elif self.board.board[cord[1]][cord[0]] != 0:
                if cord[1] > 0:
                    return True
        return False

    def lock(self):

        id_to_piece = {
            1: ZPiece,
            2: LPiece,
            3: IPiece,
            4: JPiece,
            5: TPiece,
            6: OPiece,
            7: SPiece
        }


        for cord in self.cur_piece.cords:
            self.board.board[cord[1]][cord[0]] = self.cur_piece.id

        self.bag.remove(self.cur_piece)

        if len(self.bag) == 0:
            for i in range(7):
                
                self.bag.append(id_to_piece[random.randint(1,7)]())


            #self.bag = [IPiece(), JPiece(), LPiece(), OPiece(), TPiece(), SPiece(), ZPiece()]
        
        self.cur_piece = self.cur_piece = random.choice(self.bag)
        self.clear_check()
       

    def clear_check(self):
        
        count=0
        for i in range(len(self.board.board)-1,-1,-1):
            if all(element != 0 for element in self.board.board[i]):
                count+=1
                self.board.board[i] = [0 for j in range(10)]  
            else:
                if count > 0:
                    self.board.board[i+count] = self.board.board[i]
                    self.board.board[i] = [0 for j in range(10)]


        if count > 0:
            if count == 1:
                self.score += 1
            if count == 2:
                self.score += 2
            if count == 3:
                self.score += 3
            if count == 4:
                self.score += 4
            
            

        self.gameover_check()

    def gameover_check(self):

        for cord in self.cur_piece.cords:
            if self.board.board[cord[1]][cord[0]] != 0:
                self.state = 0
        

        if self.state !=0:            
            self.state=1