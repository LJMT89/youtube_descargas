import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
import subprocess

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

        # Barra de menú
        self.barra_menu = tk.Menu(self.root)
        
        # Menú Archivo
        self.menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        #self.menu_archivo.add_command(label="Nuevo")
        self.menu_archivo.add_command(label="Abrir carpeta contenedora", command=self.abrir_carpeta)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=root.quit)
        self.barra_menu.add_cascade(label="Archivo", menu=self.menu_archivo)
        
        # Menú Ayuda
        # self.menu_ayuda = tk.Menu(self.barra_menu, tearoff=0)
        # self.menu_ayuda.add_command(label="Ayuda")
        # self.menu_ayuda.add_command(label="Acerca de")
        # self.barra_menu.add_cascade(label="Ayuda", menu=self.menu_ayuda)
        
        self.root.config(menu=self.barra_menu)

        self.label_title = tk.Label(self.frame, text="INGRESE AQUÍ LA URL DE YOUTUBE", font=self.title_font)
        self.label_title.pack(pady=15)

        self.url = tk.Entry(self.frame, width=50, font=self.url_font)
        self.url.pack(pady=15)
        self.url.focus_set()
        #self.url.bind("<Button-3>", self.mostrar_menu_contextual)

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
        subprocess.Popen(["xdg-open", self.current_folder])

    def pegar_texto(self):
        # Obtener el texto del portapapeles y pegarlo en el Entry
        texto_clipboard = self.root.clipboard_get()
        self.url.insert(tk.INSERT, texto_clipboard)

    def borrar_url(self):
        self.url.delete(0, tk.END)

    def descargar_audio(self):
        url_youtube = self.obtener_url()
        if self.validar_url_youtube(url_youtube):
            # current_folder = os.getcwd()
            #current_folder = "/media/jose/90980D73980D58DC/PAPA/Música/Descargas de YouTube"
            yt = YouTube(url_youtube)
            audio = yt.streams.filter(only_audio=True).first()
            audio.download(output_path=self.current_folder)
            video_title = yt.title
            self.borrar_url()
            self.mostrar_mensaje(f"Canción descargada con éxito: \n{video_title}")
        else:
            self.mostrar_mensaje("La URL de YouTube no es válida.")

    '''
    def mostrar_menu_contextual(self, event):
        # Crea un menú contextual con algunas opciones
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Cortar")
        menu.add_command(label="Copiar")
        menu.add_command(label="Pegar", command=self.pegar_texto)
        menu.add_separator()
        menu.add_command(label="Seleccionar todo")

        # Muestra el menú contextual en la posición actual del ratón
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    '''

def main():
    root = tk.Tk()
    vista = Vista(root)
    root.mainloop()

if __name__ == "__main__":
    main()
