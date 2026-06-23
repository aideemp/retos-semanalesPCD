import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


# PARTE 1: Análisis Estadístico Básico

def estadisticas_basicas(precios: pd.Series) -> Dict:
    """
    Calcula estadísticas descriptivas de los precios.
    """
    # Cada métrica es un método de agregación de la Series
    resultado = {
        "precio_actual": float(precios.iloc[-1]),        # último precio de la serie
        "precio_minimo": float(precios.min()),
        "precio_maximo": float(precios.max()),
        "precio_promedio": float(precios.mean()),
        "precio_mediana": float(precios.median()),
        "desviacion_std": float(precios.std()),
        "rango": float(precios.max() - precios.min()),
        "dias_analizados": int(len(precios))
    }

    return resultado


def calcular_rendimientos(precios: pd.Series) -> pd.Series:
    """
    Calcula el rendimiento diario porcentual.
    """
    # pct_change da la variación relativa respecto al día anterior; ×100 -> porcentaje
    # El primer valor queda como NaN (no hay día previo)
    return precios.pct_change() * 100


def analisis_rendimientos(rendimientos: pd.Series) -> Dict:
    """
    Analiza los rendimientos calculados.
    """
    # Se descarta el primer NaN para no afectar los cálculos
    rend = rendimientos.dropna()

    # idxmax/idxmin devuelven la fecha (índice) del mejor y peor día
    fecha_mejor = rend.idxmax()
    fecha_peor = rend.idxmin()

    def fecha_str(f):
        # Formatea el Timestamp del índice como YYYY-MM-DD
        return f.strftime('%Y-%m-%d') if hasattr(f, 'strftime') else str(f)

    resultado = {
        "rendimiento_total": float(rend.sum()),          # rendimiento acumulado (suma diaria)
        "rendimiento_promedio": float(rend.mean()),      # promedio diario
        "mejor_dia": (fecha_str(fecha_mejor), float(rend.loc[fecha_mejor])),
        "peor_dia": (fecha_str(fecha_peor), float(rend.loc[fecha_peor])),
        "dias_positivos": int((rend > 0).sum()),
        "dias_negativos": int((rend < 0).sum()),
        "volatilidad": float(rend.std())                 # desviación estándar de los rendimientos
    }

    return resultado


# PARTE 2: Indicadores Técnicos

def media_movil(precios: pd.Series, ventana: int) -> pd.Series:
    """
    Calcula la media móvil simple (SMA).
    """
    # rolling crea ventanas deslizantes de tamaño 'ventana'; mean promedia cada una
    return precios.rolling(window=ventana).mean()


def bandas_bollinger(precios: pd.Series, ventana: int = 20, num_std: int = 2) -> Dict:
    """
    Calcula las Bandas de Bollinger.
    """
    # Banda media = SMA; las bandas se separan num_std desviaciones de la media móvil
    media = precios.rolling(window=ventana).mean()
    desv = precios.rolling(window=ventana).std()

    resultado = {
        "banda_superior": media + num_std * desv,
        "banda_media": media,
        "banda_inferior": media - num_std * desv
    }

    return resultado


def detectar_maximos_minimos(precios: pd.Series, ventana: int = 5) -> Dict:
    """
    Detecta máximos y mínimos locales.
    """
    # Ventana centrada que abarca 'ventana' días antes y después de cada punto
    ventana_total = 2 * ventana + 1

    max_local = precios.rolling(window=ventana_total, center=True).max()
    min_local = precios.rolling(window=ventana_total, center=True).min()

    # Un punto es máximo local si coincide con el máximo de su vecindario
    es_maximo = precios == max_local
    es_minimo = precios == min_local

    resultado = {
        "maximos": precios[es_maximo],
        "minimos": precios[es_minimo]
    }

    return resultado


def clasificar_tendencia(precios: pd.Series, ventana: int = 10) -> str:
    """
    Clasifica la tendencia actual.
    """
    ma = media_movil(precios, ventana)

    precio_actual = precios.iloc[-1]
    ma_actual = ma.iloc[-1]
    ma_previa = ma.iloc[-2]   # valor de la MA un día antes, para ver su pendiente

    # ALCISTA: precio por encima de la MA y la MA creciendo
    if precio_actual > ma_actual and ma_actual > ma_previa:
        return "ALCISTA"
    # BAJISTA: precio por debajo de la MA y la MA decreciendo
    elif precio_actual < ma_actual and ma_actual < ma_previa:
        return "BAJISTA"
    else:
        return "LATERAL"


