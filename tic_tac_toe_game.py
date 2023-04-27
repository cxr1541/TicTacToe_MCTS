# let's say player o is the AI and player x is the human
# let's say the maximum time for the AI to play his turn is 2 seconds
import random
from collections import defaultdict
from abc import ABC, abstractmethod
import math
class MCTS:
    def __init__(self):
        self.V = defaultdict(int) #the total reward for each node
        self.N = defaultdict(int) #the total times the node has been visited
        self.children = dict(); #children of each node, for now we set the dictionnary as being empty
    def select(self, board_state):
        #starting at the root node
        node = board_state
        #traverse the tree until a leaf node is reached
        while not node.is_terminal() and node is self.children:
            #the UCB algorithm will select a child node to explore
            _, node = max((self.V[child] / self.N[child] + math.sqrt(2*math.log(self.N[node])/self.N[child])
                           for child in self.children[node]))
        #expand the node if it hasnt been expanded yet and add it to the tree
        if not node.is_terminal():
            unexplored_moves = [move for move in node.get_possible_moves()
                                if move not in self.children[node]]
            #chooses the first unexplored move should we keep it at the first option or make it random like the paper?
            move = unexplored_moves[0]
            new_node = node.next_state(move)
            self.children[node][move] = new_node
            node = new_node
        return node
   
    def rollout(self, board_state):
        #check if there is a winner in the current state
        winner = board_state.check_winner()
        if winner:
            if winner == 'O':
                return 1
            else:
                return 1
            #if there is no winner continue playing
        while not board_state.is_draw():
            row, col = random.choice(board_state.avaliable_play())
            board_state.play_move(row,col)
            winner = board_state.check_winner()
            if winner:
                if winner == 'O':
                    return 1
                else:
                    return -1
        return 00
    def rollout_policy(board_state):
        #returns a random valid move for the given board state
        return random.choice(board_state.avaliable_play())
    def choose_next_move(self,board_state):
        #choosing the best sucessor out of all 
        if board_state.is_terminal():
            raise RuntimeError(f"choose_next_move was called when no more moves are possible {board_state}")
        def score(n):
            if self.N[n] == 0:
                return float("-inf") 
                #by doing this we are avoiding to choose before having explored the node
            return self.V[n] / self.N[n] #this is the average number
        return max(self.children[board_state], key = score)
        #self.children[board_state] needs a row and a col function for the main to work and get the movment they want it to be
class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
    def available_play(self):
        #list of the different available possible plays, we could make a list with all the different poissible move, so that we can pop that possibility when we want to expand that node
       
        list_of_possible_moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    list_of_possible_moves.append((row,col))
        return list_of_possible_moves[0]
    def print_board(self):
        """Print the current game board."""
        for row in self.board:
            print(" | ".join(row))
            print("-" * 9)

    def check_winner(self):
        """Check if there's a winner."""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != " ":
                return row[0]

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != " ":
                return self.board[0][col]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
            return self.board[0][2]

        return None

    def is_draw(self):
        """Check if the game is a draw."""
        for row in self.board:
            if " " in row:
                return False
        return True
    
    def play_move(self, row, col):
        if row < 0 or row > 2 or col < 0 or col > 2 or self.board[row][col] != " ":
            print("Invalid move. Try again.")
        else:
            self.board[row][col] = self.current_player
            self.current_player = "X" if self.current_player == "O" else "O"

    def main(self):
        """Main function to run the game."""

        print("Welcome to Tic-Tac-Toe!")
        self.print_board()
        print(self.available_play())

        while True:
            if self.current_player == "O":
                print(f"Player {self.current_player} is playing, wait for him to enter his move")
                row = MCTS.choose_next_move.row - 1
                col = MCTS.choose_next_move.col - 1
            else:
                print(f"Player {self.current_player}, enter your move (row [1-3], column [1-3]):")
                row = int(input("Enter row: ")) - 1
                col = int(input("Enter column: ")) - 1

            self.play_move(row, col)
            self.print_board()

            winner = self.check_winner()
            if winner:
                print(f"Player {winner} wins!")
                break
            elif self.is_draw():
                print("It's a draw!")
                break

if __name__ == "__main__":
    game = TicTacToe()
    game.main()

class board_state(ABC):
    #these is what can be considered as a node. MCTS will create a tree of these nodes, expand from the current node and explore, simulate and backtrack
    def __init__(self) -> None:
        super().__init__()

