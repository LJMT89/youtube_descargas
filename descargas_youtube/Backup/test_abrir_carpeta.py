import subprocess

def abrir_nemo_carpeta(ruta_carpeta):
    try:
        subprocess.Popen(["nemo", ruta_carpeta])
    except Exception as e:
        print(f"Error al abrir la carpeta en Nemo: {str(e)}")

# Llamar a la función para abrir la carpeta en Nemo
abrir_nemo_carpeta("/media/jose/90980D73980D58DC/PAPA/Música/Descargas de YouTube")
