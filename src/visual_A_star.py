import copy
import A_star
import pygame
from maze_generator import *


# Inicialización de Pygame
pygame.init()

WIN_SIZE = 400

# Definición de colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (15,67,15)
L_BLUE = (100,149,237)
YELLOW = (255,255,0)
FAKE = (142,112,65)
GRAY = (128, 128, 128)

cell_w = WIN_SIZE // WIDTH
cell_h = WIN_SIZE // HEIGHT
cell = min(cell_w, cell_h)


maze = maze_generator()
steps = A_star.A_star(pos_inicial, goals, maze)

# Creación de la pantalla y dibujar el laberinto
screen = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
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
            elif (row,col) == pos_inicial:
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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            maze, pos = next(steps)  # obtenemos el siguiente estado
        except StopIteration:
            running = False
            continue  # salimos del loop

        screen.fill(GRAY)
        draw_maze(maze)

        # resaltamos la posición actual en amarillo
        pygame.draw.rect(screen, YELLOW, (pos[1]*cell, pos[0]*cell, cell, cell))

        pygame.display.flip()
        pygame.time.delay(250) 
    
    pygame.quit()

if __name__ == "__main__":
    main()