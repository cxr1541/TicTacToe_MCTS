class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

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

        while True:
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
