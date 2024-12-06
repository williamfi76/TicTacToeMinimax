import tkinter as tk
from functools import partial

# Initialize the game variables
player, opponent = 'x', 'o'
board = [['_' for _ in range(3)] for _ in range(3)]


def isMovesLeft(board):
    for row in board:
        if '_' in row:
            return True
    return False


def evaluate(b):
    # Check rows and columns
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] and b[i][0] != '_':
            return 10 if b[i][0] == player else -10
        if b[0][i] == b[1][i] == b[2][i] and b[0][i] != '_':
            return 10 if b[0][i] == player else -10

    # Check diagonals
    if b[0][0] == b[1][1] == b[2][2] and b[0][0] != '_':
        return 10 if b[0][0] == player else -10
    if b[0][2] == b[1][1] == b[2][0] and b[0][2] != '_':
        return 10 if b[0][2] == player else -10

    return 0


# Recursive function
def minimax(board, depth, isMax):
    score = evaluate(board)

    if score == 10 or score == -10:
        return score
    if not isMovesLeft(board):
        return 0

    if isMax:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = player
                    best = max(best, minimax(board, depth + 1, not isMax))
                    board[i][j] = '_'
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, not isMax))
                    board[i][j] = '_'
        return best


def findBestMove(board):
    bestVal = 1000  # The bot plays as the minimizing player (opponent)
    bestMove = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = opponent
                moveVal = minimax(board, 0, True)  # Switch roles: player becomes maximizing
                board[i][j] = '_'
                if moveVal < bestVal:  # Minimize score for opponent
                    bestMove = (i, j)
                    bestVal = moveVal
    return bestMove


def computerMove():
    global board
    bestMove = findBestMove(board)
    if bestMove != (-1, -1):
        board[bestMove[0]][bestMove[1]] = opponent
        buttons[bestMove[0]][bestMove[1]].config(text=opponent, state='disabled', disabledforeground='red')
        checkWinner()


def checkWinner():
    global board
    score = evaluate(board)
    if score == 10:
        status_label.config(text="You Win!", fg="green")
        disableButtons()
    elif score == -10:
        status_label.config(text="Computer Wins!", fg="red")
        disableButtons()
    elif not isMovesLeft(board):
        status_label.config(text="It's a Draw!", fg="blue")
        disableButtons()


def disableButtons():
    for row in buttons:
        for btn in row:
            btn.config(state='disabled')


def onClick(row, col):
    global board
    if board[row][col] == '_':
        board[row][col] = player
        buttons[row][col].config(text=player, state='disabled', disabledforeground='green')
        checkWinner()
        if isMovesLeft(board) and evaluate(board) == 0:
            computerMove()


# Create the main window
root = tk.Tk()
root.title("Tic Tac Toe with Smart AI")

# Create a grid of buttons
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text="", font=('Helvetica', 20), height=2, width=5,
                                  command=partial(onClick, i, j))
        buttons[i][j].grid(row=i, column=j)

# Create a status label
status_label = tk.Label(root, text="Your Turn", font=('Helvetica', 16))
status_label.grid(row=3, column=0, columnspan=3)

# Start the main loop
root.mainloop()

"""
Algoritma Minimax adalah algoritma yang digunakan untuk mencari solusi optimal dalam permainan tic tac toe. 
Algoritma ini dibangun dengan penerapan strategi minimax, yang mengasumsikan bahwa AI akan mencoba semua posisi papan yang 
dapat dilakukan oleh player dan mencari solusi yang memberikan skor terbesar bagi AI. 

Completeness: 
Program ini bisa disebut complete, karena solusi yang dimunculkan oleh computer selalu win atau draw.
Algoritma AI yang dibuat disini sudah dipastikan tidak pernah kalah.

Optimality:
Algoritma minimax bisa dibilang optimal, karena ia dapat menemukan solusi optimal yang paling efektif dalam permainan 
tic tac toe untuk mencegah player menang. 

Time Complexity:
Program ini memiliki time complexity O(2^n) dengan n sebagai depth dari tree nya. Tree disini mengacu kepada pilihan 
move yang akan dilakukan oleh computer yang nanti nya akan dikalkulasi dan dicari nilai yang paling maksimal untuk
diambil.
"""
