# Reto semana 12
# Analizador de plataforma de streaming musical
Análisis de datos de la plataforma ficticia **SoundWave** usando **Pandas avanzado**. Combina, agrupa y resume datos de artistas, canciones, usuarios y streams para generar un reporte ejecutivo.

---

## Estructura del proyecto

```
reto-semana-12/
├── reto_12_analizador_streaming.ipynb   # Notebook con la solución completa
└── README.md
```

---

## Conceptos aplicados

| Tema | Funciones / técnicas |
|------|----------------------|
| Combinar datos | `pd.concat()` para apilar streams mensuales |
| Joins | `pd.merge()` entre streams, canciones, artistas y usuarios |
| Agregaciones | `groupby().agg()`, `size`, `nunique` |
| Tablas dinámicas | `pivot_table()` por género/país y mes/tipo de cuenta |
| Reformado | `melt()` de formato ancho a largo |

---

## Ejercicios resueltos

- **Parte 1 (concat)**: unificación de los streams de Enero y Febrero.
- **Parte 2 (merge)**: enriquecimiento con datos de canciones, artistas y usuarios; comparación Premium vs Free.
- **Parte 3 (groupby)**: top de artistas, estadísticas por género y evolución por país y mes.
- **Parte 4 (pivot_table)**: matriz de streams por género y país, engagement por mes y tipo de cuenta.
- **Parte 5 (melt) — Bonus**: conversión de la matriz a formato largo para visualización.
- **Desafío final**: reporte ejecutivo con top de canciones, género líder, país líder, comparación Premium/Free y artista con mayor crecimiento.

---

## Cómo ejecutar

1. Abrir `reto_12_analizador_streaming.ipynb` en Jupyter Notebook o JupyterLab.
2. Seleccionar **Kernel → Restart & Run All**.
3. Verificar que todas las celdas se ejecuten sin errores y muestren los resultados.
