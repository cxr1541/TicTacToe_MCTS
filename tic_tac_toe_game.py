# let's say player o is the AI and player x is the human
# let's say the maximum time for the AI to play his turn is 2 seconds
import random
from collections import defaultdict
from abc import ABC, abstractmethod
import math

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.visits = 0
        self.wins = 0
        self.children = {}

        print("Created node with state:")
        print(self.state)

class MCTS:
    def __init__(self):
        self.V = defaultdict(int) #the total reward for each node
        self.N = defaultdict(int) #the total times the node has been visited
        self.children = dict(); #children of each node, for now we set the dictionnary as being empty

    def select(self, board_state):
    # starting at the root node
      node = board_state
  
      # traverse the tree until a leaf node is reached
      while not node.check_winner() and node in self.children:
          # the UCB algorithm will select a child node to explore
          if node not in self.children:
              # add the node to the tree and expand it
              self.children[node] = {move: node.next_state(move) for move in node.get_possible_moves()}
          else:
              _, node = max(((self.V[child] / self.N[child]) + math.sqrt(2 * math.log(self.N[node]) / self.N[child]), child) for child in self.children[node])
  
          # perform some action on the child node
  
          # expand the node if it hasn't been expanded yet and add it to the tree
          if not node.check_winner():
              unexplored_moves = [move for move in node.get_possible_moves() if move not in self.children[node]]
              # chooses unexplored move randomly
              if unexplored_moves:
                  move = random.choice(unexplored_moves)
                  new_node = node.next_state(move)
                  self.children[node][move] = new_node
                  node = new_node
  
      return node

    def backpropagate(self, node, score):
        # update nodes's up to root node
        while node is not None:
            # update node's visits
            node.visits += 1
            
            # update node's score
            node.score += score
            
            # set node to parent
            node = node.parent

   
    def rollout(self, board_state):
        #check if there is a winner in the current state
        winner = board_state.check_winner()
        if winner:
            if winner == 'O':
                return -1
            else:
                return 1
            #if there is no winner continue playing
        while not board_state.is_draw():
            row, col = random.choice(board_state.available_play())
            board_state.play_move(row,col)
            winner = board_state.check_winner()
            if winner:
                if winner == 'O':
                    return -1
                else:
                    return 1
        return 0
    def rollout_policy(board_state):
        #returns a random valid move for the given board state
        return random.choice(board_state.available_play())
    def choose_next_move(self,board_state):
        #choosing the best sucessor out of all 
        if board_state.check_winner():
            raise RuntimeError(f"choose_next_move was called when no more moves are possible {board_state}")
        def score(n):
            if self.N[n] == 0:
                return float("-inf") 
                #by doing this we are avoiding to choose before having explored the node
            return self.V[n] / self.N[n] #this is the average number
        return max(self.children[board_state], key = score)
        #self.children[board_state] needs a row and a col function for the main to work and get the movment they want it to be

class TicTacToe:
    # initialize tic tac toe board
    def __init__(self):
        # creates a 2D list of size 3x3
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        # player is X
        self.current_player = 'X'

    # all moves that are currently available
    def available_play(self):
        # list of the different available possible plays, we could make a list with all the different poissible move, so that we can pop that possibility when we want to expand that node
        list_of_possible_moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    #add moves to the list
                    list_of_possible_moves.append((row,col))
        return list_of_possible_moves
    
    # print the current game board
    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * 9)

    # check if there is a winner
    def check_winner(self):
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

    #check if there is a draw
    def is_draw(self):
        for row in self.board:
            if " " in row:
                return False
        return True
    
    # play move
    def play_move(self, row, col):
        # check if move is valid
        if row < 0 or row > 2 or col < 0 or col > 2 or self.board[row][col] != " ":
            print("Invalid move. Try again.")
        
        else:
            # assign current player to grid they select
            self.board[row][col] = self.current_player
            #swap players since player and AI take turns 
            self.current_player = "X" if self.current_player == "O" else "O"

    # Main function to run the game
    def main(self):

        
        print("Welcome to Tic-Tac-Toe!")
        print("X goes first.")
        print("The cells are numbered from 0 to 8 as shown below.")
        self.print_board()
        print(self.available_play())

        while not self.is_draw():
            if self.current_player == 'X':
                row = int(input("Enter row: "))
                col = int(input("Enter col: "))
            else:
                print("Thinking...")
                mcts = MCTS()
                node = self
                for i in range(1000):
                    mcts.N[node] += 1
                    leaf = mcts.select(node)
                    reward = mcts.rollout(leaf)
                    #mcts.backpropagate(leaf, reward)
                row, col = mcts.choose_next_move(node)
                print(f"AI plays {row}, {col}")

            self.play_move(row, col)
            self.print_board()

            winner = self.check_winner()
            if winner:
                print(f"{winner} wins!")
                return

        print("Draw.")




if __name__ == "__main__":
    #create tic tac toe board
    game = TicTacToe()
    #start the game
    game.main()

class board_state(ABC):
    #these is what can be considered as a node. MCTS will create a tree of these nodes, expand from the current node and explore, simulate and backtrack
    def __init__(self) -> None:
        super().__init__()

