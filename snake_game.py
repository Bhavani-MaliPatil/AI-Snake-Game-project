import pygame
import random
from collections import deque
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Directions (Up, Down, Left, Right)
DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def place_food(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

def draw_snake(snake):
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    x, y = food
    pygame.draw.circle(screen, RED, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def show_game_over(score):
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 30))
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
    pygame.display.update()
    time.sleep(3)

def bfs_path(snake, food):
    """Find shortest path from snake head to food avoiding snake body."""
    start = snake[0]
    queue = deque([(start, [])])
    visited = {start}

    while queue:
        current, path = queue.popleft()

        if current == food:
            return path

        for dx, dy in DIRS:
            nx, ny = current[0] + dx, current[1] + dy
            next_pos = (nx, ny)

            if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and
                next_pos not in snake and next_pos not in visited):
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))

    return []  # No path found

def game_loop():
    snake = [(5, 5), (4, 5), (3, 5)]
    food = place_food(snake)
    score = 0

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Find path to food
        path = bfs_path(snake, food)

        if path:
            next_cell = path[0]
        else:
            # Try to move in a safe random direction
            moved = False
            for dx, dy in DIRS:
                nx, ny = snake[0][0] + dx, snake[0][1] + dy
                if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in snake):
                    next_cell = (nx, ny)
                    moved = True
                    break
            if not moved:
                show_game_over(score)
                pygame.quit()
                return

        # Move snake
        snake.insert(0, next_cell)

        # Check collisions
        if (snake[0] in snake[1:] or
            snake[0][0] < 0 or snake[0][0] >= GRID_WIDTH or
            snake[0][1] < 0 or snake[0][1] >= GRID_HEIGHT):
            show_game_over(score)
            pygame.quit()
            return

        # Eat food
        if snake[0] == food:
            score += 1
            food = place_food(snake)
        else:
            snake.pop()

        # Draw game
        draw_snake(snake)
        draw_food(food)
        show_score(score)

        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    game_loop()
