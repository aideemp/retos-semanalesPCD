# Reto semana 10
# Analizador de acciones bursátiles
Analizador de precios de acciones usando **Pandas Series**. Calcula estadísticas, rendimientos, medias móviles, indicadores técnicos y señales de trading a partir de series temporales de precios.

---

## Estructura del proyecto

```
reto-semana-10/
├── reto_10_analizador_acciones.ipynb   # Notebook con la solución completa
└── README.md
```

---

## Conceptos aplicados

| Tema | Funciones / técnicas |
|------|----------------------|
| Estadística de Series | `min`, `max`, `mean`, `median`, `std` |
| Rendimientos | `pct_change`, `diff` |
| Ventanas móviles | `rolling().mean()/.std()/.max()/.min()` |
| Indicadores técnicos | Bandas de Bollinger, medias móviles, RSI |
| Señales | cruces de medias (`shift`), clasificación de tendencia |
| Índices | `idxmax`, `idxmin`, `iloc` |

---

## Funciones implementadas

```python
estadisticas_basicas(precios)        # precio actual, mín, máx, promedio, mediana, std, rango
calcular_rendimientos(precios)       # rendimiento diario en %
analisis_rendimientos(rendimientos)  # mejor/peor día, días positivos/negativos, volatilidad
media_movil(precios, ventana)        # media móvil simple
bandas_bollinger(precios, ...)       # banda superior, media e inferior
detectar_maximos_minimos(precios)    # máximos y mínimos locales
clasificar_tendencia(precios, ma)    # ALCISTA / BAJISTA / LATERAL
generar_senales_trading(ma_c, ma_l)  # COMPRA / VENTA / MANTENER
alertas_precio(rendimientos, umbral) # alertas de subida/caída
clasificar_volatilidad(std)          # BAJA / MEDIA / ALTA / MUY ALTA
generar_reporte_completo(...)        # reporte integrado de la acción
```

### Bonus

```python
calcular_rsi(precios)                # Índice de Fuerza Relativa
backtest_estrategia(precios, ...)    # simulación de estrategia de trading
```

---

## Cómo ejecutar

1. Abrir `reto_10_analizador_acciones.ipynb` en Jupyter Notebook o JupyterLab.
2. Seleccionar **Kernel → Restart & Run All**.
3. Verificar que todas las celdas se ejecuten sin errores y muestren los resultados.
