import random
import numpy as np
import math as math

# Tanto el ancho como el largo del laberinto deben ser impares
WIDTH = 11  # Ancho del laberinto
HEIGHT = 11 # Largo del laberinto

# Verificaciones
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3

# Semilla predefinida
SEED = 1
random.seed(SEED)

# Caracteres para mostrar el laberinto
EMPTY_C = ' '
WALL_C = chr(9608) #'█'
WALL_M_C = chr(9633) #'■'
NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'
LOW = chr(9617) #'░'
MID = chr(9618) #'▒'
HEAVY = chr(9619) #'▓'

# Declaracion de constantes
WALL_M = -2
WALL = -1
HOLLOW = 0

# Dleclaracion de variables
mov_wall = [] # Lista de posiciones de las paredes moviles
prob_wall = 0.05 # Probabilidad de que una pared sea una pared movil
prob_move = 0.05 # Probabilidad de que una pared movil se mueva en cada iteracion
goals = [(1,1), (1, HEIGHT-2), (WIDTH-2, 1), (WIDTH-2, HEIGHT-2)] # Posiciones finales posibles, estan predefinidas como las esquinas, aunque despues se podria probar colocandolas aleatoriamente

# Declaracion de variables globales
grid_maze = np.ones((HEIGHT, WIDTH), dtype=int) * -1 # El laberinto al inicio esta completamente hecho de paredes
startx = random.randrange(1, WIDTH,2)
starty = random.randrange(1, HEIGHT,2)
pos_incial = (startx, starty) # Posicion inicial
hasVisited = [(startx, starty)] # Lista de posiciones visitadas

def print_maze_grid(maze):
    p_maze = np.empty((HEIGHT, WIDTH), dtype=str)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if maze[i][j] == WALL:
                p_maze[i][j] = WALL
            elif maze[i][j] == WALL_M:
                p_maze[i][j] = 'M' # Pared movil
            else:
                p_maze[i][j] = str(maze[i][j]) # Peso del nodo
    print(p_maze)

def print_maze(maze):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if maze[i][j] == WALL:
                print(WALL_C, end='')
            elif maze[i][j] == WALL_M:
                print(WALL_M_C, end='') # Pared movil
            elif maze[i][j] < 33:
                print(LOW, end='') # Peso bajo
            elif maze[i][j] < 66:
                print(MID, end='') # Peso medio
            else:
                print(HEAVY, end='') # Peso alto
        print()

def config_maze(maze):

    '''
    Funcion para la configuracion del laberinto, se encarga de recorrer la matriz y
    asignar las paredes moviles y los pesos a los nodos de forma aleatoria
    '''

    # Recorrido de la matriz
    for i in range(HEIGHT):
        for j in range(WIDTH):
            
            # Asignacion de las paredes moviles del laberinto
            if maze[i][j] == WALL:
                if i > 0 and i < HEIGHT-1 and j > 0 and j < WIDTH-1 and random.uniform(0,1) < prob_wall: # Identificacion de pared interna
                        mov_wall.append((i,j)) 
                        maze[i][j] = WALL_M

            elif maze[i][j] == HOLLOW:
                maze[i][j] = random.randint(1, WIDTH + HEIGHT - 2) # Asignacion de un peso aleatorio al nodo