# PARTE 3: Sistema de Alertas

def generar_senales_trading(precios: pd.Series, ma_corta: int = 5, ma_larga: int = 20) -> pd.Series:
    """
    Genera señales de compra/venta basadas en cruces de medias móviles.
    """
    ma_c = media_movil(precios, ma_corta)
    ma_l = media_movil(precios, ma_larga)

    # Diferencia entre ambas medias: su cambio de signo indica un cruce
    diferencia = ma_c - ma_l

    # Por defecto MANTENER; se sobrescriben los días con cruce
    senales = pd.Series("MANTENER", index=precios.index)

    # COMPRA: la MA corta pasa de estar por debajo (o igual) a por encima
    cruce_arriba = (diferencia > 0) & (diferencia.shift(1) <= 0)
    # VENTA: la MA corta pasa de estar por encima (o igual) a por debajo
    cruce_abajo = (diferencia < 0) & (diferencia.shift(1) >= 0)

    senales[cruce_arriba] = "COMPRA"
    senales[cruce_abajo] = "VENTA"

    return senales


def alertas_precio(precios: pd.Series, umbral_cambio: float = 5.0) -> List[Dict]:
    """
    Genera alertas cuando hay cambios significativos.
    """
    alertas = []

    # Rendimientos diarios (sin el primer NaN)
    rendimientos = calcular_rendimientos(precios).dropna()

    # Solo los días cuyo cambio absoluto supera el umbral
    significativos = rendimientos[rendimientos.abs() > umbral_cambio]

    for fecha, cambio in significativos.items():
        fecha_str = fecha.strftime('%Y-%m-%d') if hasattr(fecha, 'strftime') else str(fecha)
        alertas.append({
            "fecha": fecha_str,
            "tipo": "SUBIDA" if cambio > 0 else "CAIDA",
            "cambio": float(cambio)
        })

    return alertas


def clasificar_volatilidad(rendimientos: pd.Series) -> str:
    """
    Clasifica el nivel de volatilidad del activo.
    """
    # Volatilidad = desviación estándar de los rendimientos (ignorando NaN)
    volatilidad = rendimientos.dropna().std()

    if volatilidad < 1:
        return "BAJA"
    elif volatilidad < 3:
        return "MEDIA"
    elif volatilidad < 5:
        return "ALTA"
    else:
        return "MUY ALTA"


def generar_reporte_completo(precios: pd.Series, nombre_accion: str) -> Dict:
    """
    Genera un reporte completo de análisis.
    """
    # Se reutilizan todas las funciones anteriores
    rendimientos = calcular_rendimientos(precios)
    senales = generar_senales_trading(precios)

    def fecha_str(f):
        return f.strftime('%Y-%m-%d') if hasattr(f, 'strftime') else str(f)

    reporte = {
        "nombre": nombre_accion,
        "periodo": {
            "inicio": fecha_str(precios.index[0]),
            "fin": fecha_str(precios.index[-1]),
            "dias": len(precios)
        },
        "estadisticas": estadisticas_basicas(precios),
        "rendimientos": analisis_rendimientos(rendimientos),
        "tendencia": clasificar_tendencia(precios),
        "volatilidad": clasificar_volatilidad(rendimientos),
        "senal_actual": senales.iloc[-1],
        "alertas_recientes": alertas_precio(precios)
    }

    return reporte


# Simular 60 días de precios de una acción
np.random.seed(42)  # Para reproducibilidad

# Generar fechas
fechas = pd.date_range(start='2024-01-01', periods=60, freq='B')  # B = días hábiles

# Generar precios con tendencia alcista y volatilidad
precio_inicial = 100
rendimientos_simulados = np.random.normal(0.002, 0.02, 60)  # Media 0.2%, std 2%
precios_simulados = precio_inicial * np.cumprod(1 + rendimientos_simulados)

# Crear Serie de precios
PRECIOS_ACCION = pd.Series(
    precios_simulados.round(2),
    index=fechas,
    name='ACME Corp'
)


# Datos adicionales para pruebas más completas
np.random.seed(123)

# Acción con alta volatilidad
rend_volatil = np.random.normal(0, 0.05, 60)  # 5% de volatilidad diaria
precios_volatil = 50 * np.cumprod(1 + rend_volatil)
ACCION_VOLATIL = pd.Series(
    precios_volatil.round(2),
    index=fechas,
    name='VolatilTech'
)

