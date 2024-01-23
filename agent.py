# A*

from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w, FULLSCREEN
from random import randint
import pygame
from numpy import sqrt

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
display.set_caption("Snake Game Agent - A* Algorithm")
clock = time.Clock()

def finding_path(food1, snake1):
    # Initialize camefrom for the food and all segments of the snake
    food1.camefrom = []
    for s in snake1:
        s.camefrom = []
    # Initialize the open and closed sets and direction array
    openset = [snake1[-1]]
    closedset = []
    dir_array1 = []
    # Loop until the optimal path to the food is found
    while 1:
        # Get the segment with the lowest f score from the open set
        current1 = min(openset, key=lambda x: x.f)
        # Remove the current segment from the open set and add it to the closed set
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        closedset.append(current1)
        # Update the g, h, and f scores for each neighbor of the current segment
        for neighbor in current1.neighbors:
            # Only consider neighbors that are not obstacles, not in the closed set, and not part of the snake
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.camefrom = current1
        # If the food segment has been reached, break out of the loop
        if current1 == food1:
            break
    # Trace back the path from the food to the snake's head using the camefrom pointers
    while current1.camefrom:
        if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
            dir_array1.append(2)  # Up
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(0)  # Down
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(3)  # Left
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(1)  # Right
        current1 = current1.camefrom
    # Reset the camefrom, f, h, and g values for all segments of the grid
    for i in range(rows):
        for j in range(columns):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
    # Return the direction array
    return dir_array1

class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # f: represents the sum of g and h. This value is used to determine the priority of the node in the open set,
        # which is the set of nodes that are currently being considered for expansion by the algorithm.
        self.f = 0
        # g: represents the cost of the path from the start node to the current node.
        self.g = 0
        # h: represents the estimated cost from the current node to the goal node.
        # This is typically calculated as the straight-line distance between the two nodes in Euclidean space
        # although other heuristics can be used as well.
        self.h = 0

        self.neighbors = []
        self.camefrom = []
        self.obstrucle = False
        if (self.x == 0 or self.y == 0 or self.x == (columns - 1) or self.y == (rows - 1)):
            self.obstrucle = True

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

def print_path(dir_path):
    dir_array = []
    for i in range(len(dir_path)):
        if dir_path[i] == 0:
            dir_array.append("Down")
        elif dir_path[i] == 1:
            dir_array.append("Right")
        elif dir_path[i] == 2:
            dir_array.append("Up")
        elif dir_path[i] == 3:
            dir_array.append("Left")
    dir_array.reverse()
    print(dir_array)

def display_score(score):
    font = pygame.font.SysFont(None, 25)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen(score):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 50)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(game_over_text, (width // 2 - 100, height // 2 - 50))
    screen.blit(score_text, (width // 2 - 50, height // 2))
    display.flip()

# Create a 2D array of Spot objects representing the grid
grid = [[Spot(i, j) for j in range(columns)] for i in range(rows)]

# Add neighbors to each Spot object in the grid
for i in range(rows):
    for j in range(columns):
        grid[i][j].add_neighbors()

snake = [grid[round(rows / 2)][round(columns / 2)]]
food = grid[randint(0, rows - 1)][randint(0, columns - 1)]
current = snake[-1]

dir_array = finding_path(food, snake)
food_array = [food]
score = 0

# New window to display score when the game window is closed
score_window = display.set_mode([600, 600])

try:
    while not done:
        clock.tick(4)
        screen.fill(BLACK)
        print_path(dir_array)
        direction = dir_array.pop(-1)

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
                if not (food.obstrucle or food in snake):
                    break
            food_array.append(food)
            dir_array = finding_path(food, snake)
        else:
            snake.pop(0)

        for spot in snake:
            spot.show(WHITE)
        for i in range(rows):
            for j in range(columns):
                if grid[i][j].obstrucle:
                    grid[i][j].show(RED)

        food.show(GREEN)
        snake[-1].show(BLUE)

        display_score(score)

        display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_w and not direction == 0:
                    direction = 2
                elif event.key == K_a and not direction == 1:
                    direction = 3
                elif event.key == K_s and not direction == 2:
                    direction = 0
                elif event.key == K_d and not direction == 3:
                    direction = 1

    if len(snake) == rows * columns:
        game_over_screen(score)
        pygame.time.delay(3000)
        done = True

finally:
    # Game window is closed, display the score window
    score_window.fill(BLACK)
    font = pygame.font.SysFont(None, 25)
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_window.blit(score_text, (50, 50))
    display.flip()

    # Keep the score window open until the user closes it
    score_done = False
    while not score_done:
        for event in pygame.event.get():
            if event.type == QUIT:
                score_done = True

pygame.quit()
