# Importar librerías necesarias
import pandas as pd
import numpy as np

# Configuración para mejor visualización
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


# ═══════════════════════════════════════════════════════════════
# DATOS DE LA PLATAFORMA SOUNDWAVE
# ═══════════════════════════════════════════════════════════════

# 1. CATÁLOGO DE ARTISTAS
artistas = pd.DataFrame({
    'artista_id': ['A001', 'A002', 'A003', 'A004', 'A005', 'A006', 'A007', 'A008'],
    'nombre': ['Bad Bunny', 'Taylor Swift', 'BTS', 'Peso Pluma', 'Dua Lipa', 
               'Feid', 'The Weeknd', 'Karol G'],
    'pais_origen': ['Puerto Rico', 'USA', 'Corea del Sur', 'México', 'Reino Unido',
                   'Colombia', 'Canadá', 'Colombia'],
    'genero_principal': ['Reggaeton', 'Pop', 'K-Pop', 'Regional Mexicano', 'Pop',
                        'Reggaeton', 'R&B', 'Reggaeton'],
    'seguidores_millones': [45.2, 52.1, 48.7, 12.3, 38.5, 18.9, 41.2, 35.6]
})

# 2. CATÁLOGO DE CANCIONES
canciones = pd.DataFrame({
    'cancion_id': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008',
                   'C009', 'C010', 'C011', 'C012', 'C013', 'C014', 'C015', 'C016'],
    'artista_id': ['A001', 'A001', 'A002', 'A002', 'A003', 'A003', 'A004', 'A004',
                   'A005', 'A005', 'A006', 'A006', 'A007', 'A007', 'A008', 'A008'],
    'titulo': ['Monaco', 'Tití Me Preguntó', 'Anti-Hero', 'Shake It Off', 
               'Dynamite', 'Butter', 'Ella Baila Sola', 'Lady Gaga',
               'Levitating', 'Dance The Night', 'Ferxxo 100', 'Normal',
               'Blinding Lights', 'Save Your Tears', 'TQG', 'Provenza'],
    'duracion_segundos': [198, 243, 201, 219, 199, 165, 232, 185,
                          203, 176, 245, 198, 200, 215, 197, 208],
    'fecha_publicacion': ['2024-01-15', '2022-05-06', '2022-10-21', '2014-08-18',
                          '2020-08-21', '2021-05-21', '2023-03-10', '2023-06-23',
                          '2020-10-01', '2023-05-25', '2022-03-25', '2023-08-15',
                          '2020-03-20', '2021-02-05', '2023-02-24', '2022-04-22'],
    'explicito': [True, True, False, False, False, False, True, True,
                  False, False, True, True, False, False, True, False]
})

# 3. USUARIOS DE LA PLATAFORMA
usuarios = pd.DataFrame({
    'usuario_id': ['U001', 'U002', 'U003', 'U004', 'U005', 'U006', 'U007', 'U008',
                   'U009', 'U010', 'U011', 'U012', 'U013', 'U014', 'U015', 'U016'],
    'nombre': ['Carlos', 'María', 'Juan', 'Ana', 'Pedro', 'Sofía', 'Diego', 'Valentina',
               'Miguel', 'Camila', 'Andrés', 'Isabella', 'Ricardo', 'Fernanda', 'Jorge', 'Lucía'],
    'pais': ['México', 'México', 'Colombia', 'Colombia', 'España', 'España', 
             'Argentina', 'Argentina', 'Chile', 'Chile', 'Perú', 'Perú',
             'México', 'México', 'Colombia', 'Colombia'],
    'tipo_cuenta': ['Premium', 'Free', 'Premium', 'Premium', 'Free', 'Premium',
                    'Premium', 'Free', 'Premium', 'Free', 'Free', 'Premium',
                    'Premium', 'Free', 'Premium', 'Premium'],
    'edad': [22, 25, 19, 31, 28, 24, 35, 20, 27, 23, 29, 18, 33, 21, 26, 30],
    'fecha_registro': ['2023-01-15', '2023-03-22', '2022-11-08', '2023-06-17',
                       '2022-08-30', '2023-02-14', '2021-12-01', '2023-09-05',
                       '2022-05-20', '2023-07-11', '2023-04-03', '2022-10-25',
                       '2021-06-15', '2023-08-19', '2022-02-28', '2023-01-07']
})