# Acción con tendencia bajista
rend_bajista = np.random.normal(-0.005, 0.015, 60)  # Tendencia negativa
precios_bajista = 200 * np.cumprod(1 + rend_bajista)
ACCION_BAJISTA = pd.Series(
    precios_bajista.round(2),
    index=fechas,
    name='DeclineCorp'
)


def mostrar_reporte(reporte: Dict) -> None:
    """Muestra el reporte de forma legible."""
    print("=" * 70)
    print(f"           REPORTE DE ANÁLISIS: {reporte['nombre']}")
    print("=" * 70)
    
    # Período
    periodo = reporte.get('periodo', {})
    print(f"\n📅 PERÍODO DE ANÁLISIS")
    print("-" * 40)
    print(f"Inicio: {periodo.get('inicio', 'N/A')}")
    print(f"Fin: {periodo.get('fin', 'N/A')}")
    print(f"Días analizados: {periodo.get('dias', 'N/A')}")
    
    # Estadísticas
    stats = reporte.get('estadisticas', {})
    print(f"\n📊 ESTADÍSTICAS DE PRECIO")
    print("-" * 40)
    print(f"Precio actual:  ${stats.get('precio_actual', 0):,.2f}")
    print(f"Precio mínimo:  ${stats.get('precio_minimo', 0):,.2f}")
    print(f"Precio máximo:  ${stats.get('precio_maximo', 0):,.2f}")
    print(f"Precio promedio: ${stats.get('precio_promedio', 0):,.2f}")
    
    # Rendimientos
    rend = reporte.get('rendimientos', {})
    print(f"\n📈 RENDIMIENTO")
    print("-" * 40)
    print(f"Rendimiento total: {rend.get('rendimiento_total', 0):+.2f}%")
    print(f"Rendimiento promedio diario: {rend.get('rendimiento_promedio', 0):+.3f}%")
    if rend.get('mejor_dia'):
        print(f"Mejor día: {rend['mejor_dia'][0]} ({rend['mejor_dia'][1]:+.2f}%)")
    if rend.get('peor_dia'):
        print(f"Peor día: {rend['peor_dia'][0]} ({rend['peor_dia'][1]:+.2f}%)")
    print(f"Días positivos: {rend.get('dias_positivos', 0)}")
    print(f"Días negativos: {rend.get('dias_negativos', 0)}")
    
    # Indicadores
    print(f"\n🎯 INDICADORES")
    print("-" * 40)
    print(f"Tendencia: {reporte.get('tendencia', 'N/A')}")
    print(f"Volatilidad: {reporte.get('volatilidad', 'N/A')}")
    print(f"Señal actual: {reporte.get('senal_actual', 'N/A')}")
    
    # Alertas
    alertas = reporte.get('alertas_recientes', [])
    if alertas:
        print(f"\n⚠️ ALERTAS RECIENTES")
        print("-" * 40)
        for alerta in alertas[-5:]:  # Últimas 5
            emoji = "🔺" if alerta['tipo'] == 'SUBIDA' else "🔻"
            print(f"{emoji} {alerta['fecha']}: {alerta['tipo']} de {alerta['cambio']:+.2f}%")
    
    print("\n" + "=" * 70)


def visualizar_precios_texto(precios: pd.Series, ancho: int = 50) -> None:
    """Visualización simple de precios en texto (ASCII chart)."""
    min_precio = precios.min()
    max_precio = precios.max()
    rango = max_precio - min_precio
    
    print(f"\nGráfico de precios: {precios.name}")
    print(f"Max: ${max_precio:.2f}")
    print("-" * (ancho + 10))
    
    # Mostrar cada 3 días para no saturar
    for fecha, precio in precios.iloc[::3].items():
        posicion = int((precio - min_precio) / rango * ancho) if rango > 0 else ancho // 2
        barra = " " * posicion + "█"
        fecha_str = fecha.strftime('%m/%d') if hasattr(fecha, 'strftime') else str(fecha)[:5]
        print(f"{fecha_str} |{barra}")
    
    print("-" * (ancho + 10))
    print(f"Min: ${min_precio:.2f}")


# Prueba de funciones individuales
print("PRUEBA DE FUNCIONES INDIVIDUALES")
print("=" * 50)

# Estadísticas básicas
print("\n-- Estadísticas Básicas --")
stats = estadisticas_basicas(PRECIOS_ACCION)
print(stats)

# Rendimientos
print("\n-- Rendimientos (primeros 5) --")
rendimientos = calcular_rendimientos(PRECIOS_ACCION)
print(rendimientos.head())

