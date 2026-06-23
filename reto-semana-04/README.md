# Sistema de Inventario Modular

## Descripcion
Sistema que genera reportes de productos que necesitan reorden.

## Estructura del Proyecto
reto_semana_04/
├── main.py
├── README.md
├── .gitignore
├── models/
│   ├── init.py
│   └── producto.py
├── utils/
│   ├── init.py
│   ├── io.py
│   └── validators.py
├── data/
│   └── inventario.csv
└── outputs/
└── reporte_inventario.csv

## Como Ejecutar
```bash
python main.py
```

## Entrada
Archivo `data/inventario.csv` con columnas: sku, nombre, categoria, precio, stock, stock_minimo.

## Salida
Archivo `outputs/reporte_inventario.csv` con productos que necesitan reorden, ordenados por unidades faltantes.

## Autor
Molina Palmas Sandra Aide