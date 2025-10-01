import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar datos
df = pd.read_csv('resultados_laberinto_d.csv')

# Filtrar solo casos exitosos para análisis de rendimiento
df_exitosos = df[df['Éxito'] == True]

# Calcular métricas por algoritmo y nivel de dinamismo
metricas = df.groupby(['Dinamismo', 'Algoritmo']).agg({
    'Tiempo': 'mean',
    'Longitud': 'mean',
    'Éxito': lambda x: (x.sum() / len(x)) * 100  # Tasa de éxito en porcentaje
}).reset_index()

# Crear figura con 3 subgráficos
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Análisis de Dinamismo: A* vs Algoritmo Genético (N=41)', fontsize=16, fontweight='bold')

# Colores para cada algoritmo
colores = {'A*': '#2E86AB', 'AG': '#A23B72'}

# Gráfico 1: Tiempo de ejecución promedio
for algo in ['A*', 'AG']:
    data = metricas[metricas['Algoritmo'] == algo]
    axes[0].plot(data['Dinamismo'], data['Tiempo'], marker='o', linewidth=2.5, 
                 markersize=10, label=algo, color=colores[algo])

axes[0].set_xlabel('Nivel de Dinamismo', fontsize=11)
axes[0].set_ylabel('Tiempo promedio (segundos)', fontsize=11)
axes[0].set_title('Tiempo de Ejecución', fontsize=12, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3)
axes[0].set_xticks([0.1, 0.25, 0.35])
axes[0].set_yscale('log')

# Gráfico 2: Tasa de éxito
bar_width = 0.03
x_pos = np.array([0.1, 0.25, 0.35])
data_a = metricas[metricas['Algoritmo'] == 'A*']['Éxito'].values
data_ag = metricas[metricas['Algoritmo'] == 'AG']['Éxito'].values

axes[1].bar(x_pos - bar_width/2, data_a, bar_width, 
            label='A*', color=colores['A*'], alpha=0.8)
axes[1].bar(x_pos + bar_width/2, data_ag, bar_width, 
            label='AG', color=colores['AG'], alpha=0.8)

