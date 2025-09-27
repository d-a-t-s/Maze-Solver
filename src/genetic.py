from maze_generator import *

# Declaracion de alelos para la construccion posterior de los cromosomas
UP = "00"
DOWN = "01"
LEFT = "10"
RIGHT = "11"

# Conjunto de movimientos a realizar
MOVES = [UP, DOWN, LEFT, RIGHT]

# Largo de cada cromosoma/individuo, corresponde al numero de ACCIONES que podrá realizar cada individuo
cromosoma_lenght = ((WIDTH - 2) * (HEIGHT - 2))//2

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

    # cromosoma_lenght = 5
    gen_size = 50 #Tamaño de la generacion

    new_gen = [] # Lista donde se almacenarán los nuevos individuos luego del crossover y la mutacion
    old_gen = [] # Lista donde se almacenarán los individuos que se pondrán a prueba en el laberinto

    pos = start                         # Posicion inicial en donde se comienza el recorrido en el laberinto
    true_goal = random.choice(goals)    # Seleccion de una salida verdadera al azar
    score = []                          # Lista donde se almacenarán los valores dados por la FITNESS FUNCTION para cada individuo
    # top_10 = []                         # Lista donde se almacenarán los 10 mejores individuos de cada generacion (ELITISM)
    n_gen = 0                           # Contador de generaciones
    gen_limit = 10                       # Limite de numero de generaciones
    elitism_list = []                   # Lista donde se almacenarán los 10 mejores individuos de cada generacion (ELITISM)
    # elite_num = 10                      # Cantidad de individuos que se elegiran como elite de su generacion
    new_elite = []

    # print("Posicion inicial:", pos, maze[pos])
    # print("Metas posibles:", goals)
    # print("Meta verdadera:", true_goal)

    #Creacion de la Generacion 0 (Primera generacion), se crea de forma aleatoria
    for i in range(gen_size):
        s = ""
        for j in range(cromosoma_lenght):
            s = s + random.choice(MOVES)
        old_gen.append(s)

    # Calculo y almacenamiento del valor de la fitness function para cada individuo
    for individual in old_gen:
        result = fitness_function(pos, individual, true_goal, maze)

        # Descomentar para que el algoritmo termine una vez encontrada la solucion
        # if result == 1.0:
        #     return print("Individuo:", individual, "Encontró la salida del laberinto")

        if result >= 0.9:
            elitism_list.append(individual)

        #Eliminar despues
        score.append(result)
    
    print("Numero de soluciones encontradas en la gen:", n_gen, score.count(1.0))

    #BUCLE PRINCIPAL
    while(n_gen < gen_limit):

        # Guardamos en una lista los mejores individuos de su generacion
        # elitism_list = heapq.nlargest(elite_num,score)
        score.clear()


        # print("Top 10 mejores individuos de la gen:", elitism_list)
        print("NUMERO DE INDIVIDUOS:", len(old_gen))
        print("NUMERO DE ELITES:", len(elitism_list))

        # Generacion de la nueva generacion + mutacion de los individuos, modificar luego para elegir solo el child con el mejor valor fitness
        for i in range(gen_size - len(elitism_list)):
            child1,child2 = single_point_crossover(random.choice(old_gen), random.choice(old_gen))
            
            # Se eleige como nuevo individuo aquel cuyo valor dado por la FITNESS FUNCTION sea mayor
            result1 = fitness_function(pos, child1, true_goal, maze)
            result2 = fitness_function(pos, child2, true_goal, maze)
            
            # Dado que se está utilizando la FITNESS FUNCTION, podemos saber inmediatamente si ya se ha encontrado una solucion, por lo tanto:
            if result1 == 1.0:
                # return print("Individuo:", child1, "Encontró la salida del laberinto")

                # Borrar despues
                score.append(1.0)
                new_gen.append(child1)
                continue
            if result2 == 1.0:
                # return print("Individuo:", child2, "Encontró la salida del laberinto")
                
                # Borrar despues
                score.append(1.0)
                new_gen.append(child2)
                continue
            
            # Si uno de los individuos anteriores no era una solucion entonces les aplicamos una mutacion
            child1 = mutation(child1)
            child2 = mutation(child2)

            # Calculamos su nuevo valor para la FITNESS FUNCTION
            result1 = fitness_function(pos, child1, true_goal, maze)
            result2 = fitness_function(pos, child2, true_goal, maze)

            # Y nuevamente elegimos aquel individuo cuyo valor sea mayor y verificamos si puede pertencer al conjunto de elite
            if result1 > result2:
                new_individual = child1

                if result1 >= 0.9:
                    new_elite.append(new_individual)
            else:
                new_individual = child2
                if result2 >= 0.9:
                    new_elite.append(new_individual)

            # Una vez obtenido al de mayor valor podemos lo agregamos a la nueva generacion
            new_gen.append(new_individual)

        # print(old_gen)
        # print(old_gen == new_gen)
        # print(old_gen)
        # print(new_gen)

        old_gen.clear()                 # Borramos la generacion vieja
        old_gen.extend(new_gen)         # Almacenamos en su lugar la generacion nueva
        old_gen.extend(elitism_list)    # junto con los individuos de elite

        new_gen.clear()                 #  Borramos la generacion actual para almacenar la proxima generacion en la siguiente iteracion
        elitism_list.clear()            # Borramos los individuos de elite de la generacion vieja
        elitism_list.extend(new_elite)  # En su lugar almacenamos al grupo de elite de la generacion actual
        new_elite.clear()               # Borramos los elites de la generacion actual para almacenar los de la proxima generacion

        # print(old_gen)

        # Aumento del numero de la generacion
        print("PASO DE GENERACION, DE GENERACION:", n_gen, "A", n_gen+1)
        n_gen = n_gen + 1
        # print(score)
        print("Cantidad de soluciones correctas:", score.count(1.0))
        # print("Valores maximos:")

