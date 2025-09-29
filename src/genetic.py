from maze_generator1 import *
import copy

# Declaracion de alelos para la construccion posterior de los cromosomas
UP = "00"
DOWN = "01"
LEFT = "10"
RIGHT = "11"

# Conjunto de movimientos a realizar
MOVES = [UP, DOWN, LEFT, RIGHT]

# Largo de cada cromosoma/individuo, corresponde al numero de ACCIONES que podrá realizar cada individuo
cromosoma_lenght = ((WIDTH) * (HEIGHT))//2

def execute_action(position, action, maze):
    """Ejecuta una acción (movimiento) si es válida en el laberinto actual."""
    row, col = position
    
    if action == UP and maze[row - 1][col] >= 0:
        return (row - 1, col)
    elif action == DOWN and maze[row + 1][col] >= 0:
        return (row + 1, col)
    elif action == LEFT and maze[row][col - 1] >= 0:
        return (row, col - 1)
    elif action == RIGHT and maze[row][col + 1] >= 0:
        return (row, col + 1)
    
    # Si el movimiento no es válido (choca con una pared), se queda en el mismo lugar.
    return position

def fitness_function(posicion, individual, true_goal, maze):

    '''
    FITNESS FUNCTION para calcular el valor de un individuo en especifico, se basa en lo siguiente:

    1. Si el individuo es una solucion correcta el valor maximo corresponde a 1.0
    2. Si el individuo es una solucion incorrecta (salida falsa) su valor corresponderá a la distancia de Manhattan
    a la que quedo de la salida verdadera, con una penalizacion del 25%
    3. Si el individuo no es una solucion, su valor corresponderá al distancia de Manhattan a la que el individuo
    quedó de la salida
    '''
    maze_copy = copy.deepcopy(maze)
    current_pos = posicion
    max_dist = WIDTH + HEIGHT # Factor de normalización
    
    for i in range(0, len(individual), 2):
        
        action = individual[i:i+2]
        current_pos = execute_action(current_pos, action, maze_copy)

        update_maze(maze_copy) #Se da la posibilidad de que una pared se mueva
        
        # Verificacion de termino
        if current_pos in goals:
            if current_pos == true_goal:
                return 1.0
            
            else:
                # Penalizacion extra por caer en una salida falsa
                dist = (abs(current_pos[0] - true_goal[0]) + abs(current_pos[1] - true_goal[1]))
                return 0.75 * (1 - dist/max_dist)
    
    dist = (abs(posicion[0] - true_goal[0]) + abs(posicion[1] - true_goal[1]))
    return 1 - (dist/max_dist)

def tournament_selection(population, results):
    """
    Se eligen 3 individuos al azar y el de mejor fitness gana.
    """
    # Se seleccionan 3 contendientes al azar de la población
    tournament_contenders = random.sample(list(zip(population, results)), 3)
    
    # El ganador es el contendiente con el mayor fitness
    winner = max(tournament_contenders, key=lambda item: item[1])

    return winner[0]  # Se devuelve solo el cromosoma del ganador

def single_point_crossover(parent1, parent2):
    """
    Realiza un cruce de un solo punto en un lugar aleatorio.
    """
    assert len(parent1) == len(parent2)
    
    # Se elige un punto de cruce aleatorio a lo largo del cromosoma
    crossover_point = random.randint(1, len(parent1) - 1)
    
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    
    return child1, child2

def mutation(individual, mutation_rate=0.05):
    """
    Muta un individuo basado en una tasa de mutación por bit.
    Cada bit tiene una pequeña probabilidad de ser invertido.
    """
    mutated_individual = list(individual)
    for i in range(len(mutated_individual)):
        if random.random() < mutation_rate:
            # Invierte el bit (0 -> 1 o 1 -> 0)
            mutated_individual[i] = "1" if mutated_individual[i] == "0" else "0"
            
    return "".join(mutated_individual)

def gen_solver(start, goals, maze):

    '''
    Algoritmo genetico para encontrar una solucion a un laberinto dado y consta de las siguientes fases:
    
    1. Creacion de una generacion de individuos los cuales serán posibles soluciones para el laberinto
    2. Dados los individuos anteriores se obtiene el valor en base a la FITNESS FUNCTION conociendo asi
    el rendimiento de cada individuo
    3. Creacion de una nueva generacion mediante SINGLE POINT CROSSOVER eligiendo el individuo resultante
    que posea el mejor valor dado por la fitness function, ademas se aplica ELITISM dejando los ultimos 10
    mejores individuos reservados para la siguiente generacion
    4. Mutacion de los individuos de la nueva generacion
    5. Testeo de la nueva generacion como soluciones del laberinto

    Este proceso se repetirá hasta encontrar una solucion o hasta alcanzar un numero maximo de generaciones
    '''
    gen_size = 100 # Tamaño de la generacion
    gen_limit = 50 # Limite de numero de generaciones

    true_goal = random.choice(goals)    # Seleccion de una salida verdadera al azar
    n_gen = 0                           # Contador de generaciones
    

    #Creacion de la Generacion 0 (Primera generacion), se crea de forma aleatoria
    
    population = [] # Lista donde se almacenarán los individuos que se pondrán a prueba en el laberinto
    for _ in range(gen_size):
        individual = "".join(random.choice(MOVES) for _ in range(cromosoma_lenght))
        population.append(individual)

    #BUCLE PRINCIPAL
    while(n_gen < gen_limit):

        # Calculo y almacenamiento del valor de la fitness function para cada individuo
        results = [] # Lista donde se almacenan los valores de la fitness function
        for individual in population:
            result = fitness_function(start, individual, true_goal, maze)
            if result == 1.0:
                return 1
            results.append(result)
        
        elites = sorted(zip(population, results), key=lambda x: x[1], reverse=True)[:10] # Seleccion de los 10 mejores individuos

        new_gen = [individual for individual, _ in elites] # Lista donde se almacenarán los nuevos individuos luego del crossover y la mutacion


        # Generacion de la nueva generacion + mutacion de los individuos
        while len(new_gen) < gen_size:
            
            parent1 = tournament_selection(population, results)
            parent2 = tournament_selection(population, results)

            child1,child2 = single_point_crossover(parent1, parent2)
            
            # Mutación
            child1 = mutation(child1)
            child2 = mutation(child2)

            # Evaluación de los hijos para seleccionar el mejor
            fit1 = fitness_function(start, child1, true_goal, maze)
            fit2 = fitness_function(start, child2, true_goal, maze)

            # Una vez obtenido al de mayor valor podemos lo agregamos a la nueva generacion
            new_gen.append(child1 if fit1 > fit2 else child2)
        
        population = new_gen # La nueva generacion pasa a ser la generacion actual

        # Aumento del numero de la generacion
        n_gen = n_gen + 1
    
    return 0