import tkinter as tk
from PIL import Image, ImageTk

def on_button_click():
    print("Botón presionado")

root = tk.Tk()
root.title("Botón con icono")
root.geometry("300x200")

# Cargar y redimensionar la imagen del icono
icon_image = Image.open("/media/libardo/567E18C87E18A333/IDEAFIX/DescargasYoutube/Backup/image/eliminar.png")  # Reemplaza "ruta/a/tu/imagen/icono.png" con la ruta de tu propia imagen
icon_image = icon_image.resize((32, 32))  # Cambia el tamaño del icono según sea necesario
icon = ImageTk.PhotoImage(icon_image)

# Crear botón con el icono
button_with_icon = tk.Button(root, text="Botón con icono", image=icon, compound=tk.LEFT, command=on_button_click)
button_with_icon.pack(pady=20)

root.mainloop()
