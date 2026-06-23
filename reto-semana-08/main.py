import numpy as np

# Configuración para reproducibilidad
np.random.seed(42)


# ═══════════════════════════════════════════════════════════════════
#                    GENERACIÓN DE DATOS DE SENSORES
# ═══════════════════════════════════════════════════════════════════

# Nombres de estaciones
estaciones = ['Coyoacán', 'Azcapotzalco', 'Xochimilco', 'Tlalpan', 'Miguel Hidalgo']
n_estaciones = len(estaciones)
n_dias = 7
n_horas = 24

# ─────────────────────────────────────────────────────────────────────
# TEMPERATURA (°C)
# Array 3D: (estaciones, días, horas)
# ─────────────────────────────────────────────────────────────────────
# Base de temperatura por estación (algunas zonas más cálidas)
temp_base = np.array([22, 24, 20, 19, 23])  # Temperatura base por estación

# Variación diaria (ciclo día/noche)
hora_del_dia = np.arange(24)
variacion_diaria = 5 * np.sin((hora_del_dia - 6) * np.pi / 12)  # Máx a las 14h, mín a las 6h

# Generar datos de temperatura
temperatura = np.zeros((n_estaciones, n_dias, n_horas))
for i in range(n_estaciones):
    for d in range(n_dias):
        temperatura[i, d, :] = temp_base[i] + variacion_diaria + np.random.normal(0, 1.5, n_horas)

# Introducir algunos valores faltantes (sensores desconectados)
temperatura[1, 2, 10:14] = np.nan  # Azcapotzalco, día 3, horas 10-13
temperatura[3, 5, 0:3] = np.nan    # Tlalpan, día 6, horas 0-2

# ─────────────────────────────────────────────────────────────────────
# HUMEDAD RELATIVA (%)
# Array 3D: (estaciones, días, horas)
# ─────────────────────────────────────────────────────────────────────
humedad_base = np.array([55, 45, 70, 65, 50])  # Xochimilco y Tlalpan más húmedos

# Variación inversa a temperatura (más húmedo en la noche)
variacion_humedad = -15 * np.sin((hora_del_dia - 6) * np.pi / 12)

humedad = np.zeros((n_estaciones, n_dias, n_horas))
for i in range(n_estaciones):
    for d in range(n_dias):
        humedad[i, d, :] = humedad_base[i] + variacion_humedad + np.random.normal(0, 5, n_horas)

# Asegurar rango válido [20, 95]
humedad = np.clip(humedad, 20, 95)

# Valores faltantes
humedad[0, 4, 15:18] = np.nan  # Coyoacán, día 5, horas 15-17

# ─────────────────────────────────────────────────────────────────────
# NIVELES DE CO2 (ppm)
# Array 3D: (estaciones, días, horas)
# ─────────────────────────────────────────────────────────────────────
co2_base = np.array([380, 420, 360, 350, 410])  # Zonas con más tráfico tienen más CO2

# Patrón de hora pico (más CO2 en horas de tráfico)
patron_trafico = np.zeros(24)
patron_trafico[7:10] = 30   # Hora pico mañana
patron_trafico[17:20] = 40  # Hora pico tarde
patron_trafico[12:14] = 15  # Mediodía

co2 = np.zeros((n_estaciones, n_dias, n_horas))
for i in range(n_estaciones):
    for d in range(n_dias):
        co2[i, d, :] = co2_base[i] + patron_trafico + np.random.normal(0, 10, n_horas)

# Día de contingencia (día 4) - CO2 elevado
co2[:, 3, :] *= 1.15

# Valores faltantes
co2[2, 1, 5:8] = np.nan  # Xochimilco, día 2, horas 5-7

# ─────────────────────────────────────────────────────────────────────
# ARRAY 2D SIMPLIFICADO: Promedios diarios por estación
# ─────────────────────────────────────────────────────────────────────
# Para ejercicios más simples
temp_promedio_diario = np.nanmean(temperatura, axis=2)  # Shape: (5, 7)
humedad_promedio_diario = np.nanmean(humedad, axis=2)
co2_promedio_diario = np.nanmean(co2, axis=2)


