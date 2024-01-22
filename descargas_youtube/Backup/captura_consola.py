import subprocess
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class ConvertidorMP3:
    def __init__(self, input_file, output_file, text_widget):
        self.input_file = input_file
        self.output_file = output_file
        self.text_widget = text_widget

    def convertir(self):
        comando = [
            "ffmpeg",
            "-i", self.input_file,
            "-codec:a", "libmp3lame",
            "-qscale:a", "2",
            self.output_file
        ]

        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)

        for linea in proceso.stdout:
            # Mostrar la salida en el widget de texto
            self.text_widget.insert(tk.END, linea)
            self.text_widget.see(tk.END)  # Desplazar hacia abajo automáticamente
            self.text_widget.update_idletasks()  # Actualizar la interfaz

        proceso.wait()

        # Puedes agregar mensajes adicionales o lógica después de que termine la conversión
        if proceso.returncode == 0:
            mensaje = f"Conversión a MP3 completada"
        else:
            mensaje = f"Error en la conversión, código de salida: {proceso.returncode}"

        self.text_widget.insert(tk.END, mensaje + "\n")
        self.text_widget.see(tk.END)  # Desplazar hacia abajo automáticamente

class Aplicacion:
    def __init__(self, master):
        self.master = master
        self.master.title("Convertidor de canciones a MP3")

        # Crear un widget de texto desplazable
        self.texto_salida = ScrolledText(master, wrap=tk.WORD, width=60, height=15)
        self.texto_salida.pack(padx=10, pady=10)

        # Entrada para el archivo de entrada
        self.label_input = tk.Label(master, text="Archivo de entrada:")
        self.label_input.pack(pady=5)
        self.entry_input = tk.Entry(master, width=40)
        self.entry_input.pack(pady=5)

        # Entrada para el archivo de salida
        self.label_output = tk.Label(master, text="Archivo de salida:")
        self.label_output.pack(pady=5)
        self.entry_output = tk.Entry(master, width=40)
        self.entry_output.pack(pady=5)

        # Botón para iniciar la conversión
        self.boton_convertir = tk.Button(master, text="Convertir a MP3", command=self.iniciar_conversion)
        self.boton_convertir.pack(pady=5)

    def iniciar_conversion(self):
        input_file = self.entry_input.get()
        output_file = self.entry_output.get()

        # Crear una instancia del convertidor y ejecutar la conversión
        convertidor = ConvertidorMP3(input_file, output_file, self.texto_salida)
        convertidor.convertir()

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
