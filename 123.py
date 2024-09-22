import itertools
import pygame
import sys

EMPTY = 0
BLACK = 1
WHITE = 2
GRID_SIZE = 80
BOARD_SIZE = GRID_SIZE * 6  # 修改棋盘大小为6x6

# Initialize the board
board = [[EMPTY] * 6 for _ in range(6)]
board[2][2] = WHITE
board[3][3] = WHITE
board[2][3] = BLACK
board[3][2] = BLACK

# Function to check if a move is valid
def is_valid_move(board, row, col, color):
    if board[row][col] != EMPTY:
        return False
    for dr, dc in itertools.product([-1, 0, 1], repeat=2):
        if dr == 0 and dc == 0:
            continue
        r, c = row + dr, col + dc
        while 0 <= r < 6 and 0 <= c < 6 and board[r][c] != EMPTY and board[r][c] != color:
            r += dr
            c += dc
        if 0 <= r < 6 and 0 <= c < 6 and board[r][c] == color and (r, c) != (row + dr, col + dc):
            return True
    return False

# Function to make a move
def make_move(board, row, col, color):
    if not is_valid_move(board, row, col, color):
        return None
    board[row][col] = color
    flipped_positions = []
    for dr, dc in itertools.product([-1, 0, 1], repeat=2):
        if dr == 0 and dc == 0:
            continue
        r, c = row + dr, col + dc
        while 0 <= r < 6 and 0 <= c < 6 and board[r][c] != EMPTY and board[r][c] != color:
            r += dr
            c += dc
        if 0 <= r < 6 and 0 <= c < 6 and board[r][c] == color and (r, c) != (row + dr, col + dc):
            while (r, c) != (row, col):
                r -= dr
                c -= dc
                if (r, c) != (row, col):
                    board[r][c] = color
                    flipped_positions.append((r, c))
    return flipped_positions

# Function to get a list of valid moves for a given color
def get_valid_moves(board, color):
    moves = []
    for row in range(6):
        for col in range(6):
            if is_valid_move(board, row, col, color):
                moves.append((row, col))
    return moves

# Function to evaluate the current board state for the AI player
def evaluate_board(board):
    black_score = 0
    white_score = 0
    for row in range(6):
        for col in range(6):
            if board[row][col] == BLACK:
                black_score += 1
            elif board[row][col] == WHITE:
                white_score += 1
    return white_score - black_score

# Function for the AI player's move using the Alpha-Beta Pruning algorithm
def alphabeta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or not get_valid_moves(board, BLACK) or not get_valid_moves(board, WHITE):
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        valid_moves = get_valid_moves(board, WHITE)
        for move in valid_moves:
            row, col = move
            temp_board = [row[:] for row in board]
            make_move(temp_board, row, col, WHITE)
            eval = alphabeta(temp_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        valid_moves = get_valid_moves(board, BLACK)
        for move in valid_moves:
            row, col = move
            temp_board = [row[:] for row in board]
            make_move(temp_board, row, col, BLACK)
            eval = alphabeta(temp_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function for the AI player's move
def ai_move(board):
    valid_moves = get_valid_moves(board, WHITE)
    if not valid_moves:
        return False
    best_score = float('-inf')
    best_move = None
    for move in valid_moves:
        row, col = move
        temp_board = [row[:] for row in board]
        make_move(temp_board, row, col, WHITE)
        score = alphabeta(temp_board, 3, float('-inf'), float('inf'), False)
        if score > best_score:
            best_score = score
            best_move = move
    if best_move:
        row, col = best_move
        make_move(board, row, col, WHITE)
    return True

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Reversi")
font = pygame.font.Font(None, 36)

# Function to draw the board
def draw_board(screen, board):
    screen.fill((0, 128, 0))
    for row in range(6):
        for col in range(6):
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            if board[row][col] == BLACK:
                pygame.draw.circle(screen, (0, 0, 0), rect.center, GRID_SIZE // 2 - 4)
            elif board[row][col] == WHITE:
                pygame.draw.circle(screen, (255, 255, 255), rect.center, GRID_SIZE // 2 - 4)
    pygame.display.flip()

# Main game loop
current_player = BLACK
running = True

while running:
    draw_board(screen, board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and current_player == BLACK:
            x, y = event.pos
            row, col = y // GRID_SIZE, x // GRID_SIZE
            flipped_positions = make_move(board, row, col, current_player)
            if flipped_positions is not None:
                draw_board(screen, board)
                pygame.time.delay(1000)
                if not get_valid_moves(board, WHITE):
                    if not get_valid_moves(board, BLACK):
                        running = False
                else:
                    current_player = WHITE

    if current_player == WHITE and running:
        if not ai_move(board):
            if not get_valid_moves(board, BLACK):
                running = False
        else:
            draw_board(screen, board)
            if not get_valid_moves(board, BLACK):
                if not get_valid_moves(board, WHITE):
                    running = False
            else:
                current_player = BLACK

    if not get_valid_moves(board, BLACK) and not get_valid_moves(board, WHITE):
        running = False

def display_results(screen, black_score, white_score):
    """Displays the end game results and a button to exit."""
    screen.fill((0, 128, 0))  # Clear the screen
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    black_score_text = font.render(f"Black Score: {black_score}", True, (255, 255, 255))
    white_score_text = font.render(f"White Score: {white_score}", True, (255, 255, 255))
    result_text = "It's a Tie!" if black_score == white_score else ("Black Wins!" if black_score > white_score else "White Wins!")
    result_text = font.render(result_text, True, (255, 255, 255))

    exit_button = pygame.Rect(BOARD_SIZE / 2 - 100, 300, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), exit_button)  # Draw the exit button
    exit_text = font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_text, (exit_button.centerx - exit_text.get_width() / 2, exit_button.centery - exit_text.get_height() / 2))

    # Update screen positions
    screen.blit(game_over_text, (BOARD_SIZE / 2 - game_over_text.get_width() / 2, 50))
    screen.blit(black_score_text, (BOARD_SIZE / 2 - black_score_text.get_width() / 2, 100))
    screen.blit(white_score_text, (BOARD_SIZE / 2 - white_score_text.get_width() / 2, 150))
    screen.blit(result_text, (BOARD_SIZE / 2 - result_text.get_width() / 2, 200))

    pygame.display.flip()  # Update the display

    # Event loop for the results screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if exit_button.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

# Modify the game loop to call this function when the game ends
if not running:
    black_score = sum(row.count(BLACK) for row in board)
    white_score = sum(row.count(WHITE) for row in board)
    display_results(screen, black_score, white_score)