def fitness_function(posicion, individual, true_goal, maze):

    '''
    FITNESS FUNCTION para calcular el valor de un individuo en especifico, se basa en lo siguiente:

    1. Si el individuo es una solucion correcta el valor maximo corresponde a 1.0
    2. Si el individuo es una solucion incorrecta (salida falsa) su valor corresponderá a la distancia de Manhattan
    a la que quedo de la salida verdadera, con una penalizacion del 25%
    3. Si el individuo no es una solucion, su valor corresponderá al distancia de Manhattan a la que el individuo
    quedó de la salida
    '''

    # print("LABERINTO EN SU ESTADO INICIAL:")
    # print(maze)
    for i in range(len(individual)//2):
        
        update_maze(maze) #Se da la posibilidad de que una pared se mueva
        # Verificacion de termino
        if posicion in goals:
            if posicion == true_goal:
                # print("Se ha encontrado una salida en:", true_goal, maze[true_goal])
                maze = aux_maze # Devolvemos el laberinto a su estado inicial para que el siguiente individuo lo pueda probar
                return 1.0
            
            else:
                # Penalizacion extra por caer en una salida falsa
                # print("Se ha encontrado una salida falsa en:", posicion, maze[posicion])
                maze = aux_maze # Devolvemos el laberinto a su estado inicial para que el siguiente individuo lo pueda probar
                return 0.75 * (1 - (abs(posicion[0] - true_goal[0]) + abs(posicion[1] - true_goal[1]))/100)

        action = individual[len(individual) - 2 - i*2] + individual[len(individual) - 1 - i*2]
        # print(action, end="")

        if action == UP:
            # print(" UP")
            if maze[posicion[0]-1][posicion[1]] >= 0:
                posicion = (posicion[0]-1,posicion[1])

        elif action == DOWN:
            # print(" DOWN")
            if maze[posicion[0]+1][posicion[1]] >= 0:
                posicion = (posicion[0]+1,posicion[1])
        elif action == LEFT:
            # print(" LEFT")
            if maze[posicion[0]][posicion[1]-1] >= 0:
                posicion = (posicion[0],posicion[1]-1)

        elif action == RIGHT:
            # print(" RIGHT")
            if maze[posicion[0]][posicion[1]+1] >= 0:
                posicion = (posicion[0],posicion[1]+1)

    # print("No se ha encontrado una solucion, posicion final:", posicion)
    maze = aux_maze # Devolvemos el laberinto a su estado inicial para que el siguiente individuo lo pueda probar
    return 1 - (abs(posicion[0] - true_goal[0]) + abs(posicion[1] - true_goal[1]))/100

def single_point_crossover(individual1, individual2):

    '''
    Cada individuo corresponde a una cadena de movimientos donde cada movimiento corresponde a dos bits, considerando
    que cada cadeba posee ((WIDTH - 2) * (HEIGHT - 2))//2 movimientos se tiene
    '''

    child1 = individual1[0: cromosoma_lenght*2 - 10] + individual2[cromosoma_lenght*2 - 10: cromosoma_lenght*2]

    child2 = individual2[0: cromosoma_lenght*2 - 10] + individual1[cromosoma_lenght*2 - 10: cromosoma_lenght*2]

    return child1,child2

def mutation(individual):
    individual = list(individual)
    individual[random.randrange(0,cromosoma_lenght*2)] = str(random.randrange(0,2))
    return "".join(individual)


def dec_to_bin(bin):
    dec = 0
    for i in range(len(bin)):
        dec = dec + int(bin[len(bin) - i - 1]) * 2**i
    return dec

# Mini main
maze = maze_generator()
aux_maze = maze

gen_solver(pos_incial, goals, maze)

# print(mutation("0123456789"))
# print(maze)