def recursive_backtracker(x,y):

    '''
    Recursive Backtracker Algorithm para la generacion del laberinto inspirado en:
    https://inventwithpython.com/recursion/chapter11.html
    '''

    grid_maze[y][x] = 0

    while True:

        # Verificacion de los vecinos no visitados
        unvisitedNeighbors = []
        if y > 1 and (x, y - 2) not in hasVisited:
            unvisitedNeighbors.append(NORTH)

        if y < HEIGHT - 2 and (x, y + 2) not in hasVisited:
            unvisitedNeighbors.append(SOUTH)

        if x > 1 and (x - 2, y) not in hasVisited:
            unvisitedNeighbors.append(WEST)

        if x < WIDTH - 2 and (x + 2, y) not in hasVisited:
            unvisitedNeighbors.append(EAST)

        # Caso base, indica si estamos en un punto muerto y se realiza el backtracking
        if len(unvisitedNeighbors) == 0:
            return
        # Caso recursivo, se elige un vecino no visitado aleatoriamente
        else:
            nextIntersection = random.choice(unvisitedNeighbors)

            # Movimiento hacia el vecino no visitado
            if nextIntersection == NORTH:
                nextX = x
                nextY = y - 2
                grid_maze[y - 1][x] = 0
            elif nextIntersection == SOUTH:
                nextX = x
                nextY = y + 2
                grid_maze[y + 1][x] = 0
            elif nextIntersection == WEST:
                nextX = x - 2
                nextY = y
                grid_maze[y][x - 1] = 0
            elif nextIntersection == EAST:
                nextX = x + 2
                nextY = y
                grid_maze[y][x + 1] = 0

            hasVisited.append((nextX, nextY)) # Marcado como visitado
            recursive_backtracker(nextX, nextY) # Llamada recursiva

def maze_generator():

    '''
    Funcion principal para la generacion del laberinto
    '''

    recursive_backtracker(startx, starty) # Iniciar la generacion del laberinto
    config_maze(grid_maze) # Configuracion del laberinto
    return grid_maze

def update_maze(maze):
    
    if not mov_wall:
        return
    if random.uniform(0,1) < prob_move:

        dinamic_wall = random.choice(mov_wall)
        mov_wall.remove(dinamic_wall)
        
        posibilities = []

        if maze[dinamic_wall[0]+1][dinamic_wall[1]] >= 0:
            posibilities.append((dinamic_wall[0]+1, dinamic_wall[1]))
        if maze[dinamic_wall[0]-1][dinamic_wall[1]] >= 0:
            posibilities.append((dinamic_wall[0]-1, dinamic_wall[1]))
        if maze[dinamic_wall[0]][dinamic_wall[1]+1] >= 0:
            posibilities.append((dinamic_wall[0], dinamic_wall[1]+1))
        if maze[dinamic_wall[0]][dinamic_wall[1]-1] >= 0:
            posibilities.append((dinamic_wall[0], dinamic_wall[1]-1))
        
        move = random.choice(posibilities)

        swap = maze[dinamic_wall[0]][dinamic_wall[1]]
        maze[dinamic_wall[0]][dinamic_wall[1]] = maze[move[0]][move[1]]
        maze[move[0]][move[1]] = swap
        print("Se ha movido una pared de:", dinamic_wall, "a", move)
        print(maze)

def get_neighbors(node, maze, queue, visited):
    neighbors = []
    x = node[0]
    y = node[1]

    if maze[x+1][y] > 0 and (x+1,y) not in queue and (x+1,y) not in visited:
        neighbors.append((x+1,y))
    if maze[x][y+1] > 0 and (x,y+1) not in queue and (x,y+1) not in visited:
        neighbors.append((x,y+1))
    if maze[x-1][y] > 0 and (x-1,y) not in queue and (x-1,y) not in visited:
        neighbors.append((x-1,y))
    if maze[x][y-1] > 0 and (x,y-1) not in queue and (x,y-1) not in visited:
        neighbors.append((x,y-1))
        
    return neighbors

#MAIN PROVISORIO

# maze = maze_generator()

# print(maze)
# print()
# # A_star(pos_incial, goals, maze)
# print()
# print(maze)

# # graph = maze_to_graph(grid_maze)
# config_maze(grid_maze)
# # print()
# print(grid_maze)

# print()
# print("Paredes moviles:", mov_wall)
# print("Posiciones finales posibles:", final_pos)
# print()

# La heuristica de cada nodo sera la distancia de manhattan a la salida mas cercana
# tenemos la ubicacion de las 4 salidas por lo que podemos calcular la distancia y
# en base a eso decidir hacia donde movernos

# Para los pesos lo que se va a hacer es mientras mas cerca esté un nodo de una pared
# movil, mayor sera su peso, y mientras mas lejos este un nodo de una pared movil, menor
# será su peso