# 4. STREAMS DE ENERO 2024
streams_enero = pd.DataFrame({
    'stream_id': [f'S{i:04d}' for i in range(1, 26)],
    'usuario_id': ['U001', 'U002', 'U001', 'U003', 'U004', 'U005', 'U006', 'U007',
                   'U008', 'U009', 'U010', 'U011', 'U012', 'U001', 'U002', 'U003',
                   'U013', 'U014', 'U015', 'U016', 'U004', 'U005', 'U006', 'U007', 'U008'],
    'cancion_id': ['C001', 'C003', 'C007', 'C005', 'C001', 'C009', 'C013', 'C015',
                   'C002', 'C011', 'C004', 'C006', 'C008', 'C010', 'C012', 'C014',
                   'C001', 'C003', 'C007', 'C015', 'C016', 'C002', 'C005', 'C009', 'C011'],
    'fecha': ['2024-01-05'] * 8 + ['2024-01-12'] * 8 + ['2024-01-20'] * 9,
    'escucha_completa': [True, True, False, True, True, True, True, False,
                         True, True, True, False, True, True, False, True,
                         True, True, True, True, False, True, True, True, False],
    'mes': ['Enero'] * 25
})

# 5. STREAMS DE FEBRERO 2024
streams_febrero = pd.DataFrame({
    'stream_id': [f'S{i:04d}' for i in range(26, 51)],
    'usuario_id': ['U002', 'U004', 'U006', 'U008', 'U010', 'U012', 'U014', 'U016',
                   'U001', 'U003', 'U005', 'U007', 'U009', 'U011', 'U013', 'U015',
                   'U002', 'U004', 'U006', 'U008', 'U010', 'U012', 'U014', 'U016', 'U001'],
    'cancion_id': ['C001', 'C001', 'C001', 'C003', 'C003', 'C005', 'C007', 'C007',
                   'C009', 'C011', 'C013', 'C015', 'C002', 'C004', 'C006', 'C008',
                   'C010', 'C012', 'C014', 'C016', 'C001', 'C007', 'C015', 'C003', 'C013'],
    'fecha': ['2024-02-03'] * 8 + ['2024-02-14'] * 8 + ['2024-02-25'] * 9,
    'escucha_completa': [True, True, True, False, True, True, True, True,
                         True, False, True, True, True, True, False, True,
                         True, True, True, False, True, True, True, True, True],
    'mes': ['Febrero'] * 25
})


# ╔═══════════════════════════════════════════════════════════════╗
# ║ EJERCICIO 1.1: Combinar streams de Enero y Febrero            ║
# ╚═══════════════════════════════════════════════════════════════╝

# Apilar verticalmente los streams de ambos meses y reiniciar el índice
streams_total = pd.concat([streams_enero, streams_febrero], ignore_index=True)

# Verificación
print(f"Total de streams combinados: {len(streams_total)}")
print(streams_total.head())


# ╔═══════════════════════════════════════════════════════════════╗
# ║ EJERCICIO 2.1: Unir streams con información de canciones      ║
# ╚═══════════════════════════════════════════════════════════════╝

# Inner join entre los streams y el catálogo de canciones por cancion_id
streams_canciones = pd.merge(streams_total, canciones, on='cancion_id', how='inner')

# Verificación
print(streams_canciones[['stream_id', 'titulo', 'fecha', 'escucha_completa']].head(10))


# ╔═══════════════════════════════════════════════════════════════╗
# ║ EJERCICIO 2.2: Agregar información de artistas                ║
# ╚═══════════════════════════════════════════════════════════════╝

# Unir el resultado anterior con artistas para sumar género y nombre del artista
streams_completos = pd.merge(streams_canciones, artistas, on='artista_id', how='inner')

# Columnas relevantes para el reporte (nombre = nombre del artista)
columnas_reporte = ['stream_id', 'titulo', 'nombre', 'genero_principal', 'fecha', 'escucha_completa']
streams_reporte = streams_completos[columnas_reporte]

# Verificación
print(streams_reporte.head(10))


# ╔═══════════════════════════════════════════════════════════════╗
# ║ EJERCICIO 2.3: Comparar comportamiento Premium vs Free        ║
# ╚═══════════════════════════════════════════════════════════════╝

