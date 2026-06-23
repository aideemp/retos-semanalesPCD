# Reto Semana 3: Analizador de Ventas

## Descripción
Programa que lee transacciones de ventas en formato CSV y genera un reporte consolidado por producto, ordenado por ingreso total de mayor a menor.

## Uso
```bash
python main.py < entrada.txt
```

## Formato de Entrada
Archivo CSV con las columnas:
- `fecha` — Fecha de la venta (YYYY-MM-DD)
- `producto` — Nombre del producto
- `cantidad` — Unidades vendidas
- `precio_unitario` — Precio por unidad

## Formato de Salida
Archivo CSV con las columnas:
- `producto` — Nombre del producto
- `unidades_vendidas` — Total de unidades vendidas
- `ingreso_total` — Ingreso total con 2 decimales
- `precio_promedio` — Precio promedio con 2 decimales

## Ejemplo

Entrada: fecha,producto,cantidad,precio_unitario
2026-01-01,Laptop,2,15000.00
2026-01-02,Mouse,10,250.00
2026-01-03,Laptop,1,14500.00

Salida:
producto,unidades_vendidas,ingreso_total,precio_promedio
Laptop,3,44500.00,14833.33
Mouse,10,2500.00,250.00

## Reglas
- Se ignoran líneas con datos inválidos o incompletos
- El reporte se ordena por ingreso total de mayor a menor
- Los valores monetarios se muestran con 2 decimales

## Tecnologías
- Python 3
- Módulo `sys` para leer desde stdin
- Diccionarios para agrupar datos por producto


## Autor
Molina Palmas Sandra Aide