import tkinter as tk
import threading
import time
from tkinter import messagebox

# Función para simular un proceso que toma tiempo
def iniciar_proceso():
    time.sleep(15)  # Simulando un proceso que toma 15 segundos
    return "Proceso finalizado"

# Función para actualizar la barra de progreso
def actualizar_barra_progreso():
    while proceso_activo:
        for i in range(1, 11):
            if not proceso_activo:
                break
            label_carga.config(text=f"{'*' * i}")
            time.sleep(0.5)
        if not proceso_activo:
            break
        label_carga.config(text="")
        time.sleep(0.5)

# Función para iniciar el proceso
def iniciar():
    global proceso_activo
    proceso_activo = True
    thread_proceso = threading.Thread(target=ejecutar_proceso)
    thread_progreso = threading.Thread(target=actualizar_barra_progreso)

    thread_progreso.start()
    thread_proceso.start()

def ejecutar_proceso():
    global proceso_activo
    resultado = iniciar_proceso()
    proceso_activo = False
    label_carga.config(text="")
    messagebox.showinfo("Proceso Finalizado", f"Descarga exitosa: {resultado}")

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("App con Animación de Carga")

# Crear el Label para la barra de progreso
label_carga = tk.Label(root, text="")
label_carga.pack()

# Botón para iniciar el proceso
boton = tk.Button(root, text="Iniciar Proceso", command=iniciar)
boton.pack()

proceso_activo = False  # Bandera para controlar el estado del proceso

# Ejecutar la interfaz gráfica
root.mainloop()
