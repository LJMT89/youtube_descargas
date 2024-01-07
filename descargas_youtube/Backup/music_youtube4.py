import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
import moviepy.editor as mp
import subprocess
import os

class Vista:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x180")
        self.root.resizable(False, False)
        self.root.title("YOUTUBE A MP3".center(60).upper())
        self.title_font = ('Arial', 18, 'bold')
        self.url_font = ('Arial', 18)

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.barra_menu = tk.Menu(self.root)
        
        self.menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        self.menu_archivo.add_command(label="Abrir carpeta contenedora", command=self.abrir_carpeta)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=root.quit)
        self.barra_menu.add_cascade(label="Archivo", menu=self.menu_archivo)
        
        self.root.config(menu=self.barra_menu)

        self.label_title = tk.Label(self.frame, text="INGRESE AQUÍ LA URL DE YOUTUBE", font=self.title_font)
        self.label_title.pack(pady=15)

        self.url = tk.Entry(self.frame, width=50, font=self.url_font)
        self.url.pack(pady=15)
        self.url.focus_set()

        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.pack()
        
        self.boton_pegar = tk.Button(self.btn_frame, text="PEGAR", command=self.pegar_texto, bg="#4484ff", activebackground="#98bbff")
        self.boton_pegar.pack(side=tk.LEFT, padx=120)
        
        self.boton_borrar = tk.Button(self.btn_frame, text="BORRAR", command=self.borrar_url, bg="#f94949", activebackground="#ff9898")
        self.boton_borrar.pack(side=tk.RIGHT, padx=120)

        self.boton_descargar = tk.Button(self.btn_frame, text="DESCARGAR", command=self.descargar_audio, bg="#3eff2a", activebackground="#90ff84")
        self.boton_descargar.pack()

        self.current_folder = "/media/jose/90980D73980D58DC/PAPA/Música/Descargas de YouTube"

    def obtener_url(self):
        return self.url.get()

    def mostrar_mensaje(self, mensaje):
        messagebox.showinfo("Mensaje", mensaje)

    def validar_url_youtube(self, texto):
        if texto.startswith("https://www.youtube.com/"):
            return True
        else:
            return False

    def abrir_carpeta(self):
        subprocess.Popen(["nemo", self.current_folder])

    def pegar_texto(self):
        texto_clipboard = self.root.clipboard_get()
        self.url.insert(tk.INSERT, texto_clipboard)

    def borrar_url(self):
        self.url.delete(0, tk.END)

    def descargar_audio(self):
        url_youtube = self.obtener_url()
        if self.validar_url_youtube(url_youtube):
            try:
                yt = YouTube(url_youtube)
                audio = yt.streams.filter(only_audio=True).first()
                if audio:
                    # Descargar el archivo MP4
                    video_title = yt.title
                    mp4_file = self.current_folder + '/' + video_title + '.mp4'
                    audio.download(output_path=self.current_folder)
                    
                    # Convertir MP4 a MP3
                    mp3_file = self.current_folder + '/' + video_title + '.mp3'
                    clip = mp.VideoFileClip(mp4_file)
                    clip.audio.write_audiofile(mp3_file)

                    # Eliminar el archivo MP4 después de la conversión
                    clip.close()
                    os.remove(mp4_file)
                    
                    self.borrar_url()
                    self.mostrar_mensaje(f"Canción descargada con éxito: \n{video_title}")
                else:
                    self.mostrar_mensaje("No se encontró un archivo de audio disponible.")
            except Exception as e:
                self.mostrar_mensaje(f"Error al descargar: {str(e)}")
        else:
            self.mostrar_mensaje("La URL de YouTube no es válida.")

def main():
    root = tk.Tk()
    vista = Vista(root)
    root.mainloop()

if __name__ == "__main__":
    main()