# ═══════════════════════════════════════════════════════════════════
#                    EJERCICIO 1.1: INSPECCIÓN
# ═══════════════════════════════════════════════════════════════════

# 1. Número de dimensiones del array temperatura
n_dimensiones = temperatura.ndim

# 2. Forma (shape) del array
forma = temperatura.shape

# 3. Número total de elementos
total_elementos = temperatura.size

# 4. Tipo de datos
tipo_datos = temperatura.dtype

# 5. Tamaño en memoria (bytes)
memoria_bytes = temperatura.nbytes

# Mostrar resultados
print("📊 PROPIEDADES DEL ARRAY TEMPERATURA")
print("─" * 40)
print(f"Dimensiones: {n_dimensiones}D")
print(f"Forma: {forma}")
print(f"  → {forma[0]} estaciones")
print(f"  → {forma[1]} días")
print(f"  → {forma[2]} horas por día")
print(f"Total de mediciones: {total_elementos:,}")
print(f"Tipo de datos: {tipo_datos}")
print(f"Memoria: {memoria_bytes:,} bytes ({memoria_bytes/1024:.2f} KB)")


# ═══════════════════════════════════════════════════════════════════
#                    EJERCICIO 1.2: INDEXACIÓN
# ═══════════════════════════════════════════════════════════════════

# 1. Temperatura de Coyoacán (índice 0), día 1 (índice 0), a las 12:00 (índice 12)
temp_coyoacan_d1_12h = temperatura[0, 0, 12]
print(f"🌡️ Coyoacán, Día 1, 12:00h: {temp_coyoacan_d1_12h:.1f}°C")

# 2. Todas las temperaturas de Xochimilco (índice 2) en el día 3 (índice 2)
#    Los ":" finales toman las 24 horas completas
temp_xochimilco_d3 = temperatura[2, 2, :]
print(f"\n🌡️ Xochimilco, Día 3 (24 horas):")
print(f"   Primeras 6 horas: {temp_xochimilco_d3[:6].round(1)}")

# 3. Temperatura promedio diario de Miguel Hidalgo (índice 4) para los 7 días
#    Se usa el array 2D ya calculado (estaciones, días)
temp_mh_7dias = temp_promedio_diario[4]
print(f"\n📊 Miguel Hidalgo - Promedio por día:")
print(f"   {temp_mh_7dias.round(1)}")

# 4. Último valor de CO2 registrado (última estación, último día, última hora)
#    Los índices negativos cuentan desde el final
ultimo_co2 = co2[-1, -1, -1]
print(f"\n🏭 Último CO2 registrado: {ultimo_co2:.1f} ppm")


# ═══════════════════════════════════════════════════════════════════
#                    EJERCICIO 1.3: SLICING
# ═══════════════════════════════════════════════════════════════════

# 1. Temperaturas de TODAS las estaciones, TODOS los días, solo horas de la TARDE (12-18)
#    El slice 12:18 toma las horas 12 a 17 (6 horas)
temp_tardes = temperatura[:, :, 12:18]
print(f"🌅 Temperaturas de tardes (12-17h)")
print(f"   Shape: {temp_tardes.shape}")

# 2. Humedad de las primeras 3 estaciones, últimos 3 días, todas las horas
#    -3: toma los últimos 3 días
humedad_subset = humedad[:3, -3:, :]
print(f"\n💧 Subset de humedad")
print(f"   Shape: {humedad_subset.shape}")

# 3. CO2 de estaciones pares (0, 2, 4), todos los días, horas de mañana (6-12)
#    El paso ::2 selecciona las estaciones de índice par
co2_mañanas_pares = co2[::2, :, 6:12]
print(f"\n🏭 CO2 mañanas (estaciones pares)")
print(f"   Shape: {co2_mañanas_pares.shape}")

