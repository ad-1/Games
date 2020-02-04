import pygame
import random


class App:
    """
        Pygame snake app
    """

    def __init__(self):
        self._running = True
        self._display_surf = None
        size = self.width, self.height = 500, 500
        pygame.init()
        self.clock = pygame.time.Clock()
        self._display_surf = pygame.display.set_mode(size)
        self._display_surf.fill((0, 0, 0))
        self.font = pygame.font.SysFont(None, 30)
        pygame.display.flip()
        pygame.display.set_caption('Snake')
        self.block_size = 10
        self.snake = None
        self.food = None
        self.restart = False

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if not self.snake.alive:
                self._running = False
                if event.key != pygame.K_q:
                    self.restart = True
            else:
                self.snake.change_direction(event)

    def on_loop(self):
        if self.check_boundary_condition():
            self.snake.move()
            self.eat_food()
        else:
            self.snake.stop()

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        pygame.draw.rect(self._display_surf, self.food.color, self.food.dim)
        self.draw_snake()
        if not self.snake.alive:
            self.message('Game Over', (255, 0, 0), -50)
            self.message('Score {}'.format(self.snake.length), (0, 255, 0), 0)
            self.message('Press any key to pay again or Q to quit', (255, 255, 255), +50)
        pygame.display.update()
        self.clock.tick(15)

    def on_execute(self):
        self.create_objects()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        if self.restart:
            self.restart_game()
        self.on_cleanup()

    def restart_game(self):
        self.snake = None
        self.food = None
        self._running = True
        self.restart = False
        self.on_execute()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def message(self, msg, color, y_displacement):
        text_surface = self.font.render(msg, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.width / 2, (self.height / 2) + y_displacement)
        self._display_surf.blit(text_surface, text_rect)

    def check_boundary_condition(self):
        if self.snake.head[0] < 0 or self.snake.head[0] > self.width - self.block_size or \
                self.snake.body[-1][1] < 0 or self.snake.body[-1][1] > self.width - self.block_size:
            return False
        if self.snake.head in self.snake.body[:-2]:
            return False
        return True

    def create_objects(self):
        if self.snake is None:
            self.snake = Snake(self.width, self.height, self.block_size)
        self.add_food()

    def add_food(self):
        if self.food is None:
            x = round(random.randint(0, self.width - self.block_size) / 10.0) * 10.0
            y = round(random.randint(0, self.height - self.block_size) / 10.0) * 10.0
            if [x, y] not in self.snake.body:
                self.food = Food(x, y, self.block_size)
            else:
                self.add_food()

    def eat_food(self):
        if self.food.dim[0] <= self.snake.head[0] <= self.food.dim[0] + self.block_size and \
                self.food.dim[1] <= self.snake.head[1] <= self.food.dim[1] + self.block_size:
            self.snake.grow()
            self.food = None
            self.add_food()

    def draw_snake(self):
        body_parts = self.snake.body
        for p in body_parts:
            pygame.draw.rect(self._display_surf, self.snake.color, [p[0], p[1], self.block_size, self.block_size])


class Snake:
    """
        Snake object
    """

    def __init__(self, screen_width, screen_height, block_size):
        x = round((screen_width / 2) / 10.0) * 10.0
        y = round((screen_height / 2) / 10.0) * 10.0
        self.head = [x, y]
        self.body = [self.head]
        self.color = 0, 0, 255
        self.dim = [x, y, block_size, block_size]
        self.dx = 10
        self.dy = 0
        self.alive = True
        self.length = 1

    def change_direction(self, event):
        velocity = self.dim[2]
        if self.dx == 0:
            if event.key == pygame.K_LEFT:
                self.dx = -velocity
                self.dy = 0
            elif event.key == pygame.K_RIGHT:
                self.dx = velocity
                self.dy = 0
        elif self.dy == 0:
            if event.key == pygame.K_UP:
                self.dy = -velocity
                self.dx = 0
            elif event.key == pygame.K_DOWN:
                self.dy = velocity
                self.dx = 0

    def move(self):
        self.head = self.body[-1]
        self.head[0] += self.dx
        self.head[1] += self.dy
        if len(self.body) > self.length:
            del self.body[0]
        self.body.append([self.head[0], self.head[1]])

    def stop(self):
        self.dx = 0
        self.dy = 0
        self.alive = False

    def grow(self):
        self.length += 1


class Food:
    """
        Food object
    """

    def __init__(self, x, y, block_size):
        width = block_size
        height = block_size
        self.color = 255, 0, 0
        self.dim = [x, y, width, height]


# Driver program to run app
if __name__ == "__main__":
    app = App()
    app.on_execute()
