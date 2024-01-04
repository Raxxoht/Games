## Welcome to the game

## Expect to be entertained and to learn

import pygame as game, random as rand, sys ## Import pygame, random and system libraries
from pygame.math import Vector2
game.init() ## Start the game process



class SNAKE():
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.body_vertical = game.image.load("Snake/Images/snake_body_ver.png").convert_alpha()
        self.body_horizontal = game.image.load("Snake/Images/snake_body_hor.png").convert_alpha()

        self.head_up = game.image.load("Snake/Images/snake_head_up.png").convert_alpha()
        self.head_down = game.image.load("Snake/Images/snake_head_down.png").convert_alpha()
        self.head_left = game.image.load("Snake/Images/snake_head_left.png").convert_alpha()
        self.head_right = game.image.load("Snake/Images/snake_head_right.png").convert_alpha()

        self.tail_up = game.image.load("Snake/Images/snake_tail_up.png").convert_alpha()
        self.tail_down = game.image.load("Snake/Images/snake_tail_down.png").convert_alpha()
        self.tail_left = game.image.load("Snake/Images/snake_tail_left.png").convert_alpha()
        self.tail_right = game.image.load("Snake/Images/snake_tail_right.png").convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = block.x*cell_size
            y_pos = block.y*cell_size
            block_rect = game.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0 :
                screen.blit(self.head, block_rect)

            elif index == len(self.body)-1 :
                screen.blit(self.tail, block_rect)
            else:
                game.draw.rect(screen, (150,100,100), block_rect)



        #for block in self.body:
        #    block_rect = game.Rect(int(block.x*cell_size), int(block.y*cell_size), cell_size, cell_size)
        #    screen.blit(snake_png, block_rect)
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        
        if head_relation == right: self.head = self.head_left
        elif head_relation == left: self.head = self.head_right
        elif head_relation == up: self.head = self.head_down
        elif head_relation == down: self.head = self.head_up

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        
        if tail_relation == right: self.tail = self.tail_left
        elif tail_relation == left: self.tail = self.tail_right
        elif tail_relation == up: self.tail = self.tail_down
        elif tail_relation == down: self.tail = self.tail_up

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
        else:
            body_copy = self.body[:-1]
        
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]
        self.new_block = False

    def add_block(self):
        self.new_block = True

class FRUIT:
    def __init__(self):
        self.x = rand.randint(0,cell_number-1)
        self.y = rand.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = game.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        #game.draw.rect(screen,(126,166,114),fruit_rect)

    def newPos(self):
        self.x = rand.randint(0,cell_number-1)
        self.y = rand.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)


class Main(): ## Main logic engine
    def __init__(self):
        self.snake = SNAKE() 
        self.fruit = FRUIT()
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            print('"Tasty"')
            self.score += 1
            print("Score = ", self.score)
            self.snake.add_block()
            self.fruit.newPos()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()


    def game_over(self):
        game.quit()
        sys.exit()

cell_size = 20
cell_number = 20
right = Vector2(1, 0) ## Define vectors for each direction
left = Vector2(-1, 0)
up = Vector2(0, -1)
down = Vector2(0, 1)

screen = game.display.set_mode((cell_number*cell_size,cell_number*cell_size)) ## Define our screen
clock = game.time.Clock() ## Define a clock object to use time methods
apple = game.image.load("Snake/Images/Apple.png").convert_alpha() ## Made my own sprite for this 

SCREEN_UPDATE = game.USEREVENT
game.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

while True: ## While loop to keep the game running 
    snake = main_game.snake
    for event in game.event.get(): ## Loop for every event in the pygame process
        if event.type == game.QUIT: ## Check if the user want to quit using the red cross in the corner
            game.quit() ## Quit the game
            sys.exit() ## Exit current program
        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == game.KEYDOWN:
            if event.key == game.K_UP  and snake.direction != down:
                ## Checking key events and adding corresponding vector
                snake.direction = up # Up
            elif event.key == game.K_DOWN and snake.direction != up: 
                snake.direction = down # Down 
            elif event.key == game.K_LEFT and snake.direction != right:
                snake.direction = left # Left
            elif event.key == game.K_RIGHT and snake.direction != left:
                snake.direction = right # Right
            elif event.key == game.K_ESCAPE:
                game.quit()
                sys.exit()
    screen.fill(game.Color((175,210,70))) ## Fill the screen, rgb value
    main_game.draw_elements()
    game.display.update() ## Update current display
    clock.tick(60) ## Game tick limit per second, aka fps limiter