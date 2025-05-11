import pygame
import os
import time
import sys

pygame.init()
pygame.mixer.init()

# Load sounds
SOUNDS = {
    "move": pygame.mixer.Sound("sounds/move.wav"),
    "capture": pygame.mixer.Sound("sounds/capture.wav"),
    "checkmate": pygame.mixer.Sound("sounds/checkmate.wav"),
}

WIDTH = 600
HEIGHT = 720
BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE // 8
BORDER_WIDTH = 10
TIMER_HEIGHT = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шахматы на Python")

WHITE = (221, 221, 221)
GRAY = (100, 100, 100)
HIGHLIGHT = (255, 255, 0, 100)
BORDER_COLOR = (50, 50, 50)
font = pygame.font.SysFont(None, 60)
timer_font = pygame.font.SysFont(None, 40)

# --- Загрузка изображений ---
PIECE_IMAGES = {}
def load_piece_images():
    names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['white', 'black']
    for color in colors:
        for name in names:
            path = os.path.join("assets", f"{color}_{name}.png")
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
                PIECE_IMAGES[f"{color}_{name}"] = img

load_piece_images()

# --- Класс фигур ---
class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.name = self.__class__.__name__.lower()

    def draw(self):
        x = self.position[1] * SQUARE_SIZE
        y = self.position[0] * SQUARE_SIZE + BORDER_WIDTH + TIMER_HEIGHT
        key = f"{self.color}_{self.name}"
        if key in PIECE_IMAGES:
            screen.blit(PIECE_IMAGES[key], (x, y))
        else:
            self.draw_default()

    def draw_default(self):
        x = self.position[1] * SQUARE_SIZE + SQUARE_SIZE // 2
        y = self.position[0] * SQUARE_SIZE + SQUARE_SIZE // 2 + BORDER_WIDTH + TIMER_HEIGHT
        color = (255, 255, 255) if self.color == 'white' else (0, 0, 0)
        pygame.draw.circle(screen, color, (x, y), SQUARE_SIZE // 3)

class Pawn(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        direction = -1 if self.color == 'white' else 1

        new_row = row + direction
        if 0 <= new_row < 8 and board.grid[new_row][col] is None:
            moves.append((new_row, col))

        if (self.color == 'white' and row == 6) or (self.color == 'black' and row == 1):
            if board.grid[new_row][col] is None and board.grid[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))

        for dc in [-1, 1]:
            new_col = col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.grid[new_row][new_col] is not None and board.grid[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))

        return moves

class King(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.grid[new_row][new_col] is None or board.grid[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))

        return moves

