# Reto semana 08
# Métricas de sensores ambientales
Análisis de datos de una red de sensores ambientales usando **NumPy**. Se trabaja con arreglos tridimensionales (estaciones × días × horas) que registran temperatura, humedad y CO2, incluyendo valores faltantes (`NaN`).

---

## Estructura del proyecto

```
reto-semana-08/
├── reto_08_metricas_sensores.ipynb   # Notebook con la solución completa
└── README.md
```

---

## Conceptos aplicados

| Tema | Funciones / técnicas |
|------|----------------------|
| Atributos de arreglos | `ndim`, `shape`, `size`, `dtype`, `nbytes` |
| Indexación y slicing | acceso por índice, rangos, pasos, inversión de ejes |
| Estadística con nulos | `nanmean`, `nanstd`, `nanmax`, `nanmin` |
| Agregación por ejes | parámetro `axis` (por estación, día, hora) |
| Operaciones vectorizadas | conversión de unidades, normalización, broadcasting |
| Máscaras booleanas | detección de anomalías, conteos condicionales |

---

## Secciones resueltas

- **Atributos del arreglo**: dimensiones, forma, tamaño y memoria de los datos.
- **Indexación**: lecturas puntuales y por estación/día/hora.
- **Slicing**: ventanas horarias, subconjuntos de estaciones y reordenamientos.
- **Estadísticas globales**: media, máximo, mínimo y desviación ignorando `NaN`.
- **Agregaciones por eje**: promedios por estación, por día y por hora.
- **Transformaciones**: Celsius → Fahrenheit / Kelvin y normalización.
- **Índices y máscaras**: índice de confort térmico, anomalías y análisis de contingencia.
- **Rankings**: estaciones más cálidas/frías con `argmax`/`argmin` y conteo de `NaN`.

---

## Cómo ejecutar

1. Abrir `reto_08_metricas_sensores.ipynb` en Jupyter Notebook o JupyterLab.
2. Seleccionar **Kernel → Restart & Run All**.
3. Verificar que todas las celdas se ejecuten sin errores y muestren los resultados.
