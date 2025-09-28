import random, pygame
import A_star
import pygame
from maze_generator import *


# Inicialización de Pygame
pygame.init()

cell = 20

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (15,67,15)
L_BLUE = (100,149,237)
YELLOW = (255,255,0)
FAKE = (142,112,65)

maze = maze_generator()

maze = A_star.A_star(pos_incial, goals, maze)

# Creación de la pantalla y dibujar el laberinto
screen = pygame.display.set_mode((WIDTH * cell, HEIGHT * cell))
pygame.display.set_caption("Maze")

# Dibujar el laberinto en pantalla
def draw_maze(maze):
    for row in range(len(maze)):
        for col in range(len(maze[1])):
            if maze[row][col] == -1:
                pygame.draw.rect(screen, BLACK, (col * cell, row * cell, cell, cell))
            elif maze[row][col] == -2:
                pygame.draw.rect(screen, RED, (col * cell, row * cell, cell, cell))
            elif maze[row][col] == 0:
                pygame.draw.rect(screen, BLUE, (col * cell, row * cell, cell, cell))
            elif (row,col) == pos_incial:
                pygame.draw.rect(screen, L_BLUE, (col * cell, row * cell, cell, cell))
            elif (row,col) in goals:
                if (row,col) == true_goal:
                    pygame.draw.rect(screen, GREEN, (col * cell, row * cell, cell, cell))
                else:
                    pygame.draw.rect(screen, DARK_GREEN, (col * cell, row * cell, cell, cell))
            elif maze[row][col] == -4:
                pygame.draw.rect(screen, YELLOW, (col * cell, row * cell, cell, cell))
            elif maze[row][col] == -3:
                pygame.draw.rect(screen, FAKE, (col * cell, row * cell, cell, cell))


#El bucle principal
def main():
    global running
    running = True
    # print(laberinto)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                

        screen.fill(WHITE)
        draw_maze(maze)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()