class Queen(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.grid[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board.grid[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row, new_col = new_row + dr, new_col + dc
        return moves

class Rook(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.grid[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board.grid[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row, new_col = new_row + dr, new_col + dc
        return moves

class Knight(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.grid[new_row][new_col] is None or board.grid[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
        return moves

class Bishop(Piece):
    def get_possible_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.grid[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board.grid[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row, new_col = new_row + dr, new_col + dc
        return moves

# Класс доски
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        for col in range(8):
            self.grid[1][col] = Pawn('black', (1, col))
            self.grid[6][col] = Pawn('white', (6, col))
        self.grid[0][0] = Rook('black', (0, 0))
        self.grid[0][7] = Rook('black', (0, 7))
        self.grid[7][0] = Rook('white', (7, 0))
        self.grid[7][7] = Rook('white', (7, 7))
        self.grid[0][1] = Knight('black', (0, 1))
        self.grid[0][6] = Knight('black', (0, 6))
        self.grid[7][1] = Knight('white', (7, 1))
        self.grid[7][6] = Knight('white', (7, 6))
        self.grid[0][2] = Bishop('black', (0, 2))
        self.grid[0][5] = Bishop('black', (0, 5))
        self.grid[7][2] = Bishop('white', (7, 2))
        self.grid[7][5] = Bishop('white', (7, 5))
        self.grid[0][3] = Queen('black', (0, 3))
        self.grid[7][3] = Queen('white', (7, 3))
        self.grid[0][4] = King('black', (0, 4))
        self.grid[7][4] = King('white', (7, 4))

    def draw(self):
        for row in range(8):
            for col in range(8):
                if self.grid[row][col]:
                    self.grid[row][col].draw()

    def move(self, start, end, promotion=None):
        piece = self.grid[start[0]][start[1]]
        if piece and end in piece.get_possible_moves(self):
            # Check if it's a capture
            is_capture = self.grid[end[0]][end[1]] is not None
            # Превращение пешки
            if isinstance(piece, Pawn) and (end[0] == 0 or end[0] == 7):
                if promotion:
                    if promotion == 'queen':
                        new_piece = Queen(piece.color, end)
                    elif promotion == 'rook':
                        new_piece = Rook(piece.color, end)
                    elif promotion == 'knight':
                        new_piece = Knight(piece.color, end)
                    elif promotion == 'bishop':
                        new_piece = Bishop(piece.color, end)
                    self.grid[end[0]][end[1]] = new_piece
            else:
                self.grid[end[0]][end[1]] = piece
            self.grid[start[0]][start[1]] = None
            piece.position = end
            # Play sound
            if is_capture:
                SOUNDS["capture"].play()
            else:
                SOUNDS["move"].play()
            return True
        return False

    def is_in_check(self, color):
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color != color:
                    if king_pos in piece.get_possible_moves(self):
                        return True
        return False

    def get_legal_moves(self, start, color):
        piece = self.grid[start[0]][start[1]]
        if not piece or piece.color != color:
            return []

        moves = piece.get_possible_moves(self)
        legal_moves = []
        for move in moves:
            temp_piece = self.grid[move[0]][move[1]]
            self.grid[move[0]][move[1]] = piece
            self.grid[start[0]][start[1]] = None
            old_pos = piece.position
            piece.position = move

            if not self.is_in_check(color):
                legal_moves.append(move)

            self.grid[start[0]][start[1]] = piece
            self.grid[move[0]][move[1]] = temp_piece
            piece.position = old_pos

        return legal_moves

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    if self.get_legal_moves((row, col), color):
                        return False
        return True

def draw_board(board, selected=None, turn='white'):
    # Draw border
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, (0, 0, 0), (BORDER_WIDTH, BORDER_WIDTH + TIMER_HEIGHT,
                                        BOARD_SIZE, BOARD_SIZE))

    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color,
                           (col * SQUARE_SIZE,
                            row * SQUARE_SIZE + BORDER_WIDTH + TIMER_HEIGHT,
                            SQUARE_SIZE, SQUARE_SIZE))

    if selected:
        row, col = selected
        pygame.draw.rect(screen, HIGHLIGHT,
                        (col * SQUARE_SIZE,
                         row * SQUARE_SIZE + BORDER_WIDTH + TIMER_HEIGHT,
                         SQUARE_SIZE, SQUARE_SIZE), 4)
        piece = board.grid[row][col]
        if piece:
            legal_moves = board.get_legal_moves(selected, turn)
            for move in legal_moves:
                r, c = move
                pygame.draw.rect(screen, HIGHLIGHT,
                               (c * SQUARE_SIZE,
                                r * SQUARE_SIZE + BORDER_WIDTH + TIMER_HEIGHT,
                                SQUARE_SIZE, SQUARE_SIZE), 4)

def draw_timer(white_time, black_time):
    white_minutes = int(white_time) // 60
    white_seconds = int(white_time) % 60
    black_minutes = int(black_time) // 60
    black_seconds = int(black_time) % 60

    white_text = timer_font.render(f"Белые: {white_minutes:02}:{white_seconds:02}",
                                 True, (255, 255, 255))
    black_text = timer_font.render(f"Черные: {black_minutes:02}:{black_seconds:02}",
                                 True, (255, 255, 255))

    screen.blit(white_text, (BORDER_WIDTH + 10, HEIGHT - BORDER_WIDTH - 30))
    screen.blit(black_text, (BORDER_WIDTH + 10, BORDER_WIDTH + 10))

def main(minutes=5):
    board = Board()
    running = True
    selected = None
    turn = 'white'

    white_time = minutes * 60
    black_time = minutes * 60
    last_tick = time.time()

    while running:
        now = time.time()
        elapsed = now - last_tick
        last_tick = now

        if turn == 'white':
            white_time -= elapsed
        else:
            black_time -= elapsed

        if white_time <= 0:
            show_game_over("Черные победили по времени!")
            break
        elif black_time <= 0:
            show_game_over("Белые победили по времени!")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = (pos[1] - BORDER_WIDTH - TIMER_HEIGHT) // SQUARE_SIZE
                if 0 <= row < 8 and 0 <= col < 8:
                    if selected is None:
                        if board.grid[row][col] and board.grid[row][col].color == turn:
                            if board.get_legal_moves((row, col), turn):
                                selected = (row, col)
                    else:
                        promotion = None
                        if isinstance(board.grid[selected[0]][selected[1]], Pawn) and (row == 0 or row == 7):
                            promotion = input("Выберите фигуру (queen, rook, knight, bishop): ").lower()
                        if board.move(selected, (row, col), promotion):
                            if board.is_checkmate('black' if turn == 'white' else 'white'):
                                SOUNDS["checkmate"].play()
                                show_game_over(f"Мат! {turn.capitalize()} победили!")
                                running = False
                            turn = 'black' if turn == 'white' else 'white'
                        selected = None

        screen.fill((0, 0, 0))
        draw_board(board, selected, turn)
        board.draw()
        draw_timer(white_time, black_time)
        pygame.display.flip()

    pygame.quit()

def main_menu():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 40)
    selected_time_index = 1
    time_options = [1, 5, 10, 30]

    while True:
        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        start_button = pygame.Rect(WIDTH//2 - 100, 300, 200, 60)
        quit_button = pygame.Rect(WIDTH//2 - 100, 400, 200, 60)
        time_button = pygame.Rect(WIDTH//2 - 100, 500, 200, 60)

        pygame.draw.rect(screen, (70, 130, 180), start_button)
        pygame.draw.rect(screen, (200, 50, 50), quit_button)
        pygame.draw.rect(screen, (100, 100, 100), time_button)

        screen.blit(font.render("Шахматы на Python", True, (255, 255, 255)),
                   (WIDTH//2 - 200, 150))
        screen.blit(small_font.render("Начать игру", True, (255, 255, 255)),
                   (start_button.x + 30, start_button.y + 10))
        screen.blit(small_font.render("Выход", True, (255, 255, 255)),
                   (quit_button.x + 60, quit_button.y + 10))
        time_text = f"Таймер: {time_options[selected_time_index]} мин"
        screen.blit(small_font.render(time_text, True, (255, 255, 255)),
                   (time_button.x + 20, time_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    main(minutes=time_options[selected_time_index])
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif time_button.collidepoint(mouse_pos):
                    selected_time_index = (selected_time_index + 1) % len(time_options)

        pygame.display.flip()
        clock.tick(60)

def show_game_over(message):
    font = pygame.font.SysFont(None, 60)
    screen.fill((30, 30, 30))
    label = font.render(message, True, (255, 255, 255))
    screen.blit(label, label.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.wait(4000)

if __name__ == "__main__":
    main_menu()