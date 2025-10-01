import random
import numpy as np
import math as math

# Declaracion de constantes
WALL_M = -2
WALL = -1
HOLLOW = 0

class Maze:
    def __init__(self, n, prob_wall, prob_move, seed):
    # Verificaciones
        assert n % 2 == 1 and n >= 3

        self.width = n  # Ancho del laberinto
        self.height = n  # Alto del laberinto

        # Semilla predefinida
        if seed is not None:
            random.seed(seed)

        # Declaracion de constantes
        WALL_M = -2
        WALL = -1
        HOLLOW = 0

        # Dleclaracion de variables
        self.mov_wall = [] # Lista de posiciones de las paredes moviles
        self.prob_wall = prob_wall # Probabilidad de que una pared sea una pared movil
        self.prob_move = prob_move # Probabilidad de que una pared movil se mueva en cada iteracion
        self.goals = [(1,1), (self.height-2, 1), (1, self.width-2), (self.width-2, self.height-2)] # Posiciones finales posibles, estan predefinidas como las esquinas, aunque despues se podria probar colocandolas aleatoriamente
        self.true_goal = random.choice(self.goals)

        # Declaracion de variables globales
        self.grid_maze = np.ones((self.height, self.width), dtype=int) * -1 # El laberinto al inicio esta completamente hecho de paredes
        startx = random.randrange(1, self.width,2)
        starty = random.randrange(1, self.height,2)
        self.pos_inicial = (starty, startx) # Posicion inicial
        self.hasVisited = [(starty, startx)] # Lista de posiciones visitadas

        # Generar el laberinto
        self._maze_generator()
        # Configuración del dinamismo y los pesos
        self._config_maze()


    def _config_maze(self):

        '''
        Funcion para la configuracion del laberinto, se encarga de recorrer la matriz y
        asignar las paredes moviles y los pesos a los nodos de forma aleatoria
        '''

        # Recorrido de la matriz
        for i in range(self.height):
            for j in range(self.width):
                
                # Asignacion de las paredes moviles del laberinto
                if self.grid_maze[i][j] == WALL:
                    if i > 0 and i < self.height-1 and j > 0 and j < self.width-1 and random.uniform(0,1) < self.prob_wall: # Identificacion de pared interna
                            self.mov_wall.append((i,j)) 
                            self.grid_maze[i][j] = WALL_M

                elif self.grid_maze[i][j] == HOLLOW:
                    dist_min = min(abs(i - g[0]) + abs(j - g[1]) for g in self.goals)
                    self.grid_maze[i][j] = 1 + int(0.3 * dist_min)  # Asignacion de un peso basado en la distancia a la meta mas cercana


    def _maze_generator(self):

        '''
        Funcion principal para la generacion del laberinto
        '''
        '''
        Genera un campo abierto con obstáculos aleatorios de baja densidad.
        Es la forma más simple de garantizar (con alta probabilidad) la transibilidad.
        '''
        

        for i in range(self.height):
            for j in range(self.width):
                # Bordes siempre paredes
                if i == 0 or i == self.height-1 or j == 0 or j == self.width-1:
                    self.grid_maze[i][j] = WALL
                else:
                    if random.random() < 0.3:
                        self.grid_maze[i][j] = WALL
                    else:
                        self.grid_maze[i][j] = HOLLOW

        # Colocar posición inicial
        self.grid_maze[self.pos_inicial] = HOLLOW

        # Colocar objetivos
        for g in self.goals:
            self.grid_maze[g[1]][g[0]] = HOLLOW

        # 3. Configuración del dinamismo y los pesos
         
        return self.grid_maze

    def update_maze(self):
        
        if not self.mov_wall:
            return
        if random.uniform(0,1) < self.prob_move:

            dinamic_wall = random.choice(self.mov_wall)
            self.mov_wall.remove(dinamic_wall)
            posibilities = []

            if self.grid_maze[dinamic_wall[0]+1][dinamic_wall[1]] >= 0:
                posibilities.append((dinamic_wall[0]+1, dinamic_wall[1]))
            if self.grid_maze[dinamic_wall[0]-1][dinamic_wall[1]] >= 0:
                posibilities.append((dinamic_wall[0]-1, dinamic_wall[1]))
            if self.grid_maze[dinamic_wall[0]][dinamic_wall[1]+1] >= 0:
                posibilities.append((dinamic_wall[0], dinamic_wall[1]+1))
            if self.grid_maze[dinamic_wall[0]][dinamic_wall[1]-1] >= 0:
                posibilities.append((dinamic_wall[0], dinamic_wall[1]-1))
            
            if self.pos_inicial in posibilities:
                posibilities.remove(self.pos_inicial)
            
            for goal in self.goals:
                if goal in posibilities:
                    posibilities.remove(goal)

            if posibilities:
                move = random.choice(posibilities)
                swap = self.grid_maze[dinamic_wall[0]][dinamic_wall[1]]
                self.grid_maze[dinamic_wall[0]][dinamic_wall[1]] = self.grid_maze[move[0]][move[1]]
                self.grid_maze[move[0]][move[1]] = swap
                self.mov_wall.append(move)

    def get_neighbors(self, node):
        neighbors = []
        x = node[0]
        y = node[1]

        if self.grid_maze[x+1][y] > 0: 
            neighbors.append((x+1,y))
        if self.grid_maze[x][y+1] > 0: 
            neighbors.append((x,y+1))
        if self.grid_maze[x-1][y] > 0:
            neighbors.append((x-1,y))
        if self.grid_maze[x][y-1] > 0: 
            neighbors.append((x,y-1))
            
        return neighbors
