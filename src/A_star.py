import random
import math
from maze_generator import *

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (15,67,15)

# cell = 20

def A_star(start, goals, maze):

    '''
    Algoritmo A* para la busqueda de la salida del laberinto:
    1. En cada ejecucion de elige  una salida al azar entre las posibles como salida verdadera
    2. Se calcula la heuristica de cada nodo como la distancia de manhattan a la salida mas
    cercana a medida que se avanza en el laberinto
    3. El algoritmo fija la salida que tenga mas cerca y recorre el laberinto para encontrarla
    '''
    visited = [start] # Lista de nodos visitados
    queue = [] # Lista de nodos en cola (por visitar)
    path = [] # Camino seguido hasta la salida
    pos = start # Posicion actual
    obj_g = 0

    # Verificacion de termino por si el punto de inicio coincide con una meta
    if pos in goals:
        if pos == true_goal: # Si es la meta verdadera se termina la ejecucion
            print("Se ha encontrado una solucion en:", pos)
            maze[pos] = -4
            return maze
        else:
            goals.remove(pos) # Si es una meta falsa se elimina del conjunto de metas

    # Encontramos la salida mas cercana
    min = math.inf
    for goal in goals:
        dist = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        if dist < min:
            min = dist
            obj_g = goal

    # Obtencion de vecinos
    neighbors = get_neighbors(pos, maze, queue, visited)

    # Adicion de vecinos a los nodos no visitados
    queue = queue + neighbors

    print("Posicion inicial:", pos, maze[pos])
    print("Posibles metas:", goals)
    print("Meta verdadera:", true_goal, maze[true_goal])
    print("Meta objetivo:", obj_g)
    print("Paredes moviles:", mov_wall)

    while queue:

        # Dada la salida mas cercana, la fijamos como objetivo para ahora calcular la heuristica
        f = math.inf
        for in_queue in queue:
            h = abs(in_queue[0] - obj_g[0]) + abs(in_queue[1] - obj_g[1])
            g = maze[in_queue]
            if h + g < f:
                f = h + g
                # Actualizamos la posicion actual a la que tenga el valor mas bajo
                pos = in_queue
        
        #Una vez obtenido el siguiente nodo, se hace lo siguiente:
        visited.append(pos)     # Lo marcamos como visitado
        queue.remove(pos)       # Lo sacamos de la cola
        update_maze(maze)       # Se da la posibilidad de que una pared se mueva
        print(pos, maze[pos])
        maze[pos] = 0
        
        # Verificacion de termino
        if pos in goals:
            # Si estamos en la meta verdadera se acaba la ejecucion del algoritmo
            if pos == true_goal:
                print("Se ha encontrado una solucion en:", pos)
                maze[pos] = -4
                return maze
            # Si estamos en una meta falsa pero esta era nuestra meta objetivo, fijamos la proxima meta mas cercana
            elif pos == obj_g:
                print("Se ha encontrado una salida falsa en", pos, maze[pos])
                maze[pos] = -3
                # Encontramos la salida mas cercana
                goals.remove(obj_g)
                min = math.inf
                for goal in goals:
                    dist = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
                    if dist < min:
                        min = dist
                        obj_g = goal
            # Si era una meta falsa pero no era la meta objetivo, simplemente la eliminamos del conjunto de metas
            else:
                goals.remove(pos)
                maze[pos] = -3
            print("metas restantes:", goals)
            print("Nueva meta obejtivo:", obj_g)

        # Obtencion de vecinos
        neighbors = get_neighbors(pos, maze, queue, visited)

        # Adicion de vecinos a los nodos no visitados
        queue = queue + neighbors
    
    print("No se ha encontrado una solucion, posicion final:", pos)
    return maze



# Mini main
# maze = maze_generator()

# print(maze)
# print()
# A_star(pos_incial, goals, maze)
# print()
# print(maze)
