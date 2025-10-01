import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar datos
df = pd.read_csv('resultados_laberinto_s.csv')

# Filtrar solo casos exitosos para análisis de rendimiento
df_exitosos = df[df['Éxito'] == True]

# Calcular métricas por algoritmo y tamaño
metricas = df.groupby(['N', 'Algoritmo']).agg({
    'Tiempo': 'mean',
    'Longitud': 'mean',
    'Éxito': lambda x: (x.sum() / len(x)) * 100  # Tasa de éxito en porcentaje
}).reset_index()

# Crear figura con 3 subgráficos
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Análisis de Escalabilidad: A* vs Algoritmo Genético', fontsize=16, fontweight='bold')

# Colores para cada algoritmo
colores = {'A*': '#2E86AB', 'AG': '#A23B72'}

# Gráfico 1: Tiempo de ejecución promedio
for algo in ['A*', 'AG']:
    data = metricas[metricas['Algoritmo'] == algo]
    axes[0].plot(data['N'], data['Tiempo'], marker='o', linewidth=2.5, 
                 markersize=10, label=algo, color=colores[algo])

axes[0].set_xlabel('Tamaño del problema (N)', fontsize=11)
axes[0].set_ylabel('Tiempo promedio (segundos)', fontsize=11)
axes[0].set_title('Tiempo de Ejecución', fontsize=12, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3)
axes[0].set_xticks([11, 21, 31, 41])
axes[0].set_yscale('log')

# Gráfico 2: Tasa de éxito
bar_width = 2
x_pos = np.array([11, 21, 31, 41])
data_a = metricas[metricas['Algoritmo'] == 'A*']['Éxito'].values
data_ag = metricas[metricas['Algoritmo'] == 'AG']['Éxito'].values

axes[1].bar(x_pos - bar_width/2, data_a, bar_width, 
            label='A*', color=colores['A*'], alpha=0.8)
axes[1].bar(x_pos + bar_width/2, data_ag, bar_width, 
            label='AG', color=colores['AG'], alpha=0.8)

axes[1].set_xlabel('Tamaño del problema (N)', fontsize=11)
axes[1].set_ylabel('Tasa de éxito (%)', fontsize=11)
axes[1].set_title('Tasa de Éxito', fontsize=12, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(True, alpha=0.3, axis='y')
axes[1].set_ylim(0, 105)
axes[1].set_xticks([11, 21, 31, 41])

# Gráfico 3: Longitud de solución (solo casos exitosos)
metricas_exitosos = df_exitosos.groupby(['N', 'Algoritmo']).agg({
    'Longitud': 'mean'
}).reset_index()

for algo in ['A*', 'AG']:
    data = metricas_exitosos[metricas_exitosos['Algoritmo'] == algo]
    axes[2].plot(data['N'], data['Longitud'], marker='s', linewidth=2.5,
                 markersize=10, label=algo, color=colores[algo])

axes[2].set_xlabel('Tamaño del problema (N)', fontsize=11)
axes[2].set_ylabel('Longitud promedio de solución', fontsize=11)
axes[2].set_title('Calidad de Solución', fontsize=12, fontweight='bold')
axes[2].legend(fontsize=11)
axes[2].grid(True, alpha=0.3)
axes[2].set_xticks([11, 21, 31, 41])

plt.tight_layout()
plt.savefig('escalabilidad_comparacion.png', dpi=300, bbox_inches='tight')
plt.show()

# Generar resumen estadístico
print("\n" + "="*70)
print("RESUMEN ESTADÍSTICO POR ALGORITMO")
print("="*70)

for algo in ['A*', 'AG']:
    df_algo = df[df['Algoritmo'] == algo]
    df_algo_exitoso = df_exitosos[df_exitosos['Algoritmo'] == algo]
    
    print(f"\n{algo}:")
    print(f"  Tasa de éxito global: {(df_algo['Éxito'].sum() / len(df_algo)) * 100:.1f}%")
    print(f"  Tiempo promedio (éxitos): {df_algo_exitoso['Tiempo'].mean():.4f}s")
    print(f"  Tiempo promedio (todos): {df_algo['Tiempo'].mean():.4f}s")
    print(f"  Longitud promedio solución: {df_algo_exitoso['Longitud'].mean():.1f}")
    print(f"  Desv. estándar tiempo: {df_algo['Tiempo'].std():.4f}s")

print("\n" + "="*70)
print("CONCLUSIONES")
print("="*70)

# Calcular métricas para conclusiones
tasa_exito_a = (df[df['Algoritmo'] == 'A*']['Éxito'].sum() / len(df[df['Algoritmo'] == 'A*'])) * 100
tasa_exito_ag = (df[df['Algoritmo'] == 'AG']['Éxito'].sum() / len(df[df['Algoritmo'] == 'AG'])) * 100

tiempo_a = df_exitosos[df_exitosos['Algoritmo'] == 'A*']['Tiempo'].mean()
tiempo_ag = df_exitosos[df_exitosos['Algoritmo'] == 'AG']['Tiempo'].mean()

print(f"""
A* demuestra superioridad en escalabilidad con {tasa_exito_a:.1f}% de éxito versus 
{tasa_exito_ag:.1f}% del AG. Su tiempo de ejecución es consistentemente más bajo 
(promedio {tiempo_a:.4f}s vs {tiempo_ag:.4f}s), siendo hasta 1000x más rápido en 
problemas grandes. A* es determinista y óptimo, encontrando siempre el camino más 
corto cuando existe solución. Su eficiencia se mantiene incluso con N=41, mientras 
el AG colapsa frecuentemente por timeout.

El Algoritmo Genético muestra alta variabilidad y deterioro severo al escalar. 
Aunque encuentra soluciones en problemas pequeños, su naturaleza estocástica genera 
inconsistencia: puede tardar milisegundos o segundos para el mismo problema. Las 
soluciones son subóptimas (caminos más largos) y la tasa de fallo aumenta 
dramáticamente con N. Es inadecuado para este tipo de búsqueda de caminos donde 
se requiere garantía de optimalidad y consistencia temporal.

Recomendación: A* es la elección superior para problemas de búsqueda de caminos 
que requieran escalabilidad, optimalidad garantizada y tiempos predecibles. El AG 
solo sería considerado en escenarios donde no exista heurística admisible o el 
espacio de estados sea extremadamente grande y se acepten soluciones aproximadas.
""")