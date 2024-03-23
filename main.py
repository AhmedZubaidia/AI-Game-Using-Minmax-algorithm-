import pygame
from pygame.locals import *
import time

WINDOW_DIMENSION = 600
BOARD_DIMENSION = 8
SQUARE_SIZE = WINDOW_DIMENSION // BOARD_DIMENSION
LABEL_SIZE = WINDOW_DIMENSION // 16

WHITE = (233, 236, 239)
BLACK = (52, 58, 64)
LABEL_COLOR = (125, 135, 150)
EMPTY = " "
PLAYER1 = "X"
PLAYER2 = "O"

pygame.init()
screen = pygame.display.set_mode((WINDOW_DIMENSION, WINDOW_DIMENSION))
pygame.display.set_caption("Magnetic Cave")

font = pygame.font.Font(None, LABEL_SIZE)
modeValue = ''
modeValue2 = ''

class Game:

    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_DIMENSION)] for _ in range(BOARD_DIMENSION)]
        self.current_player = PLAYER1

    def draw_board(self):
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                color = WHITE
                pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.lines(screen, BLACK, False, [(col * SQUARE_SIZE, row * SQUARE_SIZE),
                                                         (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE)], 1)
                pygame.draw.lines(screen, BLACK, False, [(col * SQUARE_SIZE, row * SQUARE_SIZE),
                                                         ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE)], 1)

                if self.board[row][col] != EMPTY:
                    label = font.render(self.board[row][col], True, BLACK if self.board[row][col] == PLAYER1 else LABEL_COLOR)
                    label_rect = label.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                    screen.blit(label, label_rect)

        pygame.draw.lines(screen, BLACK, False, [(0, WINDOW_DIMENSION - 1), (WINDOW_DIMENSION - 1, WINDOW_DIMENSION - 1)], 1)
        pygame.draw.lines(screen, BLACK, False, [(WINDOW_DIMENSION - 1, 0), (WINDOW_DIMENSION - 1, WINDOW_DIMENSION - 1)], 1)

        for i in range(BOARD_DIMENSION):
            label = font.render(chr(97 + i), True, LABEL_COLOR)
            screen.blit(label, (i * SQUARE_SIZE + SQUARE_SIZE // 2, 0))
            screen.blit(label, (i * SQUARE_SIZE + SQUARE_SIZE // 2, WINDOW_DIMENSION - LABEL_SIZE))
            label = font.render(str(8 - i), True, LABEL_COLOR)
            screen.blit(label, (0, i * SQUARE_SIZE + SQUARE_SIZE // 2))
            screen.blit(label, (WINDOW_DIMENSION - LABEL_SIZE, i * SQUARE_SIZE + SQUARE_SIZE // 2))

    def is_valid_move(self, col, row):
        if self.board[row][col] != EMPTY:
            return False
        if col == 0 or col == BOARD_DIMENSION - 1:
            return True
        if self.board[row][col - 1] != EMPTY or self.board[row][col + 1] != EMPTY:
            return True
        return False

    def new_is_valid_move(self, row, col):
        if self.board[row][col] != EMPTY:
            return False
        if col == 0 or col == BOARD_DIMENSION - 1:
            return True
        if self.board[row][col - 1] != EMPTY or self.board[row][col + 1] != EMPTY:
            return True
        return False
    def has_won(self, col, row):
        for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            if self.count_consecutive(col, row, dx, dy) >= 5:
                return True
        return False

    def count_consecutive(self, col, row, dx, dy):
        count = 1
        for direction in [-1, 1]:
            for step in range(1, 5):
                x, y = col + direction * step * dx, row + direction * step * dy
                if 0 <= x < BOARD_DIMENSION and 0 <= y < BOARD_DIMENSION and self.board[y][x] == self.board[row][col]:
                    count += 1
                else:
                    break
        return count

    def manual_move(self):
        x, y = pygame.mouse.get_pos()
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        if self.is_valid_move(col, row):
            return col, row
        else:
            return None, None

    def automatic_move(self):
        best_move = self.minimax(4, True, float('-inf'), float('inf'))

        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                if self.new_is_valid_move(row, col):
                    self.board[row][col] = self.current_player
                    if self.has_won(col, row):
                        self.board[row][col] = EMPTY
                        return col, row
                    self.board[row][col] = EMPTY

        return best_move[1], best_move[0]



    def evaluate_board(self):
        computer_consecutive_bricks = self.get_consecutive_bricks_count(PLAYER2)
        player_consecutive_bricks = self.get_consecutive_bricks_count(PLAYER1)

        if computer_consecutive_bricks >= 5:
            return float('inf')
        elif player_consecutive_bricks >= 5:
            return float('-inf')
        elif self.is_board_full():
            return 0

        computer_two_consecutive_bricks = self.get_consecutive_bricks_count2(PLAYER2, 2)
        player_two_consecutive_bricks = self.get_consecutive_bricks_count2(PLAYER1, 2)

        computer_three_consecutive_bricks = self.get_consecutive_bricks_count2(PLAYER2, 3)
        player_three_consecutive_bricks = self.get_consecutive_bricks_count2(PLAYER1, 3)



        final_computer_score = 50 * computer_three_consecutive_bricks + 10 * computer_two_consecutive_bricks
        final_player_score = 50 * player_three_consecutive_bricks + 10 * player_two_consecutive_bricks

        return final_computer_score - final_player_score

    def make_move(self, i, j, player):
        if self.is_valid_move(i, j):
            self.board[i][j] = player

    def minimax(self,depth, maximizingPlayer, alpha, beta):
        if depth == 0 or self.is_board_full():
            score = self.evaluate_board()
            return [-1, -1, score]

        best = [-1, -1, None]

        if maximizingPlayer:
            best[2] = float('-inf')

            for i in range(8):
                for j in range(8):
                    if self.new_is_valid_move(i, j):
                        self.make_move(i, j, modeValue)
                        move = self.minimax(depth - 1, False, alpha, beta)
                        self.board[i][j] = EMPTY

                        score = move[2]

                        if score > best[2]:
                            best[0] = i
                            best[1] = j
                            best[2] = score

                        alpha = max(alpha, score)
                        if alpha >= beta:
                            return best

        else:
            best[2] = float('inf')

            for i in range(8):
                for j in range(8):
                    if self.new_is_valid_move(i, j):
                        self.make_move(i, j, modeValue2)
                        move = self.minimax(depth - 1, True, alpha, beta)
                        self.board[i][j] = EMPTY

                        score = move[2]

                        if score < best[2]:
                            best[0] = i
                            best[1] = j
                            best[2] = score

                        beta = min(beta, score)
                        if alpha >= beta:
                            return best

        return best

    def is_board_full(self):
        for row in self.board:
            if EMPTY in row:
                return False
        return True



    def get_consecutive_bricks_count(self, brick):
        count = 0
        BOARD_SIZE = len(self.board)

        # Check for horizontal consecutives
        for i in range(BOARD_SIZE):
            consecutive = 0
            for j in range(BOARD_SIZE):
                if self.board[i][j] == brick:
                    consecutive += 1
                    if consecutive >= 5:
                        return consecutive
                else:
                    consecutive = 0

        # Check for vertical consecutives
        for i in range(BOARD_SIZE):
            consecutive = 0
            for j in range(BOARD_SIZE):
                if self.board[j][i] == brick:
                    consecutive += 1
                    if consecutive >= 5:
                        return consecutive
                else:
                    consecutive = 0

        for i in range(BOARD_SIZE - 4):
            for j in range(BOARD_SIZE - 4):
                consecutive = 0
                for k in range(5):
                    if self.board[i + k][j + k] == brick:
                        consecutive += 1
                        if consecutive >= 5:
                            return consecutive
                    else:
                        consecutive = 0

        for i in range(BOARD_SIZE - 4):
            for j in range(4, BOARD_SIZE):
                consecutive = 0
                for k in range(5):
                    if self.board[i + k][j - k] == brick:
                        consecutive += 1
                        if consecutive >= 5:
                            return consecutive
                    else:
                        consecutive = 0

        return count

    def get_consecutive_bricks_count2(self, brick, length):
        count = 0
        BOARD_SIZE = len(self.board)

        for i in range(BOARD_SIZE):
            consecutive = 0
            for j in range(BOARD_SIZE):
                if self.board[i][j] == brick:
                    consecutive += 1
                    if consecutive >= length:
                        count += 1
                else:
                    consecutive = 0

        for i in range(BOARD_SIZE):
            consecutive = 0
            for j in range(BOARD_SIZE):
                if self.board[j][i] == brick:
                    consecutive += 1
                    if consecutive >= length:
                        count += 1
                else:
                    consecutive = 0

        for i in range(BOARD_SIZE - length + 1):
            for j in range(BOARD_SIZE - length + 1):
                consecutive = 0
                for k in range(length):
                    if self.board[i + k][j + k] == brick:
                        consecutive += 1
                        if consecutive >= length:
                            count += 1
                    else:
                        consecutive = 0

        for i in range(BOARD_SIZE - length + 1):
            for j in range(length - 1, BOARD_SIZE):
                consecutive = 0
                for k in range(length):
                    if self.board[i + k][j - k] == brick:
                        consecutive += 1
                        if consecutive >= length:
                            count += 1
                    else:
                        consecutive = 0

        return count

    def is_game_over(self):
        return False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    col, row = self.manual_move()
                    if col is not None and row is not None and self.is_valid_move(col, row):
                        self.board[row][col] = self.current_player
                        if self.has_won(col, row):
                            print(f"Player {self.current_player} has won!")
                            running = False
                        self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
                    else:
                        print("Invalid move. Please try again.")
                else:
                    if event.type == MOUSEBUTTONDOWN and self.current_player == PLAYER1:
                        col, row = self.manual_move()
                        if col is not None and row is not None and self.is_valid_move(col, row):
                            self.board[row][col] = self.current_player
                            if self.has_won(col, row):
                                print(f"Player {self.current_player} has won!")
                                running = False
                            self.current_player = PLAYER2
                        else:
                            print("Invalid move. Please try again.")
                    elif self.current_player == PLAYER2:
                        col, row = self.automatic_move()
                        if self.is_valid_move(col, row):
                            self.board[row][col] = self.current_player
                            if self.has_won(col, row):
                                print(f"Player {self.current_player} has won!")
                                running = False
                            self.current_player = PLAYER1

            self.draw_board()
            pygame.display.update()

        pygame.quit()


def display_mode_selection():
    while True:
        screen.fill(WHITE)

        title_text = font.render("Magnetic Cave", True, BLACK)
        title_text_rect = title_text.get_rect(center=(WINDOW_DIMENSION // 2, 100))
        screen.blit(title_text, title_text_rect)

        label_font = pygame.font.Font(None, LABEL_SIZE // 2)
        label_text = label_font.render("Please select a play mode:", True, (125, 135, 150))
        label_text_rect = label_text.get_rect(top=150, left=20)
        screen.blit(label_text, label_text_rect)

        button_width = 400
        button_height = 50
        button_padding = 20
        button_x = (WINDOW_DIMENSION - button_width) // 2
        button_y = 200

        manual_button = pygame.draw.rect(screen, BLACK, (button_x, button_y, button_width, button_height))
        manual_text = font.render("Manual X & O", True, WHITE)
        manual_text_rect = manual_text.get_rect(center=manual_button.center)
        screen.blit(manual_text, manual_text_rect)

        manual_auto_button = pygame.draw.rect(screen, BLACK, (
            button_x, button_y + button_height + button_padding, button_width, button_height))
        manual_auto_text = font.render("Manual X, automatic O", True, WHITE)
        manual_auto_text_rect = manual_auto_text.get_rect(center=manual_auto_button.center)
        screen.blit(manual_auto_text, manual_auto_text_rect)

        auto_manual_button = pygame.draw.rect(screen, BLACK, (
            button_x, button_y + 2 * (button_height + button_padding), button_width, button_height))
        auto_manual_text = font.render("Manual O, automatic X", True, WHITE)
        auto_manual_text_rect = auto_manual_text.get_rect(center=auto_manual_button.center)
        screen.blit(auto_manual_text, auto_manual_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if manual_button.collidepoint(pos):
                    return "manual"
                elif manual_auto_button.collidepoint(pos):
                    return "manual_auto"
                elif auto_manual_button.collidepoint(pos):
                    return "auto_manual"


if __name__ == "__main__":
    game = Game()

    mode = display_mode_selection()
    if mode == "manual":
        game.manual_move = game.manual_move
        game.automatic_move = game.manual_move
    elif mode == "manual_auto":
        game.manual_move = game.manual_move
        game.automatic_move = game.automatic_move
        modeValue ='O'
        modeValue2='X'
    elif mode == "auto_manual":
        game.manual_move = game.manual_move
        game.automatic_move = game.automatic_move
        game.current_player = PLAYER2
        PLAYER1, PLAYER2 = PLAYER2, PLAYER1
        modeValue = 'X'
        modeValue2 = 'O'
    game.run()

    pygame.quit()
