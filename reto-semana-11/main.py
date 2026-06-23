import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime


# PARTE 1: Carga y Exploración de Datos

def cargar_datos() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Carga los datos de estudiantes, calificaciones y materias.
    """
    # Datos de estudiantes
    estudiantes = pd.DataFrame({
        'boleta': ['2021630001', '2021630002', '2021630003', '2021630004', '2021630005',
                   '2022630001', '2022630002', '2022630003', '2022630004', '2022630005',
                   '2023630001', '2023630002', '2023630003', '2023630004', '2023630005'],
        'nombre': ['Juan Pérez García', 'María López Ruiz', 'Pedro Sánchez Torres',
                   'Ana Martínez Díaz', 'Luis Rodríguez Vega', 'Carmen Flores Luna',
                   'Roberto Díaz Mora', 'Laura Torres Silva', 'Diego Ramírez Cruz',
                   'Sofía Vargas Romo', 'Carlos Mendoza Ríos', 'Patricia Ortiz León',
                   'Miguel Ángel Castro', 'Fernanda Reyes Paz', 'Andrés Guzmán Villa'],
        'semestre': [4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2],
        'carrera': ['CD'] * 15,
        'email': ['juan.perez@ipn.mx', 'maria.lopez@ipn.mx', 'pedro.sanchez@ipn.mx',
                  'ana.martinez@ipn.mx', 'luis.rodriguez@ipn.mx', 'carmen.flores@ipn.mx',
                  'roberto.diaz@ipn.mx', 'laura.torres@ipn.mx', 'diego.ramirez@ipn.mx',
                  'sofia.vargas@ipn.mx', 'carlos.mendoza@ipn.mx', 'patricia.ortiz@ipn.mx',
                  'miguel.castro@ipn.mx', 'fernanda.reyes@ipn.mx', 'andres.guzman@ipn.mx']
    })
    
    # Datos de materias
    materias = pd.DataFrame({
        'materia_id': ['MAT101', 'MAT102', 'PROG101', 'PROG102', 'EST101', 'EST102', 'BD101'],
        'nombre': ['Cálculo Diferencial', 'Cálculo Integral', 'Programación I',
                   'Programación II', 'Probabilidad', 'Estadística Inferencial',
                   'Bases de Datos'],
        'creditos': [8, 8, 6, 6, 6, 6, 6],
        'semestre_materia': [1, 2, 1, 2, 2, 3, 3]
    })
    
    # Generar calificaciones (simuladas)
    np.random.seed(42)
    calificaciones_data = []
    
    for boleta in estudiantes['boleta']:
        semestre = estudiantes[estudiantes['boleta'] == boleta]['semestre'].values[0]
        materias_cursadas = materias[materias['semestre_materia'] <= semestre]['materia_id'].tolist()
        
        for materia in materias_cursadas:
            # Generar calificaciones aleatorias (con algunos casos especiales)
            base = np.random.uniform(5, 10)
            p1 = round(min(10, max(0, base + np.random.normal(0, 1))), 1)
            p2 = round(min(10, max(0, base + np.random.normal(0, 1))), 1)
            final = round(min(10, max(0, base + np.random.normal(0, 0.5))), 1)
            
            # Algunos valores nulos aleatorios
            if np.random.random() < 0.05:
                p2 = np.nan
            
            calificaciones_data.append({
                'boleta': boleta,
                'materia_id': materia,
                'parcial_1': p1,
                'parcial_2': p2,
                'final': final
            })
    
    calificaciones = pd.DataFrame(calificaciones_data)
    
    return estudiantes, calificaciones, materias


def info_general(df_estudiantes: pd.DataFrame, df_calificaciones: pd.DataFrame) -> Dict:
    """
    Genera información general del sistema.
    """
    resultado = {
        # Número de estudiantes registrados
        "total_estudiantes": int(len(df_estudiantes)),
        # Número de registros de calificaciones (una fila = un estudiante-materia)
        "total_registros_calif": int(len(df_calificaciones)),
        # Lista ordenada de semestres presentes
        "semestres": sorted(df_estudiantes['semestre'].unique().tolist()),
        # Materias distintas que tienen al menos un registro de calificación
        "materias_con_registros": int(df_calificaciones['materia_id'].nunique())
    }

    return resultado


def validar_datos(df_calificaciones: pd.DataFrame) -> Dict:
    """
    Valida la integridad de los datos.
    """
    # Columnas de calificación a revisar
    cols = ['parcial_1', 'parcial_2', 'final']

    # Filas que tienen al menos un valor nulo en alguna calificación
    registros_con_nulos = int(df_calificaciones[cols].isna().any(axis=1).sum())

    # Filas con alguna calificación fuera del rango válido [0, 10]
    # (las comparaciones con NaN dan False, por lo que no afectan el conteo)
    fuera = (df_calificaciones[cols] < 0) | (df_calificaciones[cols] > 10)
    calificaciones_fuera_rango = int(fuera.any(axis=1).sum())

    resultado = {
        "registros_con_nulos": registros_con_nulos,
        "calificaciones_fuera_rango": calificaciones_fuera_rango,
        # Los datos son válidos solo si no hay nulos ni valores fuera de rango
        "datos_validos": bool(registros_con_nulos == 0 and calificaciones_fuera_rango == 0)
    }

    return resultado


# PARTE 2: Consultas y Filtros

def buscar_estudiante(df_estudiantes: pd.DataFrame, criterio: str, valor: str) -> pd.DataFrame:
    """
    Busca estudiantes por diferentes criterios.
    """
    if criterio == 'nombre':
        # Búsqueda parcial e insensible a mayúsculas
        mask = df_estudiantes['nombre'].str.contains(valor, case=False, na=False)
        return df_estudiantes[mask]
    elif criterio == 'boleta':
        # Búsqueda exacta por boleta
        return df_estudiantes[df_estudiantes['boleta'] == valor]
    elif criterio == 'semestre':
        # El semestre es entero, convertimos el valor recibido
        return df_estudiantes[df_estudiantes['semestre'] == int(valor)]
    else:
        # Criterio no reconocido: devolvemos un DataFrame vacío
        return df_estudiantes.iloc[0:0]


def obtener_kardex(boleta: str, df_estudiantes: pd.DataFrame,
                   df_calificaciones: pd.DataFrame, df_materias: pd.DataFrame) -> Dict:
    """
    Obtiene el kardex completo de un estudiante.
    """
    resultado = {
        "estudiante": None,
        "materias": None,
        "promedio_general": None,
        "creditos_cursados": None,
        "materias_aprobadas": None,
        "materias_reprobadas": None
    }

    # 1. Datos del estudiante (si no existe, se devuelve el resultado vacío)
    est = df_estudiantes[df_estudiantes['boleta'] == boleta]
    if est.empty:
        return resultado
    resultado['estudiante'] = est.iloc[0].to_dict()

    # 2. Calificaciones del estudiante unidas con el nombre/créditos de la materia
    califs = df_calificaciones[df_calificaciones['boleta'] == boleta].merge(
        df_materias[['materia_id', 'nombre', 'creditos']], on='materia_id', how='left'
    )

    # 3. Promedio por materia: media de los 3 parciales ignorando nulos
    califs['promedio'] = califs[['parcial_1', 'parcial_2', 'final']].mean(axis=1).round(2)

    # 4. Tabla de materias para mostrar en el kardex
    resultado['materias'] = califs[['materia_id', 'nombre', 'parcial_1',
                                    'parcial_2', 'final', 'promedio']]

    # 5. Métricas agregadas del estudiante
    resultado['promedio_general'] = round(float(califs['promedio'].mean()), 2)
    resultado['creditos_cursados'] = int(califs['creditos'].sum())
    resultado['materias_aprobadas'] = int((califs['promedio'] >= 6.0).sum())
    resultado['materias_reprobadas'] = int((califs['promedio'] < 6.0).sum())

    return resultado


def filtrar_por_rendimiento(df_calificaciones: pd.DataFrame,
                            df_estudiantes: pd.DataFrame,
                            min_promedio: float = None,
                            max_promedio: float = None) -> pd.DataFrame:
    """
    Filtra estudiantes por rango de promedio.
    """
    # 1. Promedio por materia y luego promedio general por estudiante
    calif = df_calificaciones.copy()
    calif['promedio'] = calif[['parcial_1', 'parcial_2', 'final']].mean(axis=1)
    prom = calif.groupby('boleta')['promedio'].mean().round(2).reset_index()

    # 2. Aplicar filtros de cota inferior y superior según se reciban
    if min_promedio is not None:
        prom = prom[prom['promedio'] >= min_promedio]
    if max_promedio is not None:
        prom = prom[prom['promedio'] <= max_promedio]

    # 3. Unir con datos del estudiante y ordenar de mayor a menor promedio
    resultado = prom.merge(df_estudiantes[['boleta', 'nombre', 'semestre']], on='boleta')
    return resultado[['boleta', 'nombre', 'semestre', 'promedio']] \
        .sort_values('promedio', ascending=False).reset_index(drop=True)


# PARTE 3: Cálculos y Estadísticas

def calcular_promedio_materia(df_calificaciones: pd.DataFrame, materia_id: str) -> Dict:
    """
    Calcula estadísticas de una materia.
    """
    resultado = {
        "materia": materia_id,
        "inscritos": None,
        "promedio_parcial1": None,
        "promedio_parcial2": None,
        "promedio_final": None,
        "promedio_general": None,
        "tasa_aprobacion": None,
        "calificacion_maxima": None,
        "calificacion_minima": None
    }

    # Registros de la materia solicitada
    mat = df_calificaciones[df_calificaciones['materia_id'] == materia_id]
    if mat.empty:
        return resultado

    # Promedio por estudiante en esta materia (media de los 3 parciales)
    prom_materia = mat[['parcial_1', 'parcial_2', 'final']].mean(axis=1)

    resultado['inscritos'] = int(len(mat))
    resultado['promedio_parcial1'] = round(float(mat['parcial_1'].mean()), 2)
    resultado['promedio_parcial2'] = round(float(mat['parcial_2'].mean()), 2)
    resultado['promedio_final'] = round(float(mat['final'].mean()), 2)
    resultado['promedio_general'] = round(float(prom_materia.mean()), 2)
    # Porcentaje de estudiantes con promedio aprobatorio (>= 6)
    resultado['tasa_aprobacion'] = round(float((prom_materia >= 6.0).mean() * 100), 1)
    resultado['calificacion_maxima'] = round(float(prom_materia.max()), 2)
    resultado['calificacion_minima'] = round(float(prom_materia.min()), 2)

    return resultado


def ranking_estudiantes(df_calificaciones: pd.DataFrame,
                        df_estudiantes: pd.DataFrame,
                        top_n: int = 10) -> pd.DataFrame:
    """
    Genera ranking de mejores estudiantes por promedio.
    """
    # 1. Promedio por materia y promedio general por estudiante
    calif = df_calificaciones.copy()
    calif['promedio'] = calif[['parcial_1', 'parcial_2', 'final']].mean(axis=1)
    prom = calif.groupby('boleta')['promedio'].mean().round(2).reset_index()

    # 2-3. Unir con datos del estudiante, ordenar descendente y tomar top_n
    prom = prom.merge(df_estudiantes[['boleta', 'nombre', 'semestre']], on='boleta')
    prom = prom.sort_values('promedio', ascending=False).head(top_n).reset_index(drop=True)

    # 4. Agregar columna de posición (1, 2, 3, ...)
    prom.insert(0, 'Posición', range(1, len(prom) + 1))

    return prom[['Posición', 'nombre', 'semestre', 'promedio']].rename(
        columns={'nombre': 'Nombre', 'semestre': 'Semestre', 'promedio': 'Promedio'}
    )


def estadisticas_por_semestre(df_estudiantes: pd.DataFrame,
                              df_calificaciones: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula estadísticas agrupadas por semestre.
    """
    # Promedio por materia y semestre del estudiante al que pertenece
    calif = df_calificaciones.copy()
    calif['promedio'] = calif[['parcial_1', 'parcial_2', 'final']].mean(axis=1)
    calif = calif.merge(df_estudiantes[['boleta', 'semestre']], on='boleta')
    # Materia aprobada si su promedio es >= 6
    calif['aprobado'] = calif['promedio'] >= 6.0

    # Promedio general por estudiante (para contar alumnos y mejor/peor)
    prom_est = calif.groupby(['semestre', 'boleta'])['promedio'].mean().reset_index()

    stats = pd.DataFrame({
        'Estudiantes': prom_est.groupby('semestre')['boleta'].count(),
        'Promedio': prom_est.groupby('semestre')['promedio'].mean().round(2),
        # Tasa de aprobación a nivel materia dentro del semestre
        'Tasa Aprob.': (calif.groupby('semestre')['aprobado'].mean() * 100).round(1),
        'Mejor': prom_est.groupby('semestre')['promedio'].max().round(2),
        'Peor': prom_est.groupby('semestre')['promedio'].min().round(2),
    })
    stats.index.name = 'Semestre'

    return stats


