# Reto semana 09
# Detector de anomalías financieras
Sistema de detección de transacciones anómalas (posible fraude) usando **NumPy**. Se aplican métodos estadísticos para identificar montos atípicos a partir de una matriz de transacciones por cuenta.

---

## Estructura del proyecto

```
reto-semana-09/
├── reto_09_detector_anomalias.ipynb   # Notebook con la solución completa
└── README.md
```

---

## Conceptos aplicados

| Tema | Funciones / técnicas |
|------|----------------------|
| Estadística descriptiva | `mean`, `median`, `std`, `min`, `max` |
| Cuartiles e IQR | `percentile`, rango intercuartílico (Q3 − Q1) |
| Regla de Tukey | límites `Q1 − 1.5·IQR` y `Q3 + 1.5·IQR` |
| Z-score | estandarización y umbral de desviaciones |
| Máscaras booleanas | filtrado de valores atípicos |
| Operaciones de conjuntos | intersección y unión de anomalías |
| Correlación | `corrcoef` entre cuentas |

---

## Secciones resueltas

- **Estadísticas básicas**: medidas de tendencia central y dispersión de los montos.
- **Cuartiles e IQR**: cálculo de percentiles 25/50/75 y rango intercuartílico.
- **Método IQR**: límites inferior y superior y detección de outliers.
- **Método Z-score**: estandarización y detección por umbral de desviaciones.
- **Comparación de métodos**: intersección y unión de los outliers detectados.
- **Matriz de correlación**: relación entre los patrones de gasto de las cuentas.

---

## Cómo ejecutar

1. Abrir `reto_09_detector_anomalias.ipynb` en Jupyter Notebook o JupyterLab.
2. Seleccionar **Kernel → Restart & Run All**.
3. Verificar que todas las celdas se ejecuten sin errores y muestren los resultados.
