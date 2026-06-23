"""Funciones de validación para los datos del inventario."""

def validar_sku(sku):
    """Valida que el SKU no esté vacío."""
    if not sku or not str(sku).strip():
        return False
    return True


def validar_precio(precio):
    """Valida que el precio sea un número >= 0."""
    try:
        return float(precio) >= 0
    except (ValueError, TypeError):
        return False


def validar_stock(stock):
    """Valida que el stock sea un entero >= 0."""
    try:
        return int(stock) >= 0
    except (ValueError, TypeError):
        return False


def validar_producto(sku, nombre, categoria, precio, stock, stock_minimo):
    """
    Valida todos los campos de un producto.

    Returns:
        tuple: (es_valido: bool, mensaje_error: str o None)
    """
    if not validar_sku(sku):
        return False, "SKU vacío o inválido"
    if not nombre or not str(nombre).strip():
        return False, "Nombre vacío"
    if not validar_precio(precio):
        return False, f"Precio inválido: {precio}"
    if not validar_stock(stock):
        return False, f"Stock inválido: {stock}"
    if not validar_stock(stock_minimo):
        return False, f"Stock mínimo inválido: {stock_minimo}"
    return True, None