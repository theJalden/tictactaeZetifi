from enum import Enum

class STATES(Enum):
        CROSS_TURN = 0
        NAUGHT_TURN = 1
        DRAW = 2
        CROSS_WON = 3
        NAUGHT_WON = 4

class TicTacToe:

    def __init__(self):
        # The tic tac toe board is a 3x3 array of one of the following symbols:
        # '' - blank spot
        # 'x' - cross
        # 'o' - naught
        self.board = [['','',''], ['','',''], ['','','']]
        self.state = STATES.CROSS_TURN
    
    
    def place_marker(self, symbol: str, row: int, column: int):
        """Adds a symbol to the board, does nothing if improper parameters"""
        if (symbol == 'x' and self.state == STATES.CROSS_TURN or 
            symbol == 'o' and self.state == STATES.NAUGHT_TURN):
            # the spot is empty
            if self.board[row][column] == '':
                self.board[row][column] = symbol

                # Move to the next state
                self.update_state()

    def update_state(self):
        """
        First checks if there's been a win if there has the win goes to
        whoever's turn it was (x or o)

        Then checks for a draw

        if the game is neither won nor drawn the turn alternates from
        x to o or vice versa
        """
        if self.check_win():
            if self.state == STATES.CROSS_TURN:
                self.state = STATES.CROSS_WON
            elif self.state == STATES.NAUGHT_TURN:
                self.state = STATES.NAUGHT_WON
        elif self.check_draw():
            self.state = STATES.DRAW
        elif self.state == STATES.CROSS_TURN:
            self.state = STATES.NAUGHT_TURN
        elif self.state == STATES.NAUGHT_TURN:
            self.state = STATES.CROSS_TURN
        
    def check_draw(self) -> bool:
        """returns true if there is no blank spot on the board"""
        return ('' not in self.board[0] and
                '' not in self.board[1] and
                '' not in self.board[2])


    def check_win(self) -> bool:
        """
        Checks the board for a Cross or Naught win
        (3 in a row, column, or diagonal)

        returns true if there is a win, false otherwise
        """
        x_win = ['x', 'x', 'x']
        o_win = ['o', 'o', 'o']

        # check rows
        if x_win in self.board or o_win in self.board:
            return True
        # check columns
        col0 = [self.board[0][0], self.board[1][0], self.board[1][0]]
        col1 = [self.board[0][1], self.board[1][1], self.board[1][1]]
        col2 = [self.board[0][2], self.board[1][2], self.board[1][2]]
        if x_win in [col0, col1, col2] or o_win in [col0, col1, col2]:
            return True
        # check diagonals
        d1 = [self.board[0][0], self.board[1][1], self.board[2][2]]
        d2 = [self.board[2][0], self.board[1][1], self.board[0][2]]
        if x_win == d1 or x_win == d2 or o_win == d1 or o_win == d2:
            return True 

        # no wins
        return False


    def print_board(self):
        """Prints the current gameboard to the console/stdout"""
        for xx, row in enumerate(self.board):
            rString = ""
            for yy, col in enumerate(row):
                if col == '':
                    rString += " " # use a space instead of empty
                else:
                    rString += col
                
                if yy < 2: # don't do the last time
                    rString += "|"
            print(rString)
            if xx < 2: # don't do the last time\
                print("-----")

# Unit testing
import unittest
class TestTicTacToe(unittest.TestCase):
    def test_init(self):
        myGame = TicTacToe()
        self.assertEqual(myGame.state, STATES.CROSS_TURN)
        self.assertEqual(myGame.board, [['','',''],['','',''],['','','']])

    def test_place_marker(self):
        myGame = TicTacToe()
        myGame.place_marker('x', 0, 0)
        self.assertEqual(myGame.state, STATES.NAUGHT_TURN)
        self.assertEqual(myGame.board, [['x','',''],['','',''],['','','']])

    def test_wrong_symbol_place_marker(self):
        myGame = TicTacToe()
        myGame.place_marker('o', 0, 0)
        self.assertEqual(myGame.state, STATES.CROSS_TURN)
        self.assertEqual(myGame.board, [['','',''],['','',''],['','','']])

    def test_occupied_place_marker(self):
        myGame = TicTacToe()
        myGame.place_marker('x', 0, 0)
        myGame.place_marker('o', 0, 0)
        self.assertEqual(myGame.state, STATES.NAUGHT_TURN)
        self.assertEqual(myGame.board, [['x','',''],['','',''],['','','']])

    def test_col_win(self):
        myGame = TicTacToe()
        myGame.place_marker('x', 0, 0)
        myGame.place_marker('o', 0, 1)
        myGame.place_marker('x', 1, 0)
        myGame.place_marker('o', 1, 1)
        myGame.place_marker('x', 2, 0)
        self.assertEqual(myGame.state, STATES.CROSS_WON)

    def test_row_win(self):
        myGame = TicTacToe()
        myGame.place_marker('x', 0, 0)
        myGame.place_marker('o', 1, 0)
        myGame.place_marker('x', 0, 1)
        myGame.place_marker('o', 1, 1)
        myGame.place_marker('x', 0, 2)
        self.assertEqual(myGame.state, STATES.CROSS_WON)

    def test_diag_win(self):
        myGame = TicTacToe()
        myGame.place_marker('x', 0, 0)
        myGame.place_marker('o', 1, 0)
        myGame.place_marker('x', 1, 1)
        myGame.place_marker('o', 2, 1)
        myGame.place_marker('x', 2, 2)
        self.assertEqual(myGame.state, STATES.CROSS_WON)

    def test_o_win(self):
        myGame = TicTacToe()
        myGame.place_marker('x', 0, 0)
        myGame.place_marker('o', 1, 0)
        myGame.place_marker('x', 0, 1)
        myGame.place_marker('o', 1, 1)
        myGame.place_marker('x', 2, 2)
        myGame.place_marker('o', 1, 2)
        self.assertEqual(myGame.state, STATES.NAUGHT_WON)

    def test_draw(self):
        myGame = TicTacToe()
        """
        x|x|o
        -----
        o|o|x
        -----
        x|x|o
        """
        myGame.place_marker('x', 0, 0)
        myGame.place_marker('o', 1, 0)
        myGame.place_marker('x', 0, 1)
        myGame.place_marker('o', 1, 1)
        myGame.place_marker('x', 1, 2)
        myGame.place_marker('o', 0, 2)
        myGame.place_marker('x', 2, 0)
        myGame.place_marker('o', 2, 2)
        myGame.place_marker('x', 2, 1)
        self.assertEqual(myGame.state, STATES.DRAW)