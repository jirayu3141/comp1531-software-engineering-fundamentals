import pytest
class game:
    def __init__(self):
        self.board = [[None]*3 for i in range(3)]
        self.X_won = None
        self.O_won = None

    def show_state(self):
        for x in self.board:
            print(x)

        print("========")

    def place_x(self, x, y):
        if self.board[x][y] == None:
            self.board[x][y] = "X"
        else:
            raise ValueError
        if self.check_victory(x, y):
            self.x_won = True
            #print("X won the game")

    def place_o(self, x, y):
        if self.board[x][y] == None:
            self.board[x][y] = "O"
        else:
            raise ValueError
        if self.check_victory(x, y):
            self.O_won = True
            #print("O won the game")

    def check_victory(self, x, y):
        # check if previous move caused a win on vertical line
        if self.board[0][y] == self.board[1][y] == self.board[2][y]:
            return True

        # check if previous move caused a win on horizontal line
        if self.board[x][0] == self.board[x][1] == self.board[x][2]:
            return True

        # check if previous move was on the main diagonal and caused a win
        if x == y and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True

        # check if previous move was on the secondary diagonal and caused a win
        if x + y == 2 and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return True

        return False

    def reset(self):
        self.__init__()

game = game()

def test_tictac_vertical():
    global game
    game.reset()
    game.place_o(2, 2)
    game.place_o(1, 2)
    game.place_o(0, 2)
    assert game.O_won == True
    game.show_state()

def test_tictac_horizontal():
    global game
    game.reset()
    game.place_o(1, 0)
    game.place_o(1, 1)
    game.place_o(1, 2)
    assert game.O_won == True
    game.show_state()

def test_tictac_diagonal():
    global game
    game.reset()
    #test o
    game.place_o(0,0)
    game.place_o(1,1)
    game.place_o(2,2)
    assert game.O_won == True
    game.show_state()
    
    game.reset()
    #test x
    game.place_x(0,0)
    game.place_x(1,1)
    game.place_x(2,2)
    assert game.x_won == True
    game.show_state()

    game.reset()
    #test x
    game.place_x(2,0)
    game.place_x(1,1)
    game.place_x(0,2)
    assert game.x_won == True
    game.show_state()

def test_same_move():
    global game
    #repeated o
    with pytest.raises(ValueError):
        game.place_o(0,0)
        game.place_o(0,0)

    #repeated x
    with pytest.raises(ValueError):
        game.place_x(0,0)
        game.place_x(0,0)
    pass


if __name__ == "__main__":
    test_tictac_diagonal()
    test_tictac_horizontal()
    test_tictac_vertical()
    pass