# PARTE 4: Identificación de Riesgo y Reportes

def identificar_estudiantes_riesgo(df_calificaciones: pd.DataFrame,
                                   df_estudiantes: pd.DataFrame,
                                   umbral_promedio: float = 7.0,
                                   max_reprobadas: int = 2) -> pd.DataFrame:
    """
    Identifica estudiantes en riesgo académico.
    """
    # 1-2. Promedio general y número de materias reprobadas por estudiante
    calif = df_calificaciones.copy()
    calif['promedio'] = calif[['parcial_1', 'parcial_2', 'final']].mean(axis=1)
    agg = calif.groupby('boleta').agg(
        promedio=('promedio', 'mean'),
        reprobadas=('promedio', lambda x: int((x < 6.0).sum()))
    ).reset_index()
    agg['promedio'] = agg['promedio'].round(2)

    # 3. Criterios de riesgo: bajo promedio O demasiadas materias reprobadas
    bajo_promedio = agg['promedio'] < umbral_promedio
    muchas_reprobadas = agg['reprobadas'] > max_reprobadas
    riesgo = agg[bajo_promedio | muchas_reprobadas].copy()

    # 4. Determinar el motivo del riesgo para cada estudiante
    def _motivo(fila):
        b = fila['promedio'] < umbral_promedio
        m = fila['reprobadas'] > max_reprobadas
        if b and m:
            return 'Ambos'
        if m:
            return 'Mat. reprob.'
        return 'Bajo promedio'
    riesgo['motivo'] = riesgo.apply(_motivo, axis=1)

    # Unir con el nombre del estudiante y ordenar por promedio ascendente
    riesgo = riesgo.merge(df_estudiantes[['boleta', 'nombre']], on='boleta')
    return riesgo[['boleta', 'nombre', 'promedio', 'reprobadas', 'motivo']].rename(
        columns={'boleta': 'Boleta', 'nombre': 'Nombre', 'promedio': 'Promedio',
                 'reprobadas': 'Reprobadas', 'motivo': 'Motivo'}
    ).sort_values('Promedio').reset_index(drop=True)


