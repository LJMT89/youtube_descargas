import psutil

def verificar_nemo_abierto():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'nemo':
            return True  # Se encontró un proceso de Nemo en ejecución
    return False  # No se encontraron procesos de Nemo en ejecución

# Verificar si hay una instancia de Nemo abierta
nemo_abierto = verificar_nemo_abierto()

if nemo_abierto:
    print("Hay una instancia de Nemo abierta.")
else:
    print("No hay ninguna instancia de Nemo abierta.")
