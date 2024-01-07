import tkinter as tk

def update_time():
    minutes = min_slider.get()
    seconds = sec_slider.get()
    time_label.config(text=f"Tiempo seleccionado: {minutes} minutos y {seconds} segundos")

def toggle_controls():
    if enable_controls.get():
        min_slider.pack()
        sec_slider.pack()
    else:
        min_slider.pack_forget()
        sec_slider.pack_forget()

    # if enable_controls.get():
    #     min_slider.config(state=tk.NORMAL)
    #     sec_slider.config(state=tk.NORMAL)
    # else:
    #     min_slider.config(state=tk.DISABLED)
    #     sec_slider.config(state=tk.DISABLED)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Selector de Tiempo")
root.geometry("300x250")

# Etiqueta para mostrar el tiempo seleccionado
time_label = tk.Label(root, text="Tiempo seleccionado: 0 minutos y 0 segundos", font=("Arial", 12))
time_label.pack(pady=10)

# Control deslizante para minutos (de 0 a 59)
min_slider = tk.Scale(root, from_=0, to=59, orient="horizontal", label="Minutos", length=200)
min_slider.pack()

# Control deslizante para segundos (de 0 a 59)
sec_slider = tk.Scale(root, from_=0, to=59, orient="horizontal", label="Segundos", length=200)
sec_slider.pack()

# Checkbutton para habilitar/deshabilitar controles
enable_controls = tk.BooleanVar()
enable_controls.set(True)  # Por defecto, los controles están habilitados
controls_checkbox = tk.Checkbutton(root, text="Habilitar controles", variable=enable_controls, command=toggle_controls)
controls_checkbox.pack(pady=5)

# Botón para actualizar el tiempo seleccionado
update_button = tk.Button(root, text="Actualizar Tiempo", command=update_time)
update_button.pack(pady=10)

root.mainloop()



# import tkinter as tk

# def update_time():
#     minutes = min_slider.get()
#     seconds = sec_slider.get()
#     time_label.config(text=f"Tiempo seleccionado: {minutes} minutos y {seconds} segundos")

# # Configuración de la ventana principal
# root = tk.Tk()
# root.title("Selector de Tiempo")
# root.geometry("450x240")

# # Etiqueta para mostrar el tiempo seleccionado
# time_label = tk.Label(root, text="Tiempo seleccionado: 0 minutos y 0 segundos", font=("Arial", 12))
# time_label.pack(pady=10)

# # Crear un separador horizontal
# separator_horizontal = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
# separator_horizontal.pack(fill=tk.X, padx=5, pady=5)

# # Control deslizante para minutos (de 0 a 59)
# min_slider = tk.Scale(root, from_=0, to=15, orient="horizontal", label="Minutos", length=200)
# min_slider.pack()

# # Control deslizante para segundos (de 0 a 59)
# sec_slider = tk.Scale(root, from_=0, to=59, orient="horizontal", label="Segundos", length=200)
# sec_slider.pack()

# # Botón para actualizar el tiempo seleccionado
# update_button = tk.Button(root, text="Actualizar Tiempo", command=update_time)
# update_button.pack(pady=10)

# root.mainloop()
