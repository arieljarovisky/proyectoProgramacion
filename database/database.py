import os

ARCHIVO_DB = "movimientos.txt"

def inicializar_archivo():
    if not os.path.exists(ARCHIVO_DB):
        with open(ARCHIVO_DB, "w") as f:
            f.write("Tipo,Monto,Descripcion\n")

def registrar_movimiento(tipo, monto, descripcion):
    with open(ARCHIVO_DB, "a") as f:
        f.write(f"{tipo},{monto},{descripcion}\n")

def calcular_saldo():
    saldo = 0
    with open(ARCHIVO_DB, "r") as f:
        next(f)  # Saltar encabezado
        for linea in f:
            tipo, monto, _ = linea.strip().split(",")
            if tipo == "ingreso":
                saldo += float(monto)
            elif tipo == "egreso":
                saldo -= float(monto)
    return saldo

def obtener_movimientos():
    movimientos = []
    with open(ARCHIVO_DB, "r") as f:
        next(f)  # Saltar encabezado
        for linea in f:
            tipo, monto, descripcion = linea.strip().split(",")
            movimientos.append({"tipo": tipo, "monto": float(monto), "descripcion": descripcion})
    return movimientos