# 1. Unir streams con los datos de usuario (para conocer el tipo de cuenta)
streams_usuarios = pd.merge(streams_total, usuarios, on='usuario_id', how='inner')

# 2-3. Porcentaje de escuchas completas por tipo de cuenta
#    (el promedio de una columna booleana equivale a la proporción de True)
pct_completas = streams_usuarios.groupby('tipo_cuenta')['escucha_completa'].mean() * 100

print("Porcentaje de escuchas completas por tipo de cuenta:")
print(pct_completas.round(1))

# ¿Qué tipo de usuario escucha más completo?
tipo_top = pct_completas.idxmax()
print(f"\nLos usuarios {tipo_top} escuchan más canciones completas "
      f"({pct_completas.max():.1f}%).")


# ╔═══════════════════════════════════════════════════════════════╗
# ║ EJERCICIO 3.1: Top 5 artistas más escuchados                  ║
# ╚═══════════════════════════════════════════════════════════════╝

# Contar streams por artista y quedarse con los 5 primeros
top_artistas = streams_completos.groupby('nombre').size() \
    .sort_values(ascending=False).head(5)

print("🏆 TOP 5 ARTISTAS POR STREAMS")
print("=" * 40)
for i, (artista, n) in enumerate(top_artistas.items(), 1):
    print(f"#{i}  {artista:<15} {n} streams")


# ╔═══════════════════════════════════════════════════════════════╗
# ║ EJERCICIO 3.2: Estadísticas por género musical                ║
# ╚═══════════════════════════════════════════════════════════════╝

# Múltiples agregaciones por género: total de streams, tasa de completion y artistas únicos
stats_genero = streams_completos.groupby('genero_principal').agg(
    total_streams=('stream_id', 'count'),
    tasa_completion=('escucha_completa', 'mean'),
    artistas_unicos=('nombre', 'nunique')
)
# Pasar la tasa a porcentaje y ordenar por total de streams
stats_genero['tasa_completion'] = (stats_genero['tasa_completion'] * 100).round(1)
stats_genero = stats_genero.sort_values('total_streams', ascending=False)

print("📊 Estadísticas por género musical:")
print(stats_genero)


# ╔═══════════════════════════════════════════════════════════════╗
# ║ EJERCICIO 3.3: Streams por país y mes                         ║
# ╚═══════════════════════════════════════════════════════════════╝

# 1-3. Unir con usuarios para tener el país y contar streams por país y mes
streams_pais = pd.merge(streams_total, usuarios, on='usuario_id', how='inner')
por_pais_mes = streams_pais.groupby(['pais', 'mes']).size().reset_index(name='streams')

print("🌎 Streams por país y mes:")
print(por_pais_mes)

# 4. País con mayor crecimiento entre Enero y Febrero
tabla = por_pais_mes.pivot(index='pais', columns='mes', values='streams').fillna(0)
tabla['crecimiento'] = tabla['Febrero'] - tabla['Enero']
pais_top = tabla['crecimiento'].idxmax()
print(f"\nEl país que más creció fue {pais_top} "
      f"(+{int(tabla.loc[pais_top, 'crecimiento'])} streams).")


# ╔═══════════════════════════════════════════════════════════════╗
# ║ EJERCICIO 4.1: Pivot table de streams por género y país       ║
# ╚═══════════════════════════════════════════════════════════════╝

# 1-2. DataFrame con género (de artistas) y país (del usuario) en cada stream
streams_genero_pais = pd.merge(streams_completos, usuarios, on='usuario_id', how='inner')

# 3. Matriz género x país con conteo de streams; huecos rellenos con 0
pivot_genero_pais = pd.pivot_table(
    streams_genero_pais,
    values='stream_id',
    index='genero_principal',
    columns='pais',
    aggfunc='count',
    fill_value=0
)

print("📊 MATRIZ DE STREAMS (género x país):")
print(pivot_genero_pais)


# ╔═══════════════════════════════════════════════════════════════╗
# ║ EJERCICIO 4.2: Engagement por mes y tipo de cuenta            ║
# ╚═══════════════════════════════════════════════════════════════╝

