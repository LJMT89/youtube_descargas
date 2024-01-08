import tkinter as tk

root = tk.Tk()
root.title("Frame que ocupa toda la ventana")
root.geometry("800x600")  # Establece las dimensiones de la ventana principal

# Crea un Frame principal que ocupa toda la ventana
frame_principal = tk.Frame(root, bg="blue")
frame_principal.pack(fill=tk.BOTH, expand=True)

# Agrega otros elementos o frames dentro del frame_principal
# Por ejemplo, añadir otro frame interno al frame_principal
frame_interno = tk.Frame(frame_principal, bg="red")
frame_interno.pack(padx=20, pady=20)

root.mainloop()