# 4. Temperaturas en orden inverso de días (del día 7 al día 1)
#    El paso ::-1 sobre el eje de días invierte su orden
temp_inverso = temperatura[:, ::-1, :]
print(f"\n🔄 Temperatura días invertidos")
print(f"   Shape: {temp_inverso.shape}")


# ═══════════════════════════════════════════════════════════════════
#                 EJERCICIO 2.1: ESTADÍSTICAS GLOBALES
# ═══════════════════════════════════════════════════════════════════

# IMPORTANTE: Los arrays tienen valores NaN (sensores desconectados)
# Por eso se usan las funciones nan* que los ignoran en el cálculo

# 1. Temperatura promedio global (de todas las mediciones)
temp_promedio = np.nanmean(temperatura)

# 2. Temperatura máxima registrada
temp_maxima = np.nanmax(temperatura)

# 3. Temperatura mínima registrada
temp_minima = np.nanmin(temperatura)

# 4. Desviación estándar de temperatura
temp_std = np.nanstd(temperatura)

# 5. Rango de temperatura (máxima - mínima)
temp_rango = temp_maxima - temp_minima

print("╔══════════════════════════════════════════════════════════════╗")
print("║           ESTADÍSTICAS GLOBALES DE TEMPERATURA               ║")
print("╠══════════════════════════════════════════════════════════════╣")
print(f"║  Promedio:     {temp_promedio:>6.2f} °C                              ║")
print(f"║  Máxima:       {temp_maxima:>6.2f} °C                              ║")
print(f"║  Mínima:       {temp_minima:>6.2f} °C                              ║")
print(f"║  Desv. Est.:   {temp_std:>6.2f} °C                              ║")
print(f"║  Rango:        {temp_rango:>6.2f} °C                              ║")
print("╚══════════════════════════════════════════════════════════════╝")


# ═══════════════════════════════════════════════════════════════════
#                 EJERCICIO 2.2: ESTADÍSTICAS POR EJE
# ═══════════════════════════════════════════════════════════════════

# 1. Temperatura promedio POR ESTACIÓN (promedio sobre días y horas)
#    axis=(1,2) colapsa días y horas, deja 5 valores (uno por estación)
temp_por_estacion = np.nanmean(temperatura, axis=(1, 2))

print("🌡️ TEMPERATURA PROMEDIO POR ESTACIÓN")
print("─" * 40)
for i, est in enumerate(estaciones):
    print(f"   {est:15s}: {temp_por_estacion[i]:5.1f} °C")

# 2. Humedad promedio POR HORA DEL DÍA (promedio sobre estaciones y días)
#    axis=(0,1) colapsa estaciones y días, deja 24 valores (uno por hora)
humedad_por_hora = np.nanmean(humedad, axis=(0, 1))

print("\n💧 HUMEDAD PROMEDIO POR HORA")
print("─" * 40)
print("   Hora │ Humedad")
for h in [0, 6, 12, 18]:
    print(f"   {h:02d}:00 │ {humedad_por_hora[h]:5.1f}%")

# 3. CO2 máximo POR DÍA (máximo considerando todas las estaciones y horas)
#    axis=(0,2) colapsa estaciones y horas, deja 7 valores (uno por día)
co2_max_por_dia = np.nanmax(co2, axis=(0, 2))

print("\n🏭 CO2 MÁXIMO POR DÍA")
print("─" * 40)
for d in range(n_dias):
    print(f"   Día {d+1}: {co2_max_por_dia[d]:6.1f} ppm")


# ═══════════════════════════════════════════════════════════════════
#              EJERCICIO 3.1: CONVERSIONES VECTORIZADAS
# ═══════════════════════════════════════════════════════════════════

# Las operaciones se aplican a todo el array a la vez (sin loops)

# 1. Convertir temperatura de Celsius a Fahrenheit  (F = C × 9/5 + 32)
temperatura_fahrenheit = temperatura * 9 / 5 + 32

