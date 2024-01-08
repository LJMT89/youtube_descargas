import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("800x630")
root.title("Label con Fondo Transparente")

# Cargar una imagen con fondo transparente
ruta_imagen = "image/fondo_transparente.png"  # Ruta de tu imagen con transparencia
imagen = Image.open(ruta_imagen)
imagen = ImageTk.PhotoImage(imagen)

# Crear un Frame
frame = tk.Frame(root)
frame.pack()

# Colocar la imagen como fondo del label
label_con_fondo_transparente = tk.Label(frame, image=imagen)
label_con_fondo_transparente.image = imagen  # Mantener una referencia para evitar que la imagen se elimine
label_con_fondo_transparente.pack()

# Crear un label de texto sobre la imagen
label_texto = tk.Label(label_con_fondo_transparente, text="INGRESE AQUÍ LA URL DE YOUTUBE", font=("Arial", 12), bg="white")
label_texto.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()
