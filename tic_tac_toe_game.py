def print_board(board):
    """Print the current game board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def check_winner(board):
    """Check if there's a winner."""
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]

    return None


def is_draw(board):
    """Check if the game is a draw."""
    for row in board:
        if " " in row:
            return False
    return True


def main():
    """Main function to run the game."""
    # Initialize the game board
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        print(f"Player {current_player}, enter your move (row [1-3], column [1-3]):")
        row = int(input("Enter row: ")) - 1
        col = int(input("Enter column: ")) - 1

        if row < 0 or row > 2 or col < 0 or col > 2 or board[row][col] != " ":
            print("Invalid move. Try again.")
            continue

        board[row][col] = current_player
        print_board(board)

        winner = check_winner(board)
        if winner:
            print(f"Player {winner} wins!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        current_player = "X" if current_player == "O" else "O"


if __name__ == "__main__":
    main()
