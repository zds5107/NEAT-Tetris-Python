from piece import Piece

class TPiece(Piece):
    def __init__(self):
        super().__init__(5)
        self.cords = [[3,0], [4,0], [5,0], [4,1]]   
        
class OPiece(Piece):
    def __init__(self):
        super().__init__(6)
        self.cords = [[4,0], [5,0], [4,1], [5,1]]

    def rotate(self):
        return None

class LPiece(Piece):
    def __init__(self):
        super().__init__(2)
        self.cords = [[3,0], [4,0], [5,0], [3,1]]

class JPiece(Piece):
    def __init__(self):
        super().__init__(4)
        self.cords = [[3,0], [4,0], [5,0], [5,1]]

class SPiece(Piece):
    def __init__(self):
        super().__init__(7)
        self.cords = [[3,1], [4,1], [4,0], [5,0]]

class ZPiece(Piece):
    def __init__(self):
        super().__init__(1)
        self.cords = [[4,0], [4,1], [5,1],[3,0]]

class IPiece(Piece):
    def __init__(self):
        super().__init__(3)
        self.cords = [[3,0], [5,0], [4,0], [6,0]]
        self.state = 1

    def rotate(self):
        newcords = self.cords[:]
        xn = newcords[1][0]
        yn = newcords[1][1]

        for i in range(4):
            newX = newcords[i][0] - xn
            newY = newcords[i][1] - yn
            newcords[i] = [-1*self.state*newY+xn, self.state*newX+yn] 

        return newcords
   