def generar_reporte_academico(df_estudiantes: pd.DataFrame,
                              df_calificaciones: pd.DataFrame,
                              df_materias: pd.DataFrame) -> Dict:
    """
    Genera reporte académico completo.
    """
    reporte = {
        "resumen_general": {},
        "por_semestre": None,
        "por_materia": None,
        "mejores_estudiantes": None,
        "estudiantes_riesgo": None,
        "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Promedio por materia y promedio general por estudiante (para el resumen)
    calif = df_calificaciones.copy()
    calif['promedio'] = calif[['parcial_1', 'parcial_2', 'final']].mean(axis=1)
    prom_est = calif.groupby('boleta')['promedio'].mean()

    reporte['resumen_general'] = {
        'total_estudiantes': int(len(df_estudiantes)),
        'promedio_global': round(float(prom_est.mean()), 2),
        # Tasa de aprobación global a nivel materia
        'tasa_aprobacion': round(float((calif['promedio'] >= 6.0).mean() * 100), 1)
    }

    # Secciones del reporte reutilizando las funciones anteriores
    reporte['por_semestre'] = estadisticas_por_semestre(df_estudiantes, df_calificaciones)
    reporte['por_materia'] = pd.DataFrame(
        [calcular_promedio_materia(df_calificaciones, m) for m in df_materias['materia_id']]
    )
    reporte['mejores_estudiantes'] = ranking_estudiantes(df_calificaciones, df_estudiantes, top_n=5)
    reporte['estudiantes_riesgo'] = identificar_estudiantes_riesgo(df_calificaciones, df_estudiantes)

    return reporte


def exportar_kardex(boleta: str, kardex: Dict, formato: str = 'csv') -> str:
    """
    Exporta el kardex de un estudiante a archivo.
    """
    # Si el kardex no tiene estudiante, no hay nada que exportar
    if kardex.get('estudiante') is None:
        return ''

    # 1. Nombre de archivo con boleta y fecha
    fecha = datetime.now().strftime("%Y%m%d")

    if formato == 'csv':
        nombre_archivo = f"kardex_{boleta}_{fecha}.csv"
        # Se exporta la tabla de materias del estudiante
        kardex['materias'].to_csv(nombre_archivo, index=False, encoding='utf-8')
    elif formato == 'json':
        nombre_archivo = f"kardex_{boleta}_{fecha}.json"
        # Se arma un diccionario completo y serializable
        datos = {
            'estudiante': kardex['estudiante'],
            'materias': kardex['materias'].to_dict(orient='records'),
            'promedio_general': kardex['promedio_general'],
            'creditos_cursados': kardex['creditos_cursados'],
            'materias_aprobadas': kardex['materias_aprobadas'],
            'materias_reprobadas': kardex['materias_reprobadas'],
        }
        import json
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    else:
        raise ValueError(f"Formato no soportado: {formato}. Use 'csv' o 'json'.")

    return nombre_archivo


def mostrar_kardex(kardex: Dict) -> None:
    """Muestra el kardex de forma legible."""
    if kardex['estudiante'] is None:
        print("❌ Estudiante no encontrado")
        return
    
    est = kardex['estudiante']
    print("=" * 70)
    print("                         KARDEX ACADÉMICO")
    print("=" * 70)
    print(f"\n📋 DATOS DEL ESTUDIANTE")
    print("-" * 40)
    print(f"Boleta: {est.get('boleta', 'N/A')}")
    print(f"Nombre: {est.get('nombre', 'N/A')}")
    print(f"Semestre: {est.get('semestre', 'N/A')}")
    print(f"Carrera: {est.get('carrera', 'N/A')}")
    print(f"Email: {est.get('email', 'N/A')}")
    
    print(f"\n📚 CALIFICACIONES")
    print("-" * 70)
    if kardex['materias'] is not None and len(kardex['materias']) > 0:
        print(kardex['materias'].to_string(index=False))
    else:
        print("Sin calificaciones registradas")
    
    print(f"\n📊 RESUMEN")
    print("-" * 40)
    print(f"Promedio General: {kardex.get('promedio_general', 0):.2f}")
    print(f"Créditos Cursados: {kardex.get('creditos_cursados', 0)}")
    print(f"Materias Aprobadas: {kardex.get('materias_aprobadas', 0)}")
    print(f"Materias Reprobadas: {kardex.get('materias_reprobadas', 0)}")
    print("=" * 70)


def mostrar_reporte(reporte: Dict) -> None:
    """Muestra el reporte académico completo."""
    print("=" * 70)
    print("              REPORTE ACADÉMICO - CIENCIA DE DATOS")
    print(f"              Generado: {reporte['fecha_generacion']}")
    print("=" * 70)
    
    # Resumen general
    res = reporte.get('resumen_general', {})
    print(f"\n📊 RESUMEN GENERAL")
    print("-" * 40)
    print(f"Total de estudiantes: {res.get('total_estudiantes', 'N/A')}")
    print(f"Promedio global: {res.get('promedio_global', 0):.2f}")
    print(f"Tasa de aprobación: {res.get('tasa_aprobacion', 0):.1f}%")
    
    # Por semestre
    if reporte.get('por_semestre') is not None:
        print(f"\n📅 ESTADÍSTICAS POR SEMESTRE")
        print("-" * 40)
        print(reporte['por_semestre'].to_string())
    
    # Mejores estudiantes
    if reporte.get('mejores_estudiantes') is not None:
        print(f"\n🏆 TOP 5 ESTUDIANTES")
        print("-" * 40)
        print(reporte['mejores_estudiantes'].head().to_string(index=False))
    
    # Estudiantes en riesgo
    if reporte.get('estudiantes_riesgo') is not None and len(reporte['estudiantes_riesgo']) > 0:
        print(f"\n⚠️ ESTUDIANTES EN RIESGO ({len(reporte['estudiantes_riesgo'])})")
        print("-" * 40)
        print(reporte['estudiantes_riesgo'].to_string(index=False))
    else:
        print(f"\n✅ No hay estudiantes en riesgo académico")
    
    print("\n" + "=" * 70)


# Cargar datos
df_estudiantes, df_calificaciones, df_materias = cargar_datos()


# Prueba de información general
print("\nINFORMACIÓN GENERAL")
print("=" * 50)
info = info_general(df_estudiantes, df_calificaciones)
print(info)


# Prueba de validación
print("\nVALIDACIÓN DE DATOS")
print("=" * 50)
validacion = validar_datos(df_calificaciones)
print(validacion)


# Prueba de búsqueda
print("\nBÚSQUEDA DE ESTUDIANTES")
print("=" * 50)

print("\n-- Buscar por nombre 'María' --")
resultado = buscar_estudiante(df_estudiantes, 'nombre', 'María')
print(resultado)

print("\n-- Buscar por semestre 3 --")
resultado = buscar_estudiante(df_estudiantes, 'semestre', '3')
print(resultado)


# Prueba de kardex
print("\nKARDEX DE ESTUDIANTE")
print("=" * 50)
kardex = obtener_kardex('2021630001', df_estudiantes, df_calificaciones, df_materias)
mostrar_kardex(kardex)


# Prueba de ranking
print("\nRANKING DE ESTUDIANTES")
print("=" * 50)
ranking = ranking_estudiantes(df_calificaciones, df_estudiantes, top_n=5)
print(ranking)


# Prueba de reporte completo
print("\nREPORTE ACADÉMICO COMPLETO")
reporte = generar_reporte_academico(df_estudiantes, df_calificaciones, df_materias)
mostrar_reporte(reporte)


def predecir_riesgo_proximo_semestre(df_calificaciones: pd.DataFrame,
                                     df_estudiantes: pd.DataFrame) -> pd.DataFrame:
    """
    Predice estudiantes que podrían estar en riesgo el próximo semestre
    basándose en tendencias de calificaciones.

    Criterios:
    - Tendencia decreciente en parciales
    - Calificación final menor que parcial 1
    """
    calif = df_calificaciones.copy()
    # Materia con tendencia a la baja: el 2do parcial y el final caen respecto al 1ro
    calif['declive'] = (calif['parcial_2'] < calif['parcial_1']) & \
                       (calif['final'] < calif['parcial_1'])

    # Resumen por estudiante: cuántas materias muestran declive
    resumen = calif.groupby('boleta').agg(
        materias_en_declive=('declive', lambda x: int(x.sum())),
        total_materias=('materia_id', 'count')
    ).reset_index()
    resumen['proporcion_declive'] = (
        resumen['materias_en_declive'] / resumen['total_materias']
    ).round(2)

    # En riesgo de proyección: al menos una materia con tendencia decreciente
    resumen = resumen[resumen['materias_en_declive'] > 0]
    resumen = resumen.merge(df_estudiantes[['boleta', 'nombre']], on='boleta')

    return resumen[['boleta', 'nombre', 'materias_en_declive',
                    'total_materias', 'proporcion_declive']] \
        .sort_values('proporcion_declive', ascending=False).reset_index(drop=True)


def comparar_estudiantes(boleta1: str, boleta2: str,
                         df_calificaciones: pd.DataFrame,
                         df_estudiantes: pd.DataFrame,
                         df_materias: pd.DataFrame) -> Dict:
    """
    Compara el rendimiento de dos estudiantes.
    """
    # Reutilizamos el kardex de cada estudiante
    k1 = obtener_kardex(boleta1, df_estudiantes, df_calificaciones, df_materias)
    k2 = obtener_kardex(boleta2, df_estudiantes, df_calificaciones, df_materias)

    def _resumen(k):
        return {
            'nombre': k['estudiante']['nombre'],
            'promedio_general': k['promedio_general'],
            'materias_aprobadas': k['materias_aprobadas'],
            'materias_reprobadas': k['materias_reprobadas'],
        }

    r1, r2 = _resumen(k1), _resumen(k2)
    # Determinar quién tiene mejor promedio general
    mejor = r1['nombre'] if r1['promedio_general'] >= r2['promedio_general'] else r2['nombre']

    return {
        'estudiante_1': r1,
        'estudiante_2': r2,
        'diferencia_promedio': round(abs(r1['promedio_general'] - r2['promedio_general']), 2),
        'mejor_promedio': mejor
    }


# Pruebas de funciones adicionales (Parte 3 y 4)
print("\nPROMEDIO POR MATERIA (MAT101)")
print("=" * 50)
print(calcular_promedio_materia(df_calificaciones, 'MAT101'))

print("\nESTADÍSTICAS POR SEMESTRE")
print("=" * 50)
print(estadisticas_por_semestre(df_estudiantes, df_calificaciones))

print("\nFILTRAR POR RENDIMIENTO (promedio >= 8.0)")
print("=" * 50)
print(filtrar_por_rendimiento(df_calificaciones, df_estudiantes, min_promedio=8.0))

print("\nESTUDIANTES EN RIESGO")
print("=" * 50)
print(identificar_estudiantes_riesgo(df_calificaciones, df_estudiantes))


# Exportar un kardex (entregable) y probar funciones bonus
print("\nEXPORTAR KARDEX")
print("=" * 50)
kardex = obtener_kardex('2021630001', df_estudiantes, df_calificaciones, df_materias)
archivo_csv = exportar_kardex('2021630001', kardex, formato='csv')
archivo_json = exportar_kardex('2021630001', kardex, formato='json')
print(f"Kardex exportado a: {archivo_csv}")
print(f"Kardex exportado a: {archivo_json}")

print("\nBONUS: PREDICCIÓN DE RIESGO PRÓXIMO SEMESTRE")
print("=" * 50)
print(predecir_riesgo_proximo_semestre(df_calificaciones, df_estudiantes).head())

print("\nBONUS: COMPARACIÓN DE ESTUDIANTES")
print("=" * 50)
comparacion = comparar_estudiantes('2021630001', '2021630004',
                                   df_calificaciones, df_estudiantes, df_materias)
print(comparacion)