print("🌡️ TEMPERATURA EN FAHRENHEIT")
print(f"   Promedio: {np.nanmean(temperatura_fahrenheit):.1f} °F")
print(f"   Máxima:   {np.nanmax(temperatura_fahrenheit):.1f} °F")
print(f"   Mínima:   {np.nanmin(temperatura_fahrenheit):.1f} °F")

# 2. Convertir temperatura de Celsius a Kelvin  (K = C + 273.15)
temperatura_kelvin = temperatura + 273.15

print(f"\n🌡️ TEMPERATURA EN KELVIN")
print(f"   Promedio: {np.nanmean(temperatura_kelvin):.1f} K")

# 3. Normalizar humedad a rango [0, 1]  ->  (valor - min) / (max - min)
humedad_min = np.nanmin(humedad)
humedad_max = np.nanmax(humedad)
humedad_normalizada = (humedad - humedad_min) / (humedad_max - humedad_min)

print(f"\n💧 HUMEDAD NORMALIZADA [0-1]")
print(f"   Promedio: {np.nanmean(humedad_normalizada):.3f}")
print(f"   Min:      {np.nanmin(humedad_normalizada):.3f}")
print(f"   Max:      {np.nanmax(humedad_normalizada):.3f}")


# ═══════════════════════════════════════════════════════════════════
#              EJERCICIO 3.2: ÍNDICE DE CONFORT TÉRMICO
# ═══════════════════════════════════════════════════════════════════

# 1. ICT para TODAS las mediciones (broadcasting elemento a elemento)
#    ICT = temperatura + 0.05 * humedad
ict = temperatura + 0.05 * humedad

print("🌡️💧 ÍNDICE DE CONFORT TÉRMICO (ICT)")
print("─" * 45)
print(f"   Shape del array ICT: {ict.shape}")
print(f"   ICT promedio: {np.nanmean(ict):.2f}")
print(f"   ICT máximo:   {np.nanmax(ict):.2f}")
print(f"   ICT mínimo:   {np.nanmin(ict):.2f}")

# 2. Clasificar con indexación booleana.
#    Las comparaciones con NaN dan False, así que los NaN no se cuentan.

# Frío (ICT < 20)
n_frio = np.sum(ict < 20)

# Confortable (20 <= ICT < 25)
n_confortable = np.sum((ict >= 20) & (ict < 25))

# Cálido (25 <= ICT < 30)
n_calido = np.sum((ict >= 25) & (ict < 30))

# Muy caluroso (ICT >= 30)
n_muy_caluroso = np.sum(ict >= 30)

# Total de mediciones válidas (sin NaN)
n_validas = np.sum(~np.isnan(ict))

print("\n📊 DISTRIBUCIÓN DE CONDICIONES")
print("─" * 45)
print(f"   ❄️  Frío (<20):           {n_frio:5d} ({100*n_frio/n_validas:5.1f}%)")
print(f"   ✅ Confortable (20-25):  {n_confortable:5d} ({100*n_confortable/n_validas:5.1f}%)")
print(f"   🌤️  Cálido (25-30):       {n_calido:5d} ({100*n_calido/n_validas:5.1f}%)")
print(f"   🔥 Muy caluroso (≥30):   {n_muy_caluroso:5d} ({100*n_muy_caluroso/n_validas:5.1f}%)")
print(f"   ────────────────────────────────────────")
print(f"   Total válidas:           {n_validas:5d}")


# ═══════════════════════════════════════════════════════════════════
#              EJERCICIO 4.1: DETECCIÓN DE ANOMALÍAS
# ═══════════════════════════════════════════════════════════════════

# Criterio: un valor es anómalo si está a más de 2 desviaciones estándar
# de la media

# 1. Media y desviación estándar del CO2 (ignorando NaN)
co2_media = np.nanmean(co2)
co2_std = np.nanstd(co2)

# 2. Límites del rango normal (media ± 2*std)
limite_inferior = co2_media - 2 * co2_std
limite_superior = co2_media + 2 * co2_std

