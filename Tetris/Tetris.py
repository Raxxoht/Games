#THIS IS THE START OF MY TETRIS GAME
from setGame import *
from sys import exit
import pygame
import random

class Tetromino:
    def __init__(self, shape):
        self.shape = shape # Shape is defined upon initializing the class with an input parameter
        self.color = shape_colors[Shapes.index(shape)] # The colors are mapped to align with each shape's index, could have a customization feature later
        self.x = columns // 2 - len(shape[0]) // 2 # Center positioning on the x axis
        self.y = 0 # Starts at the top

    def rotate(self): # Defining the function used to rotate the current block
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, surface, offset_x=0, offset_y=0):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((self.x + x + offset_x) * cell_size + padding, 
                                       (self.y + y + offset_y) * cell_size + padding, 
                                       cell_size, cell_size)
                    pygame.draw.rect(surface, self.color, rect)
                    pygame.draw.rect(surface, (50, 50, 50), rect, 1)


class Main:
    
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((window_width,window_height))
        self.grid = [[(0,0,0) for _ in range(columns)] for _ in range(rows)] # Displaying the grid element as full black squares, this is its initial state and will display blocks
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.current_piece = Tetromino(random.choice(Shapes))
        self.next_piece = Tetromino(random.choice(Shapes))
        self.score = 0
        self.game_over = False


    def draw_score(self):
        pygame.font.init()
        my_font = pygame.font.SysFont("Calibri", 20)
        text_surface = my_font.render(f'Score: {self.score}', False, (255, 255, 255))
        self.display_surface.blit(text_surface, (0,0))

    def draw_score(self):
        font = pygame.font.SysFont("Calibri", 30)
        text_surface = font.render(f'Score: {self.score}', False, (255, 255, 255))
        self.display_surface.blit(text_surface, (game_width + 2 * padding, padding))

    def draw_next_piece(self):
        font = pygame.font.SysFont("Calibri", 24)
        text_surface = font.render("Next piece", False, (255, 255, 255))
        self.display_surface.blit(text_surface, (game_width + 2 * padding, 60))
        
        next_piece_x = game_width + 2 * padding
        next_piece_y = 90
        
        # Draw grey box
        box_width = 4 * cell_size
        box_height = 4 * cell_size
        pygame.draw.rect(self.display_surface, (200, 200, 200), 
                         pygame.Rect(next_piece_x, next_piece_y, box_width, box_height), 2)

        # Calculate the offset for centering the next piece inside the grey box
        piece_width = len(self.next_piece.shape[0])
        piece_height = len(self.next_piece.shape)
        offset_x = (4 - piece_width) // 2
        offset_y = (4 - piece_height) // 2

        # Draw the next piece inside the grey box
        self.next_piece.draw(self.display_surface, offset_x + (next_piece_x // cell_size - columns/2), offset_y + (next_piece_y // cell_size))

    def clear_lines(self):
        lines_cleared = 0
        for y in range(rows):
            if all(cell != (0, 0, 0) for cell in self.grid[y]):
                lines_cleared += 1
                del self.grid[y]
                self.grid.insert(0, [(0, 0, 0) for _ in range(columns)])
        return lines_cleared

    def draw_grid(self):
        for y in range(rows):
            for x in range(columns):
                color = self.grid[y][x]
                rect = pygame.Rect(x * cell_size + padding, y * cell_size + padding, cell_size, cell_size)
                pygame.draw.rect(self.display_surface, color, rect)
                pygame.draw.rect(self.display_surface, (50, 50, 50), rect, 1)  # Draw cell border

    def draw_current_piece(self):
        self.current_piece.draw(self.display_surface)

    def freeze_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color

        for x in range(columns): # Game over check
            if self.grid[0][x] != (0, 0, 0):
                self.game_over = True
                break
        return self.clear_lines()
 
    def valid_space(self, shape, offset):
        off_x, off_y = offset
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if x + off_x < 0 or x + off_x >= columns or y + off_y >= rows:
                        return False
                    if self.grid[y + off_y][x + off_x] != (0, 0, 0):
                        return False
        return True
    
    def run(self):
        while not self.game_over:
            self.display_surface.fill((0, 0, 0))
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            if self.fall_time / 1000 > 1:  # Move piece down every 0.5 seconds
                self.fall_time = 0
                if not self.valid_space(self.current_piece.shape, (self.current_piece.x, self.current_piece.y + 1)):
                    lines_cleared = self.freeze_piece()
                    self.score += len(self.current_piece.shape)
                    self.score += lines_cleared * 10 
                    self.current_piece = self.next_piece
                    self.next_piece = Tetromino(random.choice(Shapes))
                else:
                    self.current_piece.y += 1


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.valid_space(self.current_piece.shape, (self.current_piece.x - 1, self.current_piece.y)):
                            self.current_piece.x -= 1  # Move left
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_space(self.current_piece.shape, (self.current_piece.x + 1, self.current_piece.y)):
                            self.current_piece.x += 1  # Move right
                    elif event.key == pygame.K_DOWN:
                        if self.valid_space(self.current_piece.shape, (self.current_piece.x, self.current_piece.y + 1)):
                            self.current_piece.y += 1  # Move down
                    elif event.key == pygame.K_UP:
                        rotated_shape = [list(row) for row in zip(*self.current_piece.shape[::-1])]
                        if self.valid_space(rotated_shape, (self.current_piece.x, self.current_piece.y)):
                            self.current_piece.rotate()  # Rotate
                    elif event.key == pygame.K_SPACE:
                        while self.valid_space(self.current_piece.shape, (self.current_piece.x, self.current_piece.y + 1)):
                            self.current_piece.y += 1
                        self.fall_time = 0


            self.draw_grid()
            self.draw_current_piece()
            self.draw_score()
            self.draw_next_piece()
            pygame.display.update()

if __name__ == "__main__":
    print("Starting tetris...")
    main = Main()
    main.run()
else:
    print("Not running from main")
