import random
import numpy as np
import math as math

# Tanto el ancho como el largo del laberinto deben ser impares
WIDTH = 21  # Ancho del laberinto
HEIGHT = 21 # Largo del laberinto

# Verificaciones
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3

# Semilla predefinida
SEED = 3
random.seed()

# Declaracion de constantes
WALL_M = -2
WALL = -1
HOLLOW = 0

# Dleclaracion de variables
mov_wall = [] # Lista de posiciones de las paredes moviles
prob_wall = 0.35 # Probabilidad de que una pared sea una pared movil
prob_move = 0.35 # Probabilidad de que una pared movil se mueva en cada iteracion
goals = [(1,1), (HEIGHT-2, 1), (1, WIDTH-2), (WIDTH-2, HEIGHT-2)] # Posiciones finales posibles, estan predefinidas como las esquinas, aunque despues se podria probar colocandolas aleatoriamente
true_goal = random.choice(goals)

# Declaracion de variables globales
grid_maze = np.ones((HEIGHT, WIDTH), dtype=int) * -1 # El laberinto al inicio esta completamente hecho de paredes
startx = random.randrange(1, WIDTH,2)
starty = random.randrange(1, HEIGHT,2)
pos_inicial = (starty, startx) # Posicion inicial
hasVisited = [(starty, startx)] # Lista de posiciones visitadas


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


def maze_generator():

    '''
    Funcion principal para la generacion del laberinto
    '''
    '''
    Genera un campo abierto con obstáculos aleatorios de baja densidad.
    Es la forma más simple de garantizar (con alta probabilidad) la transibilidad.
    '''
    global grid_maze, mov_wall

    for i in range(HEIGHT):
        for j in range(WIDTH):
            # Bordes siempre paredes
            if i == 0 or i == HEIGHT-1 or j == 0 or j == WIDTH-1:
                grid_maze[i][j] = WALL
            else:
                if random.random() < 0.3:
                    grid_maze[i][j] = WALL
                else:
                    grid_maze[i][j] = HOLLOW

    # Colocar posición inicial
    grid_maze[starty][startx] = HOLLOW

    # Colocar objetivos
    for g in goals:
        grid_maze[g[1]][g[0]] = HOLLOW

    # Configurar el laberinto (paredes móviles y pesos)

    # 3. Configuración del dinamismo y los pesos
    config_maze(grid_maze) 
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
        
        if posibilities:
            move = random.choice(posibilities)
            swap = maze[dinamic_wall[0]][dinamic_wall[1]]
            maze[dinamic_wall[0]][dinamic_wall[1]] = maze[move[0]][move[1]]
            maze[move[0]][move[1]] = swap
            print("Se ha movido una pared de:", dinamic_wall, "a", move)
            #print(maze)

def get_neighbors(node, maze):
    neighbors = []
    x = node[0]
    y = node[1]

    if maze[x+1][y] > 0: #and (x+1,y) not in queue and (x+1,y) not in visited:
        neighbors.append((x+1,y))
    if maze[x][y+1] > 0: #and (x,y+1) not in queue and (x,y+1) not in visited:
        neighbors.append((x,y+1))
    if maze[x-1][y] > 0: #and (x-1,y) not in queue and (x-1,y) not in visited:
        neighbors.append((x-1,y))
    if maze[x][y-1] > 0: #and (x,y-1) not in queue and (x,y-1) not in visited:
        neighbors.append((x,y-1))
        
    return neighbors