print("🏭 ANÁLISIS DE ANOMALÍAS EN CO2")
print("─" * 45)
print(f"   Media CO2:      {co2_media:.1f} ppm")
print(f"   Desv. Est.:     {co2_std:.1f} ppm")
print(f"   Límite inferior: {limite_inferior:.1f} ppm")
print(f"   Límite superior: {limite_superior:.1f} ppm")

# 3. Máscara booleana: fuera de los límites y que no sea NaN
mascara_anomalias = ((co2 < limite_inferior) | (co2 > limite_superior)) & ~np.isnan(co2)

# 4. Cuenta el número de anomalías
n_anomalias = np.sum(mascara_anomalias)

# 5. Obtén los valores anómalos
valores_anomalos = co2[mascara_anomalias]

print(f"\n⚠️  ANOMALÍAS DETECTADAS: {n_anomalias}")
if n_anomalias > 0:
    print(f"   Valores: {valores_anomalos[:10].round(1)}")
    if n_anomalias > 10:
        print(f"   ... y {n_anomalias - 10} más")


# ═══════════════════════════════════════════════════════════════════
#           EJERCICIO 4.2: ANÁLISIS DE CONTINGENCIA AMBIENTAL
# ═══════════════════════════════════════════════════════════════════

# El día 4 (índice 3) hubo contingencia ambiental
DIA_CONTINGENCIA = 3

# 1. CO2 del día de contingencia (todas las estaciones y horas) -> (5, 24)
co2_contingencia = co2[:, DIA_CONTINGENCIA, :]

# 2. CO2 de los días normales (todos excepto el día 4) -> (5, 6, 24)
dias_normales = [0, 1, 2, 4, 5, 6]  # Todos excepto el 3
co2_dias_normales = co2[:, dias_normales, :]

# 3. Promedio de CO2 en el día de contingencia
promedio_contingencia = np.nanmean(co2_contingencia)

# 4. Promedio de CO2 en días normales
promedio_normal = np.nanmean(co2_dias_normales)

# 5. Incremento porcentual respecto a los días normales
incremento_porcentual = ((promedio_contingencia - promedio_normal) / promedio_normal) * 100

print("╔══════════════════════════════════════════════════════════════╗")
print("║           ANÁLISIS DE CONTINGENCIA AMBIENTAL                 ║")
print("║                        Día 4                                 ║")
print("╠══════════════════════════════════════════════════════════════╣")
print(f"║  CO2 promedio día contingencia: {promedio_contingencia:>7.1f} ppm              ║")
print(f"║  CO2 promedio días normales:    {promedio_normal:>7.1f} ppm              ║")
print(f"║  Incremento:                    {incremento_porcentual:>7.1f} %               ║")
print("╚══════════════════════════════════════════════════════════════╝")

# 6. Estación más afectada (mayor incremento de CO2)
#    Promedio por estación: contingencia colapsa solo horas (axis=1),
#    días normales colapsa días y horas (axis=(1,2))
co2_por_estacion_contingencia = np.nanmean(co2_contingencia, axis=1)
co2_por_estacion_normal = np.nanmean(co2_dias_normales, axis=(1, 2))

# Incremento por estación
incremento_por_estacion = ((co2_por_estacion_contingencia - co2_por_estacion_normal) / 
                           co2_por_estacion_normal) * 100

# Índice de la estación con mayor incremento
idx_mas_afectada = np.argmax(incremento_por_estacion)

print("\n📍 IMPACTO POR ESTACIÓN")
print("─" * 50)
for i, est in enumerate(estaciones):
    barra = "█" * int(incremento_por_estacion[i] / 2)
    print(f"   {est:15s}: +{incremento_por_estacion[i]:5.1f}% {barra}")

print(f"\n⚠️  Estación más afectada: {estaciones[idx_mas_afectada]}")


# ═══════════════════════════════════════════════════════════════════
#                    EJERCICIO BONUS: REPORTE EJECUTIVO
# ═══════════════════════════════════════════════════════════════════

