# Reto semana 11
# Sistema de gestión de calificaciones
Gestor de calificaciones de estudiantes usando **Pandas DataFrames**. Permite consultar datos, calcular promedios, identificar estudiantes en riesgo y generar reportes académicos a partir de tres tablas: estudiantes, calificaciones y materias.

---

## Estructura del proyecto

```
reto-semana-11/
├── reto_11_gestor_estudiantes.ipynb   # Notebook con la solución completa
├── kardex_2021630001_*.csv            # Kardex exportado (entregable)
├── kardex_2021630001_*.json           # Kardex exportado (entregable)
└── README.md
```

---

## Conceptos aplicados

| Tema | Funciones / técnicas |
|------|----------------------|
| Combinar tablas | `merge()` entre estudiantes, calificaciones y materias |
| Agrupar y agregar | `groupby().agg()` por estudiante, materia y semestre |
| Filtrado | máscaras booleanas, `str.contains` |
| Manejo de nulos | `isna`, promedios que ignoran `NaN` |
| Exportación | `to_csv`, `to_json` |

---

## Funciones implementadas

### Parte 1 — Carga y exploración
```python
cargar_datos()          # → (df_estudiantes, df_calificaciones, df_materias)
info_general(...)       # totales, semestres y materias con registros
validar_datos(...)      # nulos y calificaciones fuera de rango
```

### Parte 2 — Consultas y filtros
```python
buscar_estudiante(...)        # por boleta, nombre (parcial) o semestre
obtener_kardex(...)           # kardex completo con promedios y créditos
filtrar_por_rendimiento(...)  # estudiantes por rango de promedio
```

### Parte 3 — Cálculos y estadísticas
```python
calcular_promedio_materia(...)    # estadísticas por materia
ranking_estudiantes(...)          # top N por promedio
estadisticas_por_semestre(...)    # agregaciones por semestre
```

### Parte 4 — Riesgo y reportes
```python
identificar_estudiantes_riesgo(...)  # criterios de bajo promedio / reprobadas
generar_reporte_academico(...)       # reporte integrado
exportar_kardex(...)                 # exporta a CSV o JSON
```

### Bonus
```python
predecir_riesgo_proximo_semestre(...)  # tendencia decreciente de calificaciones
comparar_estudiantes(...)              # comparación de dos estudiantes
```

---

## Cómo ejecutar

1. Abrir `reto_11_gestor_estudiantes.ipynb` en Jupyter Notebook o JupyterLab.
2. Seleccionar **Kernel → Restart & Run All**.
3. Verificar que todas las celdas se ejecuten sin errores y muestren los resultados.
4. Al ejecutarse, se generan los archivos de kardex en CSV y JSON.