# Análisis de rendimientos
print("\n-- Análisis de Rendimientos --")
analisis = analisis_rendimientos(rendimientos)
print(analisis)


# Prueba de indicadores técnicos
print("\n-- Media Móvil (5 días) --")
ma5 = media_movil(PRECIOS_ACCION, 5)
print(ma5.tail())

print("\n-- Bandas de Bollinger --")
bandas = bandas_bollinger(PRECIOS_ACCION, 20, 2)
for nombre, serie in bandas.items():
    if serie is not None:
        print(f"{nombre}: {serie.iloc[-1]:.2f}")

print("\n-- Tendencia --")
tendencia = clasificar_tendencia(PRECIOS_ACCION)
print(f"Tendencia actual: {tendencia}")


# Prueba del reporte completo
print("\nGENERANDO REPORTE COMPLETO...\n")
reporte = generar_reporte_completo(PRECIOS_ACCION, "ACME Corp")
mostrar_reporte(reporte)


# Comparar las tres acciones
print("\n" + "=" * 70)
print("         COMPARACIÓN DE ACCIONES")
print("=" * 70)

acciones = [
    (PRECIOS_ACCION, "ACME Corp"),
    (ACCION_VOLATIL, "VolatilTech"),
    (ACCION_BAJISTA, "DeclineCorp")
]

for precios, nombre in acciones:
    rendimientos = calcular_rendimientos(precios)
    if rendimientos is not None:
        rend_total = rendimientos.sum() if not rendimientos.isna().all() else 0
        volatilidad = clasificar_volatilidad(rendimientos)
        tendencia = clasificar_tendencia(precios)
        
        print(f"\n{nombre}:")
        print(f"  Rendimiento: {rend_total:+.2f}%")
        print(f"  Volatilidad: {volatilidad}")
        print(f"  Tendencia: {tendencia}")


def calcular_rsi(precios: pd.Series, periodos: int = 14) -> pd.Series:
    """
    Calcula el RSI (Relative Strength Index).

    RSI = 100 - (100 / (1 + RS))
    RS = Promedio de ganancias / Promedio de pérdidas

    Interpretación:
    - RSI > 70: Sobrecomprado (posible caída)
    - RSI < 30: Sobrevendido (posible subida)
    """
    # Cambio diario de precio
    delta = precios.diff()

    # Separar ganancias (positivos) y pérdidas (valor absoluto de los negativos)
    ganancias = delta.clip(lower=0)
    perdidas = -delta.clip(upper=0)

    # Promedios móviles de ganancias y pérdidas
    avg_ganancia = ganancias.rolling(window=periodos).mean()
    avg_perdida = perdidas.rolling(window=periodos).mean()

    # RS y RSI
    rs = avg_ganancia / avg_perdida
    rsi = 100 - (100 / (1 + rs))

    return rsi


def backtest_estrategia(precios: pd.Series, senales: pd.Series, capital_inicial: float = 10000) -> Dict:
    """
    Simula la estrategia de trading y calcula rendimiento.

    Estrategia: comprar todo el capital en una señal COMPRA y vender
    toda la posición en una señal VENTA.
    """
    capital = capital_inicial   # efectivo disponible
    acciones = 0.0              # número de acciones en cartera
    en_posicion = False
    precio_compra = 0.0

    num_operaciones = 0         # operaciones de compra realizadas
    operaciones_ganadoras = 0   # ventas con precio mayor al de compra

    for fecha in precios.index:
        senal = senales.loc[fecha]
        precio = precios.loc[fecha]

        if senal == "COMPRA" and not en_posicion:
            # Invertir todo el efectivo en acciones
            acciones = capital / precio
            capital = 0.0
            en_posicion = True
            precio_compra = precio
            num_operaciones += 1

        elif senal == "VENTA" and en_posicion:
            # Liquidar la posición
            capital = acciones * precio
            acciones = 0.0
            en_posicion = False
            if precio > precio_compra:
                operaciones_ganadoras += 1

    # Valor final = efectivo + valor de mercado de las acciones aún en cartera
    capital_final = capital + acciones * precios.iloc[-1]
    rendimiento_total = (capital_final / capital_inicial - 1) * 100

    return {
        "capital_final": float(capital_final),
        "rendimiento_total": float(rendimiento_total),
        "num_operaciones": int(num_operaciones),
        "operaciones_ganadoras": int(operaciones_ganadoras)
    }
