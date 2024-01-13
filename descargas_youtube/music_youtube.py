import tkinter as tk
import threading
import time
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
        
        # Título de la ventana principal
        self.root.title("YOUTUBE A MP3".center(60).upper())
        self.current_folder = "/media/jose/90980D73980D58DC/PAPA/Música/Descargas de YouTube"
        #self.current_folder = "/media/libardo/567E18C87E18A333/IDEAFIX/DescargasYoutube/youtube_download"
        self.calidad_audio = "256k"
        self.proceso_activo = False

        # Fuentes
        self.title_font = ('Arial', 18, 'bold')
        self.url_font = ('Arial', 15)
        self.titulos_tiempos_font = ('Arial', 12, 'bold underline')
        self.label_metadatos_font = ('Arial', 12, 'bold')
        self.textfield_metadatos_font = ('Arial', 12)

        # Frame principal
        self.frame = tk.Frame(self.root, background='white')
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Barra de menú
        self.barra_menu = tk.Menu(self.root)
        self.menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        self.menu_archivo.add_command(label="Abrir carpeta contenedora", command=self.abrir_carpeta)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=root.quit)
        self.barra_menu.add_cascade(label="Archivo", menu=self.menu_archivo)
        self.root.config(menu=self.barra_menu)

        # Label de ingresar la url de youtube
        self.label_title = tk.Label(self.frame, text="INGRESE AQUÍ LA URL DE YOUTUBE", font=self.title_font, background='white')
        self.label_title.pack(pady=15)

        # Frame para la URL y los botones Abrir Carpeta Contenedora y Eliminar Texto
        self.url_btns_frame = tk.Frame(self.frame, background='white')
        self.url_btns_frame.pack()

        # Cargar y redimensionar la imagen del icono - Boton Pegar
        self.boton_pegar = tk.Button(self.url_btns_frame, text='Pegar', command=self.pegar_texto, bg="#4484ff", activebackground="#98bbff")
        self.boton_pegar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cargar y redimensionar la imagen del icono - Boton Borrar
        self.boton_borrar = tk.Button(self.url_btns_frame, text='Borrar', command=self.borrar_url, bg="#f94949", activebackground="#ff9898")
        self.boton_borrar.pack(side=tk.RIGHT, padx=(10, 0))

        # TextField para el ingreso de la URL de YouTube
        self.url = tk.Entry(self.url_btns_frame, width=50, font=self.url_font)
        self.url.pack()
        self.url.focus_set()

        # Frame para los Frame: Tiempo Inicial - Tiempo Final
        self.lbl_time_frame = tk.Frame(self.frame, background='white')
        self.lbl_time_frame.pack(pady=(15, 0))

        # Frame para los label de Tiempo Inicial y Checkbutton Tiempo Inicial
        self.lbl_time_inicial_frame = tk.Frame(self.lbl_time_frame)
        self.lbl_time_inicial_frame.pack(side=tk.LEFT, padx=90, pady=15)

        # Checkbutton para habilitar/deshabilitar Tiempo Inicial
        self.controls_tiempo_inicial = tk.BooleanVar()
        self.controls_tiempo_inicial.set(False)  # Por defecto, los controles están deshabilitados
        self.tiempo_inicial_checkbox = tk.Checkbutton(self.lbl_time_inicial_frame, variable=self.controls_tiempo_inicial, command=self.habilitar_tiempo_inicial, background='orange', activebackground='#ffc38b')
        self.tiempo_inicial_checkbox.pack(side=tk.LEFT)

        # Label para Tiempo Inicial
        self.time_label_inicial = tk.Label(self.lbl_time_inicial_frame, text="Tiempo Inicial", font=self.titulos_tiempos_font, background='white')
        self.time_label_inicial.pack(side=tk.LEFT)

        # Frame para los label de Tiempo Final y Checkbutton Tiempo Final
        self.lbl_time_final_frame = tk.Frame(self.lbl_time_frame)
        self.lbl_time_final_frame.pack(side=tk.LEFT, padx=96, pady=15)

        # Checkbutton para habilitar/deshabilitar Tiempo Final
        self.controls_tiempo_final = tk.BooleanVar()
        self.controls_tiempo_final.set(False)  # Por defecto, los controles están deshabilitados
        self.tiempo_final_checkbox = tk.Checkbutton(self.lbl_time_final_frame, variable=self.controls_tiempo_final, command=self.habilitar_tiempo_final, background='orange', activebackground='#ffc38b')
        self.tiempo_final_checkbox.pack(side=tk.LEFT)

        # Label para Tiempo Final
        self.time_label_final = tk.Label(self.lbl_time_final_frame, text="Tiempo Final", font=self.titulos_tiempos_font, background='white')
        self.time_label_final.pack(side=tk.LEFT)

        # Frame para: Frame de Tiempo Inicial - Frame de Tiempo Final
        self.time_frame = tk.Frame(self.frame, background='white')
        self.time_frame.pack(pady=(0, 9))

        # Frame de Tiempo Inicial
        self.time_frame_inicio = tk.Frame(self.time_frame, background='white')
        self.time_frame_inicio.pack(side=tk.LEFT, padx=60)

        # Control deslizante para minutos INICIO (de 0 a 15)
        self.min_slider_inicio = tk.Scale(self.time_frame_inicio, from_=0, to=15, orient="horizontal", label="Minutos", length=200, tickinterval=5, background='white')
        self.min_slider_inicio.pack()

        # Control deslizante para segundos INICIO (de 0 a 59)
        self.sec_slider_inicio = tk.Scale(self.time_frame_inicio, from_=0, to=59, orient="horizontal", label="Segundos", length=200, tickinterval=10, background='white')
        self.sec_slider_inicio.pack()

        # Frame de Tiempo Final
        self.time_frame_final = tk.Frame(self.time_frame, background='white')
        self.time_frame_final.pack(side=tk.LEFT, padx=54)

        # Control deslizante para minutos FINAL (de 0 a 15)
        self.min_slider_final = tk.Scale(self.time_frame_final, from_=0, to=15, orient="horizontal", label="Minutos", length=200, tickinterval=5, background='white')
        self.min_slider_final.pack()

        # Control deslizante para segundos FINAL (de 0 a 59)
        self.sec_slider_final = tk.Scale(self.time_frame_final, from_=0, to=59, orient="horizontal", label="Segundos", length=200, tickinterval=10, background='white')
        self.sec_slider_final.pack()

        # Frame para la barra de progreso
        self.progreso_frame = tk.Frame(self.frame)
        self.progreso_frame.pack()

        # Crear el Label para la barra de progreso
        self.label_carga = tk.Label(self.progreso_frame, text="", font=self.url_font, background='white')
        self.label_carga.pack()

        # Frame para la metadata de titulo
        self.titulo_metadata_frame = tk.Frame(self.frame, background='white')
        self.titulo_metadata_frame.pack(pady=(0, 30))

        # Label para metadata titulo
        self.titulo_lbl_metadata = tk.Label(self.titulo_metadata_frame, text="Título:   ", font=self.label_metadatos_font, background='white')
        self.titulo_lbl_metadata.pack(side=tk.LEFT)

        # TextField para la metadata del titulo
        self.titulo_metadata = tk.Entry(self.titulo_metadata_frame, width=30, font=self.textfield_metadatos_font)
        self.titulo_metadata.pack()

        # Frame para la metadata de artista
        self.artista_metadata_frame = tk.Frame(self.frame, background='white')
        self.artista_metadata_frame.pack()

        # Label para metadata artista
        self.artista_lbl_metadata = tk.Label(self.artista_metadata_frame, text="Artista:  ", font=self.label_metadatos_font, background='white')
        self.artista_lbl_metadata.pack(side=tk.LEFT)

        # TextField para la metadata del artista
        self.artista_metadata = tk.Entry(self.artista_metadata_frame, width=30, font=self.textfield_metadatos_font)
        self.artista_metadata.pack()

        # Frame para la metadata de genero
        self.genero_metadata_frame = tk.Frame(self.frame, background='white')
        self.genero_metadata_frame.pack(pady=30)

        # Label para metadata genero
        self.genero_lbl_metadata = tk.Label(self.genero_metadata_frame, text="Género: ", font=self.label_metadatos_font, background='white')
        self.genero_lbl_metadata.pack(side=tk.LEFT)

        # TextField para la metadata del genero
        self.genero_metadata = tk.Entry(self.genero_metadata_frame, width=30, font=self.textfield_metadatos_font)
        self.genero_metadata.pack()

        # Frame para el boton DESCARGAR
        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.pack()

        # Cargar y redimensionar la imagen del icono - Boton Descargar
        self.boton_descargar = tk.Button(self.btn_frame, text="DESCARGAR", command=self.iniciar, font=self.label_metadatos_font, bg="#3eff2a", activebackground="#90ff84")
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
        self.url.focus_set()

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
                            tiempo_inicio = (min_inicio * 60) + sec_inicio
                            tiempo_final = (min_final * 60) + sec_final
                            if tiempo_inicio < tiempo_final:
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
                            else:
                                os.remove(archivo_mp4_ruta)
                                return f"El tiempo de inicio debe ser menor al tiempo final"
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
                        return f"DESCARGA EXITOSA: \n{video_title}"
                        # self.mostrar_mensaje(f"DESCARGA EXITOSA: \n{video_title}")
                    else:
                        self.mostrar_mensaje("No se encontró un archivo de audio disponible.")
                except Exception as e:
                    self.mostrar_mensaje(f"Error al descargar: {str(e)}")
            else:
                self.mostrar_mensaje("Agregue un título a la canción.")
        else:
            self.mostrar_mensaje("La URL de YouTube no es válida.")

    # Función para actualizar la barra de progreso
    def actualizar_barra_progreso(self):
        time.sleep(0.5)
        while self.proceso_activo:
            for i in range(1, 11):
                if not self.proceso_activo:
                    break
                self.label_carga.config(text=f"{'*' * i}", font=self.url_font)
                time.sleep(0.5)
            if not self.proceso_activo:
                break
            self.label_carga.config(text="")
            time.sleep(0.5)

    # Función para iniciar el proceso
    def iniciar(self):
        self.proceso_activo = True
        self.boton_descargar.config(state=tk.DISABLED)
        thread_proceso = threading.Thread(target=self.ejecutar_proceso)
        thread_progreso = threading.Thread(target=self.actualizar_barra_progreso)

        thread_progreso.start()
        thread_proceso.start()

    def ejecutar_proceso(self):
        resultado = self.descargar_audio()
        self.proceso_activo = False
        self.boton_descargar.config(state=tk.NORMAL)
        self.label_carga.config(text="")
        if resultado:
            messagebox.showinfo("Proceso Finalizado", resultado)

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