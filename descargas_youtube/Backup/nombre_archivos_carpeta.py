import os

carpeta = "/media/jose/90980D73980D58DC/PAPA/Música/Descargas de YouTube"

# Cancion a comparar (string)
cancion_titulo = "cancion dos"

archivos = os.listdir(carpeta)

# Eliminar la extensión de cada archivo - Lista de canciones (strings)
canciones_lista = [os.path.splitext(archivo)[0] for archivo in archivos]

print(f"Estos son los titulos de las canciones: \n{canciones_lista}")

# Verificar si el string está en la lista
if cancion_titulo in canciones_lista:
    print(f"¡Coincidencia encontrada para '{cancion_titulo}'!")
else:
    print(f"No se encontró ninguna coincidencia para '{cancion_titulo}'.")