# 1. Estación más calurosa (mayor temperatura promedio)
#    argmax sobre el promedio por estación devuelve el índice del máximo
idx_mas_calurosa = np.argmax(np.nanmean(temperatura, axis=(1, 2)))
estacion_mas_calurosa = estaciones[idx_mas_calurosa]

# 2. Estación más húmeda (mayor humedad promedio)
idx_mas_humeda = np.argmax(np.nanmean(humedad, axis=(1, 2)))
estacion_mas_humeda = estaciones[idx_mas_humeda]

# 3. Estación con mejor calidad de aire (menor CO2 promedio -> argmin)
idx_mejor_aire = np.argmin(np.nanmean(co2, axis=(1, 2)))
estacion_mejor_aire = estaciones[idx_mejor_aire]

# 4. Hora más calurosa del día (promedio de todas las estaciones y días)
temp_por_hora = np.nanmean(temperatura, axis=(0, 1))
hora_mas_calurosa = np.argmax(temp_por_hora)

# 5. Hora con peor calidad de aire (mayor CO2 promedio)
co2_por_hora = np.nanmean(co2, axis=(0, 1))
hora_peor_aire = np.argmax(co2_por_hora)

# 6. Número de valores faltantes en total (suma de la máscara isnan)
nan_temperatura = np.sum(np.isnan(temperatura))
nan_humedad = np.sum(np.isnan(humedad))
nan_co2 = np.sum(np.isnan(co2))
total_nan = nan_temperatura + nan_humedad + nan_co2

print("")
print("╔══════════════════════════════════════════════════════════════════════╗")
print("║                                                                      ║")
print("║            🌡️  METEOSENSE - REPORTE EJECUTIVO SEMANAL  💨            ║")
print("║                        CDMX - Semana de Análisis                     ║")
print("║                                                                      ║")
print("╠══════════════════════════════════════════════════════════════════════╣")
print("║                                                                      ║")
print("║  📊 RESUMEN DE CONDICIONES                                           ║")
print("║  ─────────────────────────────────────────────────────────────────   ║")
print(f"║    🌡️  Temperatura promedio:    {np.nanmean(temperatura):>5.1f} °C                        ║")
print(f"║    💧 Humedad promedio:         {np.nanmean(humedad):>5.1f} %                         ║")
print(f"║    🏭 CO2 promedio:            {np.nanmean(co2):>6.1f} ppm                       ║")
print("║                                                                      ║")
print("║  🏆 RANKINGS                                                         ║")
print("║  ─────────────────────────────────────────────────────────────────   ║")
print(f"║    🔥 Estación más calurosa:   {estacion_mas_calurosa:15s}                  ║")
print(f"║    💧 Estación más húmeda:     {estacion_mas_humeda:15s}                  ║")
print(f"║    🌿 Mejor calidad de aire:   {estacion_mejor_aire:15s}                  ║")
print("║                                                                      ║")
print("║  ⏰ PATRONES TEMPORALES                                              ║")
print("║  ─────────────────────────────────────────────────────────────────   ║")
print(f"║    🌡️  Hora más calurosa:       {hora_mas_calurosa:02d}:00 hrs                          ║")
print(f"║    🏭 Hora con más CO2:         {hora_peor_aire:02d}:00 hrs                          ║")
print("║                                                                      ║")
print("║  ⚠️  CALIDAD DE DATOS                                                ║")
print("║  ─────────────────────────────────────────────────────────────────   ║")
print(f"║    Valores faltantes totales:  {total_nan:4d}                                 ║")
print(f"║      - Temperatura: {nan_temperatura:3d}                                            ║")
print(f"║      - Humedad:     {nan_humedad:3d}                                            ║")
print(f"║      - CO2:         {nan_co2:3d}                                            ║")
print("║                                                                      ║")
print("╚══════════════════════════════════════════════════════════════════════╝")
print("")