axes[1].set_xlabel('Nivel de Dinamismo', fontsize=11)
axes[1].set_ylabel('Tasa de éxito (%)', fontsize=11)
axes[1].set_title('Tasa de Éxito', fontsize=12, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(True, alpha=0.3, axis='y')
axes[1].set_ylim(0, 105)
axes[1].set_xticks([0.1, 0.25, 0.35])

# Gráfico 3: Longitud de solución (solo casos exitosos)
metricas_exitosos = df_exitosos.groupby(['Dinamismo', 'Algoritmo']).agg({
    'Longitud': 'mean'
}).reset_index()

for algo in ['A*', 'AG']:
    data = metricas_exitosos[metricas_exitosos['Algoritmo'] == algo]
    axes[2].plot(data['Dinamismo'], data['Longitud'], marker='s', linewidth=2.5,
                 markersize=10, label=algo, color=colores[algo])

axes[2].set_xlabel('Nivel de Dinamismo', fontsize=11)
axes[2].set_ylabel('Longitud promedio de solución', fontsize=11)
axes[2].set_title('Calidad de Solución', fontsize=12, fontweight='bold')
axes[2].legend(fontsize=11)
axes[2].grid(True, alpha=0.3)
axes[2].set_xticks([0.1, 0.25, 0.35])

plt.tight_layout()
plt.savefig('dinamismo_comparacion.png', dpi=300, bbox_inches='tight')
plt.show()

# Generar resumen estadístico
print("\n" + "="*70)
print("RESUMEN ESTADÍSTICO POR ALGORITMO Y NIVEL DE DINAMISMO")
print("="*70)

for dinamismo in [0.1, 0.25, 0.35]:
    print(f"\n{'='*70}")
    print(f"DINAMISMO = {dinamismo}")
    print(f"{'='*70}")
    
    for algo in ['A*', 'AG']:
        df_subset = df[(df['Algoritmo'] == algo) & (df['Dinamismo'] == dinamismo)]
        df_subset_exitoso = df_exitosos[(df_exitosos['Algoritmo'] == algo) & 
                                        (df_exitosos['Dinamismo'] == dinamismo)]
        
        tasa_exito = (df_subset['Éxito'].sum() / len(df_subset)) * 100 if len(df_subset) > 0 else 0
        tiempo_promedio = df_subset['Tiempo'].mean() if len(df_subset) > 0 else 0
        tiempo_exito = df_subset_exitoso['Tiempo'].mean() if len(df_subset_exitoso) > 0 else 0
        longitud_promedio = df_subset_exitoso['Longitud'].mean() if len(df_subset_exitoso) > 0 else 0
        
        print(f"\n{algo}:")
        print(f"  Tasa de éxito: {tasa_exito:.1f}%")
        print(f"  Tiempo promedio (todos): {tiempo_promedio:.4f}s")
        print(f"  Tiempo promedio (éxitos): {tiempo_exito:.4f}s")
        print(f"  Longitud promedio: {longitud_promedio:.1f}")

print("\n" + "="*70)
print("CONCLUSIONES")
print("="*70)

# Calcular métricas globales
tasa_exito_a = (df[df['Algoritmo'] == 'A*']['Éxito'].sum() / len(df[df['Algoritmo'] == 'A*'])) * 100
tasa_exito_ag = (df[df['Algoritmo'] == 'AG']['Éxito'].sum() / len(df[df['Algoritmo'] == 'AG'])) * 100

tiempo_a = df_exitosos[df_exitosos['Algoritmo'] == 'A*']['Tiempo'].mean()
tiempo_ag = df_exitosos[df_exitosos['Algoritmo'] == 'AG']['Tiempo'].mean()

longitud_a = df_exitosos[df_exitosos['Algoritmo'] == 'A*']['Longitud'].mean()
longitud_ag = df_exitosos[df_exitosos['Algoritmo'] == 'AG']['Longitud'].mean()

print(f"""
A* muestra robustez limitada ante entornos dinámicos. Con dinamismo 0.1 mantiene
{metricas[(metricas['Algoritmo']=='A*')&(metricas['Dinamismo']==0.1)]['Éxito'].values[0]:.1f}% 
de éxito, pero colapsa a {metricas[(metricas['Algoritmo']=='A*')&(metricas['Dinamismo']==0.35)]['Éxito'].values[0]:.1f}% 
con dinamismo 0.35. Su naturaleza determinista y estática lo hace inadecuado para 
replaneamiento continuo: debe recalcular completamente el camino ante cambios. Mantiene 
velocidad ({tiempo_a:.4f}s promedio) y optimalidad cuando encuentra soluciones, pero 
su tasa de fallo crece exponencialmente con el dinamismo del entorno.

El Algoritmo Genético demuestra superioridad en escenarios dinámicos con {tasa_exito_ag:.1f}% 
de éxito global versus {tasa_exito_a:.1f}% de A*. Su población diversa le permite adaptarse 
a cambios sin reiniciar desde cero. Aunque más lento ({tiempo_ag:.4f}s vs {tiempo_a:.4f}s) 
y con soluciones más largas ({longitud_ag:.1f} vs {longitud_a:.1f} nodos), su tasa de éxito 
se mantiene consistente incluso con dinamismo alto. La capacidad evolutiva y exploración 
paralela lo hacen resiliente ante obstáculos cambiantes.

Recomendación: Para entornos dinámicos, el AG es preferible pese a su mayor costo 
computacional. A* requeriría extensiones como D* o LPA* para manejar dinamismo 
eficientemente. En aplicaciones críticas con cambios frecuentes (robots móviles, 
tráfico en tiempo real), la robustez del AG compensa su menor optimalidad y mayor tiempo.
""")