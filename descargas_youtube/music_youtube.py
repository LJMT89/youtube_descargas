import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from pytube import YouTube
import ffmpeg
import subprocess
import os

class Vista:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.title("YOUTUBE A MP3".center(60).upper())
        #self.current_folder = "/media/jose/90980D73980D58DC/PAPA/Música/Descargas de YouTube"
        self.current_folder = "/media/libardo/567E18C87E18A333/IDEAFIX/DescargasYoutube/youtube_download"
        self.calidad_audio = "256k"

        # Fuentes
        self.title_font = ('Arial', 18, 'bold')
        self.url_font = ('Arial', 15)
        self.titulos_tiempos_font = ('Arial', 12, 'bold underline')
        self.label_metadatos_font = ('Arial', 12, 'bold')
        self.textfield_metadatos_font = ('Arial', 12)

        # Frame principal
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Barra de menú
        self.barra_menu = tk.Menu(self.root)
        self.menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        self.menu_archivo.add_command(label="Abrir carpeta contenedora", command=self.abrir_carpeta)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=root.quit)
        self.barra_menu.add_cascade(label="Archivo", menu=self.menu_archivo)
        self.root.config(menu=self.barra_menu)

        # Label de ingresar la url de youtube
        self.label_title = tk.Label(self.frame, text="INGRESE AQUÍ LA URL DE YOUTUBE", font=self.title_font)
        self.label_title.pack(pady=15)

        # Frame para la URL y los botones Abrir Carpeta Contenedora y Eliminar Texto
        self.url_btns_frame = tk.Frame(self.frame)
        self.url_btns_frame.pack()

        # Cargar y redimensionar la imagen del icono - Boton Pegar
        self.icon_pegar = Image.open("image/pegar.png")
        self.icon_pegar = self.icon_pegar.resize((25, 25))  # Cambia el tamaño del icono según sea necesario
        self.pegar_icono = ImageTk.PhotoImage(self.icon_pegar)
        self.boton_pegar = tk.Button(self.url_btns_frame, image=self.pegar_icono, command=self.pegar_texto, bg="#4484ff", activebackground="#98bbff")
        self.boton_pegar.pack(side=tk.LEFT, padx=10)
        
        # Cargar y redimensionar la imagen del icono - Boton Borrar
        self.icon_borrar = Image.open("image/eliminar.png")  # Reemplaza "ruta/a/tu/imagen/icono.png" con la ruta de tu propia imagen
        self.icon_borrar = self.icon_borrar.resize((25, 25))  # Cambia el tamaño del icono según sea necesario
        self.borrar_icono = ImageTk.PhotoImage(self.icon_borrar)
        self.boton_borrar = tk.Button(self.url_btns_frame, image=self.borrar_icono, command=self.borrar_url, bg="#f94949", activebackground="#ff9898")
        self.boton_borrar.pack(side=tk.RIGHT, padx=10)

        # TextField para el ingreso de la URL de YouTube
        self.url = tk.Entry(self.url_btns_frame, width=50, font=self.url_font)
        self.url.pack()
        self.url.focus_set()

        # Frame para los Frame: Tiempo Inicial - Tiempo Final
        self.lbl_time_frame = tk.Frame(self.frame)
        self.lbl_time_frame.pack(pady=15)

        # Frame para los label de Tiempo Inicial y Checkbutton Tiempo Inicial
        self.lbl_time_inicial_frame = tk.Frame(self.lbl_time_frame)
        self.lbl_time_inicial_frame.pack(side=tk.LEFT, padx=90)

        # Checkbutton para habilitar/deshabilitar Tiempo Inicial
        self.controls_tiempo_inicial = tk.BooleanVar()
        self.controls_tiempo_inicial.set(False)  # Por defecto, los controles están deshabilitados
        self.tiempo_inicial_checkbox = tk.Checkbutton(self.lbl_time_inicial_frame, variable=self.controls_tiempo_inicial, command=self.habilitar_tiempo_inicial)
        self.tiempo_inicial_checkbox.pack(side=tk.LEFT)

        # Label para Tiempo Inicial
        self.time_label_inicial = tk.Label(self.lbl_time_inicial_frame, text="Tiempo Inicial", font=self.titulos_tiempos_font)
        self.time_label_inicial.pack(side=tk.LEFT)

        # Frame para los label de Tiempo Final y Checkbutton Tiempo Final
        self.lbl_time_final_frame = tk.Frame(self.lbl_time_frame)
        self.lbl_time_final_frame.pack(side=tk.LEFT, padx=96)

        # Checkbutton para habilitar/deshabilitar Tiempo Final
        self.controls_tiempo_final = tk.BooleanVar()
        self.controls_tiempo_final.set(False)  # Por defecto, los controles están deshabilitados
        self.tiempo_final_checkbox = tk.Checkbutton(self.lbl_time_final_frame, variable=self.controls_tiempo_final, command=self.habilitar_tiempo_final)
        self.tiempo_final_checkbox.pack(side=tk.LEFT)

        # Label para Tiempo Final
        self.time_label_final = tk.Label(self.lbl_time_final_frame, text="Tiempo Final", font=self.titulos_tiempos_font)
        self.time_label_final.pack(side=tk.LEFT)

        # Frame para: Frame de Tiempo Inicial - Frame de Tiempo Final
        self.time_frame = tk.Frame(self.frame)
        self.time_frame.pack()

        # Frame de Tiempo Inicial
        self.time_frame_inicio = tk.Frame(self.time_frame)
        self.time_frame_inicio.pack(side=tk.LEFT, padx=60)

        # Control deslizante para minutos INICIO (de 0 a 15)
        self.min_slider_inicio = tk.Scale(self.time_frame_inicio, from_=0, to=15, orient="horizontal", label="Minutos", length=200, tickinterval=5)
        self.min_slider_inicio.pack()

        # Control deslizante para segundos INICIO (de 0 a 59)
        self.sec_slider_inicio = tk.Scale(self.time_frame_inicio, from_=0, to=59, orient="horizontal", label="Segundos", length=200, tickinterval=10)
        self.sec_slider_inicio.pack()

        # Frame de Tiempo Final
        self.time_frame_final = tk.Frame(self.time_frame)
        self.time_frame_final.pack(side=tk.LEFT, padx=60)

        # Control deslizante para minutos FINAL (de 0 a 15)
        self.min_slider_final = tk.Scale(self.time_frame_final, from_=0, to=15, orient="horizontal", label="Minutos", length=200, tickinterval=5)
        self.min_slider_final.pack()

        # Control deslizante para segundos FINAL (de 0 a 59)
        self.sec_slider_final = tk.Scale(self.time_frame_final, from_=0, to=59, orient="horizontal", label="Segundos", length=200, tickinterval=10)
        self.sec_slider_final.pack()

        # Frame para la metadata de titulo
        self.titulo_metadata_frame = tk.Frame(self.frame)
        self.titulo_metadata_frame.pack()

        # Label para metadata titulo
        self.titulo_lbl_metadata = tk.Label(self.titulo_metadata_frame, text="Título: ", font=self.label_metadatos_font)
        self.titulo_lbl_metadata.pack(side=tk.LEFT)

        # TextField para la metadata del titulo
        self.titulo_metadata = tk.Entry(self.titulo_metadata_frame, width=30, font=self.textfield_metadatos_font)
        self.titulo_metadata.pack(pady=30)

        # Frame para la metadata de artista
        self.artista_metadata_frame = tk.Frame(self.frame)
        self.artista_metadata_frame.pack()

        # Label para metadata artista
        self.artista_lbl_metadata = tk.Label(self.artista_metadata_frame, text="Artista: ", font=self.label_metadatos_font)
        self.artista_lbl_metadata.pack(side=tk.LEFT)

        # TextField para la metadata del artista
        self.artista_metadata = tk.Entry(self.artista_metadata_frame, width=30, font=self.textfield_metadatos_font)
        self.artista_metadata.pack()

        # Frame para la metadata de genero
        self.genero_metadata_frame = tk.Frame(self.frame)
        self.genero_metadata_frame.pack()

        # Label para metadata genero
        self.genero_lbl_metadata = tk.Label(self.genero_metadata_frame, text="Género: ", font=self.label_metadatos_font)
        self.genero_lbl_metadata.pack(side=tk.LEFT)

        # TextField para la metadata del genero
        self.genero_metadata = tk.Entry(self.genero_metadata_frame, width=30, font=self.textfield_metadatos_font)
        self.genero_metadata.pack(pady=30)

        # Frame para el boton DESCARGAR
        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.pack()

        # Cargar y redimensionar la imagen del icono - Boton Descargar
        self.icon_descargar = Image.open("image/descargar.png")  # Reemplaza "ruta/a/tu/imagen/icono.png" con la ruta de tu propia imagen
        self.icon_descargar = self.icon_descargar.resize((25, 25))  # Cambia el tamaño del icono según sea necesario
        self.descargar_icono = ImageTk.PhotoImage(self.icon_descargar)
        self.boton_descargar = tk.Button(self.btn_frame, text="DESCARGAR", image=self.descargar_icono, compound=tk.LEFT, command=self.descargar_audio, bg="#3eff2a", activebackground="#90ff84")
        self.boton_descargar.pack()

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
        try:
            subprocess.Popen(["xdg-open", self.current_folder])
        except Exception as e:
            self.mostrar_mensaje(f"Abra primero una carpeta cualquiera: {str(e)}")

    def habilitar_tiempo_inicial(self):
        if self.controls_tiempo_inicial.get():
            self.min_slider_inicio.pack()
            self.sec_slider_inicio.pack()
        else:
            self.min_slider_inicio.pack_forget()
            self.sec_slider_inicio.pack_forget()

    def habilitar_tiempo_final(self):
        if self.controls_tiempo_final.get():
            self.min_slider_final.pack()
            self.sec_slider_final.pack()
        else:
            self.min_slider_final.pack_forget()
            self.sec_slider_final.pack_forget()

    def pegar_texto(self):
        texto_clipboard = self.root.clipboard_get()
        self.url.insert(tk.INSERT, texto_clipboard)

    def borrar_url(self):
        self.url.delete(0, tk.END)

    def borrar_metadatos(self):
        self.titulo_metadata.delete(0, tk.END)
        self.artista_metadata.delete(0, tk.END)
        self.genero_metadata.delete(0, tk.END)

    def validar_titulo(self):
        titulo = self.eliminar_punto_final(self.titulo_metadata.get())
        return titulo

    def eliminar_punto_final(self, cadena):
        if cadena.endswith('.'):
            cadena = cadena[:-1]
        return cadena

    def tiempo_inicial_func(self, min, sec):
        if min < 10 and sec < 10:
            tiempo_inicial_corte = f'00:0{min}:0{sec}'
        elif min < 10:
            tiempo_inicial_corte = f'00:0{min}:{sec}'
        elif sec < 10:
            tiempo_inicial_corte = f'00:{min}:0{sec}'
        else:
            tiempo_inicial_corte = f'00:{min}:{sec}'
        return tiempo_inicial_corte

    def tiempo_final_func(self, min, sec):
        if min < 10 and sec < 10:
            tiempo_final_corte = f'00:0{min}:0{sec}'
        elif min < 10:
            tiempo_final_corte = f'00:0{min}:{sec}'
        elif sec < 10:
            tiempo_final_corte = f'00:{min}:0{sec}'
        else:
            tiempo_final_corte = f'00:{min}:{sec}'
        return tiempo_final_corte

    def descargar_audio(self):
        url_youtube = self.obtener_url()
        video_title = self.validar_titulo()
        if self.validar_url_youtube(url_youtube):
            if video_title:
                try:
                    yt = YouTube(url_youtube)
                    audio = yt.streams.filter(only_audio=True).first()
                    if audio:
                        #video_title = self.eliminar_punto_final(yt.title)
                        video_artista = self.artista_metadata.get()
                        video_genero = self.genero_metadata.get()
                        audio.download(filename=f"{video_title}.{audio.subtype}", output_path=self.current_folder)
                        archivo_mp4_ruta = os.path.join(self.current_folder, f"{video_title}.{audio.subtype}")
                        archivo_mp3_ruta = os.path.join(self.current_folder, f"{video_title}.mp3")

                        if self.controls_tiempo_inicial.get() and self.controls_tiempo_final.get():
                            min_inicio = self.min_slider_inicio.get()
                            sec_inicio = self.sec_slider_inicio.get()
                            min_final = self.min_slider_final.get()
                            sec_final = self.sec_slider_final.get()
                            start_time = self.tiempo_inicial_func(min_inicio, sec_inicio)
                            end_time = self.tiempo_final_func(min_final, sec_final)
                            ffmpeg.input(archivo_mp4_ruta).output(
                                archivo_mp3_ruta, 
                                audio_bitrate=self.calidad_audio, 
                                ss=start_time, 
                                to=end_time,
                                **{ 'metadata:g:0':f"title={video_title}", 
                                    'metadata:g:1':f"artist={video_artista}", 
                                    'metadata:g:2':f"genre={video_genero}", 
                                    }
                                ).run()
                        elif self.controls_tiempo_inicial.get():
                            min_inicio = self.min_slider_inicio.get()
                            sec_inicio = self.sec_slider_inicio.get()
                            start_time = self.tiempo_inicial_func(min_inicio, sec_inicio)
                            ffmpeg.input(archivo_mp4_ruta).output(
                                archivo_mp3_ruta, 
                                audio_bitrate=self.calidad_audio, 
                                ss=start_time,
                                **{ 'metadata:g:0':f"title={video_title}", 
                                    'metadata:g:1':f"artist={video_artista}", 
                                    'metadata:g:2':f"genre={video_genero}", 
                                    }
                                ).run()
                        elif self.controls_tiempo_final.get():
                            min_final = self.min_slider_final.get()
                            sec_final = self.sec_slider_final.get()
                            end_time = self.tiempo_final_func(min_final, sec_final)
                            ffmpeg.input(archivo_mp4_ruta).output(
                                archivo_mp3_ruta, 
                                audio_bitrate=self.calidad_audio, 
                                to=end_time,
                                **{ 'metadata:g:0':f"title={video_title}", 
                                    'metadata:g:1':f"artist={video_artista}", 
                                    'metadata:g:2':f"genre={video_genero}", 
                                    }
                                ).run()
                        else:
                            ffmpeg.input(archivo_mp4_ruta).output(
                                archivo_mp3_ruta, 
                                audio_bitrate=self.calidad_audio,
                                **{ 'metadata:g:0':f"title={video_title}", 
                                    'metadata:g:1':f"artist={video_artista}", 
                                    'metadata:g:2':f"genre={video_genero}", 
                                    }
                                ).run()
                        
                        os.remove(archivo_mp4_ruta)
                        self.borrar_url()
                        self.borrar_metadatos()
                        self.mostrar_mensaje(f"DESCARGA EXITOSA: \n{video_title}") 
                    else:
                        self.mostrar_mensaje("No se encontró un archivo de audio disponible.")
                except Exception as e:
                    self.mostrar_mensaje(f"Error al descargar: {str(e)}")
            else:
                self.mostrar_mensaje("Agregue un título a la canción.")
        else:
            self.mostrar_mensaje("La URL de YouTube no es válida.")

def main():
    root = tk.Tk()
    vista = Vista(root)
    # Función para ejecutar las funciones después de un breve tiempo
    def actualizar_control_deslizante():
        vista.habilitar_tiempo_inicial()
        vista.habilitar_tiempo_final()

    # Programar la ejecución de las funciones después de 100 milisegundos
    root.after(100, actualizar_control_deslizante)
    root.mainloop()

if __name__ == "__main__":
    main()