# Reutilizamos streams_usuarios (streams + datos de usuario)
# Pivot: filas = mes, columnas = tipo de cuenta, valores = tasa de escucha completa
engagement = pd.pivot_table(
    streams_usuarios,
    values='escucha_completa',
    index='mes',
    columns='tipo_cuenta',
    aggfunc='mean'
)
# Expresar como porcentaje y ordenar los meses cronológicamente
engagement = (engagement * 100).round(1).reindex(['Enero', 'Febrero'])

print("📈 Tasa de completion por mes y tipo de cuenta (%):")
print(engagement)

# Interpretación: ¿mejoró el engagement en Febrero?
if (engagement.loc['Febrero'] >= engagement.loc['Enero']).all():
    print("\nEl engagement mejoró (o se mantuvo) en Febrero para ambos tipos de cuenta.")
else:
    print("\nEl engagement no mejoró de forma generalizada en Febrero.")


# ╔═══════════════════════════════════════════════════════════════╗
# ║ EJERCICIO 5.1 (BONUS): Convertir pivot a formato largo        ║
# ╚═══════════════════════════════════════════════════════════════╝

# 1. Reiniciar el índice para que 'genero_principal' sea una columna
pivot_reset = pivot_genero_pais.reset_index()

# 2. Pasar de formato ancho a largo con melt()
streams_largo = pd.melt(
    pivot_reset,
    id_vars=['genero_principal'],
    var_name='pais',
    value_name='streams'
)

print("🔄 Datos en formato largo (género, país, streams):")
print(streams_largo.head(15))


# ╔═══════════════════════════════════════════════════════════════╗
# ║ DESAFÍO FINAL: Genera el reporte ejecutivo completo           ║
# ╚═══════════════════════════════════════════════════════════════╝

print("="*60)
print("📊 SOUNDWAVE - REPORTE EJECUTIVO Q1 2024")
print("="*60)

# 1. Top 3 canciones más escuchadas (con nombre de artista)
print("\n🎵 TOP 3 CANCIONES")
print("-"*40)
top_canciones = streams_completos.groupby(['titulo', 'nombre']).size() \
    .sort_values(ascending=False).head(3)
for i, ((titulo, artista), n) in enumerate(top_canciones.items(), 1):
    print(f"{i}. {titulo} - {artista} ({n} streams)")

# 2. Género con mejor tasa de completion
print("\n🎸 GÉNERO CON MEJOR ENGAGEMENT")
print("-"*40)
completion_genero = streams_completos.groupby('genero_principal')['escucha_completa'].mean() * 100
genero_top = completion_genero.idxmax()
print(f"{genero_top} ({completion_genero.max():.1f}% completion)")

# 3. País con más streams totales
print("\n🌎 PAÍS LÍDER EN STREAMS")
print("-"*40)
streams_por_pais = streams_usuarios.groupby('pais').size().sort_values(ascending=False)
pais_lider = streams_por_pais.idxmax()
print(f"{pais_lider} ({streams_por_pais.max()} streams)")

# 4. Premium vs Free (streams por usuario)
print("\n💎 PREMIUM VS FREE (streams por usuario)")
print("-"*40)
# Streams totales por tipo de cuenta entre número de usuarios de ese tipo
streams_por_tipo = streams_usuarios.groupby('tipo_cuenta').size()
usuarios_por_tipo = usuarios.groupby('tipo_cuenta').size()
promedio_por_usuario = (streams_por_tipo / usuarios_por_tipo).round(2)
for tipo, valor in promedio_por_usuario.items():
    print(f"{tipo}: {valor} streams/usuario")

# 5. Artista con mayor crecimiento entre Enero y Febrero
print("\n🚀 ARTISTA DESTACADO (mayor crecimiento)")
print("-"*40)
por_artista_mes = streams_completos.groupby(['nombre', 'mes']).size() \
    .unstack(fill_value=0)
por_artista_mes['crecimiento'] = por_artista_mes.get('Febrero', 0) - por_artista_mes.get('Enero', 0)
artista_destacado = por_artista_mes['crecimiento'].idxmax()
print(f"{artista_destacado} (+{int(por_artista_mes.loc[artista_destacado, 'crecimiento'])} "
      f"streams de Enero a Febrero)")

print("\n" + "="*60)
