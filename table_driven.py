# Table Driven

from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame

init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
columns = 20
rows = 20
width = 600
height = 600
widthOfCell = width / columns
heightOfCell = height / rows
direction = 1

screen = display.set_mode([width, height])
display.set_caption("Snake Game Agent - Table Driven")
clock = time.Clock()

class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.obstacle = False
        if (self.x == 0 or self.y == 0 or self.x == (columns - 1) or self.y == (rows - 1)):
            self.obstacle = True

    def show(self, color):
        draw.rect(screen, color, [self.x * heightOfCell + 2, self.y * widthOfCell + 2, heightOfCell - 4, widthOfCell - 4])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < columns - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

def table_driven_agent(food, snake):
    head = snake[-1]
    food_pos = (food.x, food.y)
    head_pos = (head.x, head.y)
    direction = calculate_nearest_direction(head_pos[0], head_pos[1], food_pos[0], food_pos[1])
    

    print("------------------------", food_pos) 
    print("------------------------", head_pos) 
    print("------------------------", direction)
     
    if(direction == 'left'):
        return 3
    if(direction == 'right'):
        return 1
    if(direction == 'top'):
        return 2
    if(direction == 'bottom'):
        return 0 
    else:
        return 0
    





    return 1;


def calculate_nearest_direction(x1, y1, x2, y2):
    # Calculate differences in coordinates
    delta_x = x2 - x1
    delta_y = y2 - y1

    # Determine the nearest direction
    if abs(delta_y) > abs(delta_x):
        if delta_y > 0:
            return "bottom"
        elif delta_y < 0:
            return "top"
    else:
        if delta_x > 0:
            return "right"
        elif delta_x < 0:
            return "left"



grid = [[Spot(i, j) for j in range(columns)] for i in range(rows)]

for i in range(rows):
    for j in range(columns):
        grid[i][j].add_neighbors()

snake = [grid[round(rows / 2)][round(columns / 2)]]
food = grid[randint(0, rows - 1)][randint(0, columns - 1)]
current = snake[-1]

score = 0

font = pygame.font.Font(None, 36)

try:
    while not done:
        clock.tick(4)
        screen.fill(BLACK)

        direction = table_driven_agent(food, snake)

        if direction == 0:
            snake.append(grid[current.x][current.y + 1])
        elif direction == 1:
            snake.append(grid[current.x + 1][current.y])
        elif direction == 2:
            snake.append(grid[current.x][current.y - 1])
        elif direction == 3:
            snake.append(grid[current.x - 1][current.y])
        current = snake[-1]

        if current.x == food.x and current.y == food.y:
            score += 1
            while 1:
                food = grid[randint(0, rows - 1)][randint(0, columns - 1)]
                if not (food.obstacle or food in snake):
                    break
        else:
            snake.pop(0)

        for spot in snake:
            spot.show(WHITE)
        for i in range(rows):
            for j in range(columns):
                if grid[i][j].obstacle:
                    grid[i][j].show(RED)

        food.show(GREEN)
        snake[-1].show(BLUE)

        # Render the score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()


finally:
    pygame.quit()