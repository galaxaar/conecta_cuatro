from board import Board
from list_utils import displace_list
from game import Game

if __name__ == "__main__":
    game = Game()
    game.start()


    # Crear un board
    b = Board()
    
    #Victoria vertical


    
    matrix =[["x", "x", "x", None], ["o", "x", "o", None], ["o", "o", None, None ], ["x", None, None, None]] 
    print(b.print_board(matrix))
    print(b._has_vertical_victory(matrix, "x"))