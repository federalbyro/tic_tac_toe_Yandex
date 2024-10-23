import pygame
import sys

# Инициализация Pygame
pygame.init()

# Определение констант
CELL_SIZE = 100
BOARD_SIZE = 3
WIDTH = HEIGHT = CELL_SIZE * BOARD_SIZE
LINE_WIDTH = 15
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)
X_WIDTH = 15
O_WIDTH = 15
SPACE = CELL_SIZE // 4

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Крестики-нолики')
screen.fill(BG_COLOR)

# Шрифты для отображения текста
FONT = pygame.font.SysFont('Arial', 40)

# Класс для управления игровым полем
class Board:
    def __init__(self):
        # Инициализация пустого поля
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.field_size = BOARD_SIZE

    def make_move(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
        else:
            raise CellOccupiedError("Ячейка уже занята.")

    def check_win(self, player):
        # Проверка строк
        for row in self.board:
            if all(cell == player for cell in row):
                return True

        # Проверка столбцов
        for col in range(BOARD_SIZE):
            if all(self.board[row][col] == player for row in range(BOARD_SIZE)):
                return True

        # Проверка диагоналей
        if all(self.board[i][i] == player for i in range(BOARD_SIZE)):
            return True
        if all(self.board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
            return True

        return False

    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def reset_board(self):
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Классы исключений
class CellOccupiedError(Exception):
    pass

class FieldIndexError(Exception):
    pass

# Функция для сохранения результатов игры
def save_result(result):
    with open('results.txt', 'a', encoding='utf-8') as f:
        f.write(result + '\n')

# Функция для отрисовки линий на поле
def draw_lines():
    # Горизонтальные линии
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, i * CELL_SIZE),
            (WIDTH, i * CELL_SIZE),
            LINE_WIDTH
        )

    # Вертикальные линии
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, HEIGHT),
            LINE_WIDTH
        )

# Функция для отрисовки фигур (X и O) на поле
def draw_figures(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'X':
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE),
                    (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + CELL_SIZE - SPACE),
                    X_WIDTH
                )
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (col * CELL_SIZE + SPACE, row * CELL_SIZE + CELL_SIZE - SPACE),
                    (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + SPACE),
                    X_WIDTH
                )
            elif board[row][col] == 'O':
                pygame.draw.circle(
                    screen,
                    O_COLOR,
                    (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                    CELL_SIZE // 2 - SPACE,
                    O_WIDTH
                )

# Функция для отображения текста на экране
def display_message(message):
    text = FONT.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)

# Основная функция игры
def main():
    game = Board()
    current_player = 'X'
    running = True
    game_over = False

    draw_lines()
    draw_figures(game.board)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = event.pos
                clicked_row = mouse_y // CELL_SIZE
                clicked_col = mouse_x // CELL_SIZE

                try:
                    if clicked_row < 0 or clicked_row >= game.field_size or clicked_col < 0 or clicked_col >= game.field_size:
                        raise FieldIndexError("Индекс поля вне допустимого диапазона.")
                    if game.board[clicked_row][clicked_col] != ' ':
                        raise CellOccupiedError("Ячейка уже занята.")

                    game.make_move(clicked_row, clicked_col, current_player)
                    draw_figures(game.board)

                    if game.check_win(current_player):
                        save_result(f'Победили {current_player}')
                        display_message(f'Победили {current_player}!')
                        game_over = True
                    elif game.is_board_full():
                        save_result('Ничья')
                        display_message('Ничья!')
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'

                except FieldIndexError as fie:
                    print(fie)
                except CellOccupiedError as coe:
                    print(coe)
                except Exception as e:
                    print(f'Возникла ошибка: {e}')

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
