import json
from datetime import datetime
import random

def cargar_tasas(ruta):
    with open(ruta, "r") as archivo:
        return json.load(archivo)

# Convierte el valor a otra moneda
def convertir(precio_usd, moneda_destino, tasas):
    # Obtiene la tasa de cambio de dólares a moneda de destino
    tasa = tasas["USD"].get(moneda_destino)
    
    # Si la moneda de destino no existe, lanza una excepción
    if not tasa:
        raise ValueError("Moneda no soportada")
    
    # Redondeamos el resultado de la conversión a 2 decimales
    return round(precio_usd * tasa, 2)

# Escribe una nueva línea en el archivo de registro
def registrar_transaccion(producto, precio_convertido, moneda, ruta_log):
    with open(ruta_log, "a") as archivo:
        # Obtiene la fecha y hora actual en formato YYYY-MM-DD HH:MM:SS
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Escribe una línea nueva en el archivo de registro
        archivo.write(f"{fecha} | {producto}: {precio_convertido:.2f} {moneda}\n")

def actualizar_tasas(ruta):
    # Simular API: Cambiar tasas aleatoriamente ±2%
    with open(ruta, "r+") as archivo:
        tasas = json.load(archivo)
        for moneda in tasas["USD"]:
            # Redondeamos las tasas a 2 decimales al ser actualizadas
            tasas["USD"][moneda] = round(tasas["USD"][moneda] * (0.98 + (0.04 * random.random())), 2)
        tasas["actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.seek(0)
        json.dump(tasas, archivo, indent=2)
        archivo.truncate()

# Ejemplo de uso
if __name__ == "__main__":
    #Actualizar las tasas
    actualizar_tasas("data/tasas.json")
    tasas = cargar_tasas("data/tasas.json")
    precio_usd = 100.00
    precio_eur = convertir(precio_usd, "EUR", tasas)
    registrar_transaccion("Laptop", precio_eur, "EUR", "./logs/historial.txt")
