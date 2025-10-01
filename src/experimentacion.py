import time
import copy
import numpy as np
import pandas as pd
from maze_generator import *
from A_star import *
from genetic import *

def run_solver(solver_func, start_pos, goals, maze):
    
    start_time = time.time()
    
    if solver_func == "A_star":
        
        result = A_star(start_pos, goals, maze)
        
        if result is not None:
            path_length = len(result)
            success = True
        else:
            path_length = 0
            success = False
            
    elif solver_func == "gen_solver":

        cromosoma, success = gen_solver(start_pos, goals, maze)
        if success == 1:
            path_length = len(cromosoma)
            success = True
        else:
            path_length = 0
            success = False
    
    end_time = time.time()
    
    return {
        'time': end_time - start_time,
        'path_length': path_length,
        'success': success,
    }

N_REPETITIONS = 20 # Número de veces que se ejecuta cada prueba (para estadísticas)

results_scalability = []
results_dynamism = []

# Testeo 1: Escalabilidad (Tamaño del Laberinto)

n_sizes = [11, 21, 31, 41]

for n in n_sizes:
        
        print(f"\nTesteando tamaño N={n}x{n}...")
        
        for i in range(N_REPETITIONS):
            # Inicializar y generar laberinto
            maze = Maze(n, 0.05, 0.05, seed=i)

            # 1. Ejecutar A*
            result_a_star = run_solver("A_star", maze.pos_inicial, maze.goals , copy.deepcopy(maze)) # Usar copy para que AG vea el mismo estado inicial
            results_scalability.append({
                'Test': 'Escalabilidad', 'N': n, 'Dinamismo': maze.prob_move,
                'Algoritmo': 'A*', 'Tiempo': result_a_star['time'],
                'Longitud': result_a_star['path_length'], 'Éxito': result_a_star['success']
            })

            # 2. Ejecutar AG
            result_ag = run_solver("gen_solver", maze.pos_inicial, maze.goals, copy.deepcopy(maze))
            results_scalability.append({
                'Test': 'Escalabilidad', 'N': n, 'Dinamismo': maze.prob_move,
                'Algoritmo': 'AG', 'Tiempo': result_ag['time'],
                'Longitud': result_ag['path_length'], 'Éxito': result_ag['success']
            })


# Crear el DataFrame
df_results_s = pd.DataFrame(results_scalability)

df_results_s.to_csv("resultados_laberinto_s.csv", index=False)


# Testeo 2: Robustez (Nivel de Dinamismo)

dynamism = [(0.1,0.1), (0.25, 0.25), (0.35,0.35)]

for prob_wall, prob_move in dynamism :
    print(f"\nTesteando Dinamismo: Paredes={prob_wall}, Movimiento={prob_move}...")
        
    for i in range(N_REPETITIONS):
        # Inicializar y generar laberinto
        maze = Maze(21, prob_wall, prob_move, seed=i)

        # 1. Ejecutar A*
        result_a_star = run_solver("A_star", maze.pos_inicial, maze.goals , copy.deepcopy(maze)) # Usar copy para que AG vea el mismo estado inicial
        results_dynamism.append({
                'Test': 'Escalabilidad', 'N': 21, 'Dinamismo': maze.prob_move,
                'Algoritmo': 'A*', 'Tiempo': result_a_star['time'],
                'Longitud': result_a_star['path_length'], 'Éxito': result_a_star['success']
            })

            # 2. Ejecutar AG
        result_ag = run_solver("gen_solver", maze.pos_inicial, maze.goals, copy.deepcopy(maze))
        results_dynamism.append({
                'Test': 'Escalabilidad', 'N': 21, 'Dinamismo': maze.prob_move,
                'Algoritmo': 'AG', 'Tiempo': result_ag['time'],
                'Longitud': result_ag['path_length'], 'Éxito': result_ag['success']
            })

# Crear el DataFrame
df_results_d = pd.DataFrame(results_dynamism)

df_results_d.to_csv("resultados_laberinto_d.csv", index=False)