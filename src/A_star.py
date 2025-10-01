import heapq
from maze_generator import *

def A_star(pos_inicial, goals, maze):
    """
    Algoritmo A* para la busqueda de la salida del laberinto:
    1. Se calcula la heuristica de cada nodo como la distancia de manhattan a la salida mas
    cercana a medida que se avanza en el laberinto
    2. El algoritmo fija la salida que tenga mas cerca y recorre el laberinto para encontrarla
    """

    # Inicialización
    queue = []  # cola de prioridad
    heapq.heappush(queue, (0, maze.pos_inicial))
    came_from = {}
    g_score = {maze.pos_inicial: 0}
    visited = set()

    while queue:

        # Obtener el nodo con el menor f y quitarlo de la cola
        _, pos = heapq.heappop(queue)


        # Damos la posibilidad de que las paredes se muevan
        maze.update_maze()

        #Visualizacion del proceso
        #yield maze.grid_maze, pos

        # Verificación de nodos visitados
        if pos in visited:
            continue
        
        # Agregar nodo a visitados
        visited.add(pos)

        # Verificación de término
        if pos == maze.true_goal:
            camino = rebuild_path(came_from, pos)
            if blocked_path(camino, maze):
                
                print("Camino bloqueado, replanning...")

                # Se reinician las estructuras de datos para replanificar
                queue.clear()
                heapq.heappush(queue, (0, pos_inicial))
                came_from.clear()
                g_score = {pos_inicial: 0}
                visited.clear()
                
                continue
            #else:
                #for nodo in camino:
                    #maze[nodo] = 0
                    #yield maze, nodo
            
            return camino
        
        # Caso en que se llega a una meta falsa
        if pos in maze.goals and pos != maze.true_goal:
            maze.goals.remove(pos)

        # Expandimos vecinos
        vecinos = maze.get_neighbors(pos)
        for vecino in vecinos:
            # Cálculo de g y f de cada vecino
            
            g_temp = g_score[pos] + maze.grid_maze[vecino]
            # Actualizar g_score y came_from si es un mejor camino
            if vecino not in g_score or g_temp < g_score[vecino]:
                g_score[vecino] = g_temp
                f = g_temp + heuristic(vecino, maze.goals, maze.true_goal)
                # Si el vecino no está en la cola, lo añadimos
                heapq.heappush(queue, (f, vecino))
                # Actualizamo el diccionario para guardar el camino
                came_from[vecino] = pos

    # No se encontró solución
    return None


def heuristic(pos, goals, true_goal):
    """
    Heurística de Manhattan hacia la meta más cercana.
    """
    if not goals:
        return abs(pos[0] - true_goal[0]) + abs(pos[1] - true_goal[1])
    return min(abs(pos[0] - g[0]) + abs(pos[1] - g[1]) for g in goals)


def rebuild_path(came_from, pos):
    """
    Reconstrucción del camino desde el inicio hasta la posición actual.
    """
    camino = [pos]
    while pos in came_from:
        pos = came_from[pos]
        camino.append(pos)
    camino.reverse()
    return camino

def blocked_path(camino, maze):
    """
    Verifica si el camino está bloqueado por paredes móviles.
    """
    for nodo in camino:
        if maze.grid_maze[nodo] == -2:  # Si es una pared móvil
            return True
    return False
