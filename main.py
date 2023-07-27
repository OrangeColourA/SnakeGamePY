import pygame
import sys
import time
import random

pygame.init()
cell_size = 35
cell_number = 20
WIDTH, HEIGHT = cell_size * cell_number, cell_size * cell_number
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Needy Greedy Snake")

PLAYER_WIDTH = 35
PLAYER_HEIGHT = 35
PLAYER_VEL = 15
PLAYER_JUMP = 215
GRAVITY = 5
SCREEN_UPDATE = pygame.USEREVENT

apple = pygame.image.load('Graphics/Apple.png').convert_alpha()
apple = pygame.transform.scale(apple, (35, 35))


class Snake:
    def __init__(self):
        self.body = [pygame.math.Vector2(6, 10), pygame.math.Vector2(5, 10)]
        self.direction = pygame.math.Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(WIN, 'dark blue', block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class Fruit:
    def __init__(self):
        self.x = None
        self.y = None
        self.pos = None
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        WIN.blit(apple, fruit_rect)
        # pygame.draw.rect(WIN, 'red', fruit_rect)

    def randomize(self):
        self.x = random.randint(1, cell_number - 2)
        self.y = random.randint(1, cell_number - 2)
        self.pos = pygame.math.Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        if not 1 <= self.snake.body[0].x <= cell_number - 2:
            self.game_over()
        if not 1 <= self.snake.body[0].y <= cell_number - 2:
            self.game_over()
        for block in self.snake.body[1:]:
            if block.x == self.snake.body[0].x and block.y == self.snake.body[0].y:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


def draw():
    # pygame.draw.rect(WIN, 'dark blue', player)

    pygame.display.update()


'''
def erase(x, y):
    player_erase = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
    pygame.draw.rect(WIN, 'black', player_erase)

    pygame.display.update()
'''


def main():
    run = True

    test_surface = pygame.Surface((630, 630))   # создаем поверхность

    player = pygame.Rect(350, 350, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()

    pygame.time.set_timer(SCREEN_UPDATE, 150)

    main_game = Main()

    while run:
        clock.tick(60)  # ограничиваем кадры в секунду

        WIN.fill((100, 150, 255))  # заполняем окно цветом
        WIN.blit(test_surface, (35, 35))  # рисуем поверхность
        test_surface.fill('dark green')

        main_game.draw_elements()

        for event in pygame.event.get():    # цикл для закрытия
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                    main_game.snake.direction = pygame.math.Vector2(0, -1)
                if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                    main_game.snake.direction = pygame.math.Vector2(0, 1)
                if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                    main_game.snake.direction = pygame.math.Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                    main_game.snake.direction = pygame.math.Vector2(1, 0)

        draw()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
