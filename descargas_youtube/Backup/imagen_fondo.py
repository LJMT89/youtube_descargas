import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("800x630")
root.title("Imagen de Fondo")

# Cargar la imagen
ruta_imagen = "image/background3.png"  # Reemplaza con la ruta de tu imagen
imagen = Image.open(ruta_imagen)
imagen = ImageTk.PhotoImage(imagen)

# Crear un Label y configurarlo para mostrar la imagen de fondo
label_fondo = tk.Label(root, image=imagen)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Estirar la imagen para que cubra toda la ventana

# Agregar otros widgets o elementos a la ventana
# Por ejemplo, un botón sobre la imagen de fondo
boton = tk.Button(root, text="Haz clic")
boton.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Colocar el botón en el centro

root.mainloop()
