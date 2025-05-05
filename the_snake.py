from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс родитель для змейки и яблока"""

    def __init__(self):
        self.position = None
        self.body_color = None

    def draw(self):
        """Заготовка для метода отрисовки классов наследников"""
        pass


def handle_keys(game_object):
    """Функция, обрабатывающая действия игрока (нажатые кнопки)."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class Snake(GameObject):
    """Класс наследник GameObject. Представляет собой саму змейку."""

    def __init__(self):
        super().__init__()
        self.positions = [(SCREEN_WIDTH // 2 - GRID_SIZE,
                           SCREEN_HEIGHT // 2 - GRID_SIZE)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def draw(self):
        """Метод, рисующий змейку"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод, обновляющий движение змейки. Змейка не меняет свое
        направление до тех пор, пока пользователь не нажмет какую-либо
        клавишу действия. При нажатии функция handle_keys, получающая
        на вход саму змейку меняет ее направление, т.е. изменяет атрибут
        next_direction. Следовательно, если он изменился, то нужно поменять
        текущее направление.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, двигающий змейку. Т.е.  обновляет позицию змейки
        (координаты каждой секции), добавляя новую голову в начало
        списка positions и удаляя последний элемент, если длина
        змейки не увеличилась.
        """
        current_head = self.get_head_position()
        new_position = (
            (self.direction[0] * GRID_SIZE + current_head[0]) % SCREEN_WIDTH,
            (self.direction[1] * GRID_SIZE + current_head[1]) % SCREEN_HEIGHT)

        if new_position in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None

    def get_head_position(self):
        """Метод, возвращающий голову змейки, т.е. возвращает
        первый элемент массива self.positions.
        """
        return self.positions[0]

    def reset(self):
        """Метод, возвращающий змейку в начальное положение"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


class Apple(GameObject):
    """Класс наследник GameObject. Представляет собой яблоко."""

    def randomize_position(self):
        """Метод, возвращающий случайное новое положение яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def __init__(self):
        super().__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Метод, рисующий яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def main():
    """Основной игровой цикл. Создание экземпляров классов,
    обработка событий клавиш, изменение положений змейки и яблока,
    проверка столкновения змейки, отрисовка объеков и обновление экрана
    """
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убедимся, что яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
