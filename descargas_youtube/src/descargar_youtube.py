import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.QtCore import Qt
from pytube import YouTube
import ffmpeg
import time
from PyQt5.QtCore import QThread, pyqtSignal

basedir = os.path.dirname(__file__)

class DownloadThread(QThread):
    # Señales para el progreso y la finalización de la descarga
    progress_signal = pyqtSignal(str)
    download_finished_signal = pyqtSignal()

    def __init__(self, url_youtube, check_tiempo_inicial, check_tiempo_final, current_folder, calidad_audio, video_title, video_artista, video_genero, video_compositor):
        super().__init__()
        self.url_youtube = url_youtube
        self.check_tiempo_inicial = check_tiempo_inicial
        self.check_tiempo_final = check_tiempo_final
        self.current_folder = current_folder
        self.calidad_audio = calidad_audio
        self.video_title = video_title
        self.video_artista = video_artista
        self.video_genero = video_genero
        self.video_compositor = video_compositor
        self.stopped = False

    def run(self):
        try:
            self.progress_signal.emit('')  # Iniciar el progreso con un espacio en blanco
            yt = YouTube(self.url_youtube)
            audio = yt.streams.filter(only_audio=True).first()
            if audio:
                audio.download(filename=f"{self.video_title}.{audio.subtype}", output_path=self.current_folder)
                archivo_mp4_ruta = os.path.join(self.current_folder, f"{self.video_title}.{audio.subtype}")
                archivo_mp3_ruta = os.path.join(self.current_folder, f"{self.video_title}.mp3")

                if self.check_tiempo_inicial.isChecked() and self.check_tiempo_final.isChecked():
                    min_inicio = self.slider_tiempo_inicial_min.value()
                    sec_inicio = self.slider_tiempo_inicial_seg.value()
                    min_final = self.slider_tiempo_final_min.value()
                    sec_final = self.slider_tiempo_final_seg.value()
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
                            **{ 'metadata:g:0':f"title={self.video_title}", 
                                'metadata:g:1':f"artist={self.video_artista}", 
                                'metadata:g:2':f"genre={self.video_genero}",
                                'metadata:g:3':f"composer={self.video_compositor}",
                                }
                            ).run()
                    else:
                        os.remove(archivo_mp4_ruta)
                        return f"El tiempo de inicio debe ser menor al tiempo final"
                elif self.check_tiempo_inicial.isChecked():
                    min_inicio = self.slider_tiempo_inicial_min.value()
                    sec_inicio = self.slider_tiempo_inicial_seg.value()
                    start_time = self.tiempo_inicial_func(min_inicio, sec_inicio)
                    ffmpeg.input(archivo_mp4_ruta).output(
                        archivo_mp3_ruta, 
                        audio_bitrate=self.calidad_audio, 
                        ss=start_time,
                        **{ 'metadata:g:0':f"title={self.video_title}", 
                            'metadata:g:1':f"artist={self.video_artista}", 
                            'metadata:g:2':f"genre={self.video_genero}",
                            'metadata:g:3':f"composer={self.video_compositor}",
                            }
                        ).run()
                elif self.check_tiempo_final.isChecked():
                    min_final = self.slider_tiempo_final_min.value()
                    sec_final = self.slider_tiempo_final_seg.value()
                    end_time = self.tiempo_final_func(min_final, sec_final)
                    ffmpeg.input(archivo_mp4_ruta).output(
                        archivo_mp3_ruta, 
                        audio_bitrate=self.calidad_audio, 
                        to=end_time,
                        **{ 'metadata:g:0':f"title={self.video_title}", 
                            'metadata:g:1':f"artist={self.video_artista}", 
                            'metadata:g:2':f"genre={self.video_genero}",
                            'metadata:g:3':f"composer={self.video_compositor}",
                            }
                        ).run()
                else:
                    ffmpeg.input(archivo_mp4_ruta).output(
                        archivo_mp3_ruta, 
                        audio_bitrate=self.calidad_audio,
                        **{ 'metadata:g:0':f"title={self.video_title}", 
                            'metadata:g:1':f"artist={self.video_artista}", 
                            'metadata:g:2':f"genre={self.video_genero}",
                            'metadata:g:3':f"composer={self.video_compositor}",
                            }
                        ).run()
                os.remove(archivo_mp4_ruta)
                # self.borrar_url(self.input_url)
                # self.borrar_metadatos()
                # return (f"DESCARGA EXITOSA: \n{self.video_title}")
            else:
                self.mostrar_mensaje("No se encontró un archivo de audio disponible.")
            
            if not self.stopped:
                self.progress_signal.emit('')  # Limpiar la barra de progreso al 100%
                self.download_finished_signal.emit()  # Emitir señal de finalización

        except Exception as e:
            print(f"Error al descargar: ", {str(e)})
            # Descargar_Youtube_UI.mostrar_mensaje(f"Error al descargar: ", {str(e)})

    def stop(self):
        self.stopped = True

class Descargar_Youtube_UI(QMainWindow):
    def __init__(self, ui_ppal):
        super().__init__()
        # UI Qt Designer
        self.ui_ppal = ui_ppal
        self.ui_descargar_youtube = uic.loadUi(os.path.join(basedir, "../ui", "descargar_youtube.ui"), self)

        # Personalizar el marco de las ventanas para que solo muestre un título
        self.ui_descargar_youtube.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.current_folder = "/media/jose/90980D73980D58DC/PAPA/Música/Descargas de YouTube"
        #self.current_folder = "/media/libardo/567E18C87E18A333/IDEAFIX/DescargasYoutube/youtube_download"
        self.calidad_audio = "256k"

        #Elementos ui de configuración
        self.lbl_temp_inicial_min = self.ui_descargar_youtube.lbl_cont_slider_temp_inicial_min
        self.lbl_temp_inicial_seg = self.ui_descargar_youtube.lbl_cont_slider_temp_inicial_seg
        self.slider_temp_inicial_min = self.ui_descargar_youtube.slider_tiempo_inicial_min
        self.slider_temp_inicial_seg = self.ui_descargar_youtube.slider_tiempo_inicial_seg
        self.lbl_temp_final_min = self.ui_descargar_youtube.lbl_cont_slider_temp_final_min
        self.lbl_temp_final_seg = self.ui_descargar_youtube.lbl_cont_slider_temp_final_seg
        self.slider_temp_final_min = self.ui_descargar_youtube.slider_tiempo_final_min
        self.slider_temp_final_seg = self.ui_descargar_youtube.slider_tiempo_final_seg
        self.frame_tiempo_inicial = self.ui_descargar_youtube.frme_tiempo_inicial
        self.frame_tiempo_final = self.ui_descargar_youtube.frme_tiempo_final
        self.check_tiempo_inicial = self.ui_descargar_youtube.check_tiempo_inicial
        self.check_tiempo_final = self.ui_descargar_youtube.check_tiempo_final
        self.input_url = self.ui_descargar_youtube.input_url
        self.btn_pegar = self.ui_descargar_youtube.btn_pegar
        self.btn_borrar = self.ui_descargar_youtube.btn_borrar
        self.btn_descargar = self.ui_descargar_youtube.btn_descargar
        self.titulo_metadata = self.ui_descargar_youtube.input_titulo
        self.artista_metadata = self.ui_descargar_youtube.input_artista
        self.genero_metadata = self.ui_descargar_youtube.input_genero
        self.compositor_metadata = self.ui_descargar_youtube.input_compositor
        self.lbl_progreso = self.ui_descargar_youtube.lbl_progreso

        self.btn_volver = self.ui_descargar_youtube.btn_atras
        self.btn_minimizar = self.ui_descargar_youtube.btn_minimizar
        self.btn_salir = self.ui_descargar_youtube.btn_salir

        #Controladores ui de configuración
        self.frame_tiempo_inicial.setVisible(False)
        self.frame_tiempo_final.setVisible(False)
        # self.lbl_progreso.setVisible(False)
        self.check_tiempo_inicial.stateChanged.connect(self.habilitar_tiempo_inicial)
        self.check_tiempo_final.stateChanged.connect(self.habilitar_tiempo_final)
        self.btn_pegar.clicked.connect(lambda: self.pegar_texto(self.input_url))
        self.btn_borrar.clicked.connect(lambda: self.borrar_url(self.input_url))
        self.btn_descargar.clicked.connect(self.start_stop_download)

        self.input_url.setFocus()
        self.btn_volver.clicked.connect(self.volver_function)
        self.btn_minimizar.clicked.connect(self.ui_descargar_youtube.showMinimized)
        self.btn_salir.clicked.connect(self.salir_function)

        # Conectar la señal valueChanged del slider a la función actualizar_label
        self.slider_temp_inicial_min.valueChanged.connect(self.actualizar_lbl_temp_inicial_min)
        self.slider_temp_inicial_seg.valueChanged.connect(self.actualizar_lbl_temp_inicial_seg)
        self.slider_temp_final_min.valueChanged.connect(self.actualizar_lbl_temp_final_min)
        self.slider_temp_final_seg.valueChanged.connect(self.actualizar_lbl_temp_final_seg)

        self.download_thread = None

    def actualizar_lbl_temp_inicial_min(self, valor):
        # Actualizar el texto del QLabel con el valor actual del QSlider
        self.lbl_temp_inicial_min.setText(f"Minuto: {valor}")

    def actualizar_lbl_temp_inicial_seg(self, valor):
        # Actualizar el texto del QLabel con el valor actual del QSlider
        self.lbl_temp_inicial_seg.setText(f"Segundo: {valor}")

    def actualizar_lbl_temp_final_min(self, valor):
        # Actualizar el texto del QLabel con el valor actual del QSlider
        self.lbl_temp_final_min.setText(f"Minuto: {valor}")

    def actualizar_lbl_temp_final_seg(self, valor):
        # Actualizar el texto del QLabel con el valor actual del QSlider
        self.lbl_temp_final_seg.setText(f"Segundo: {valor}")

    def habilitar_tiempo_inicial(self, state):
        if state == 2:  # 2 representa el estado "activado" (checked)
            self.frame_tiempo_inicial.setVisible(True)
        else:
            self.frame_tiempo_inicial.setVisible(False)

    def habilitar_tiempo_final(self, state):
        if state == 2:  # 2 representa el estado "activado" (checked)
            self.frame_tiempo_final.setVisible(True)
        else:
            self.frame_tiempo_final.setVisible(False)

    def pegar_texto(self, input_url):
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        input_url.setText(clipboard_text)

    def obtener_url(self):
        texto = self.input_url.text()
        return texto

    def borrar_url(self, input_url):
        input_url.clear()
    
    def borrar_metadatos(self):
        self.titulo_metadata.clear()
        self.artista_metadata.clear()
        self.genero_metadata.clear()
        self.compositor_metadata.clear()
        self.input_url.setFocus()

    def eliminar_punto_final(self, cadena):
        if cadena.endswith('.'):
            cadena = cadena[:-1]
        return cadena

    def validar_titulo(self):
        titulo = self.eliminar_punto_final(self.titulo_metadata.text())
        return titulo

    def validar_url_youtube(self, texto):
        if texto.startswith("https://www.youtube.com/"):
            return True
        else:
            return False

    def mostrar_mensaje(self, mensaje):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Mensaje')
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(mensaje)
        msg_box.setStyleSheet('background-color: white;')
        msg_box.exec_()

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

    def descargar_cancion(self):
        url_youtube = self.obtener_url()
        video_title = self.validar_titulo()
        if self.validar_url_youtube(url_youtube):
            if video_title:
                try:
                    yt = YouTube(url_youtube)
                    audio = yt.streams.filter(only_audio=True).first()
                    if audio:
                        video_artista = self.artista_metadata.text()
                        video_genero = self.genero_metadata.text()
                        video_compositor = self.compositor_metadata.text()
                        audio.download(filename=f"{video_title}.{audio.subtype}", output_path=self.current_folder)
                        archivo_mp4_ruta = os.path.join(self.current_folder, f"{video_title}.{audio.subtype}")
                        archivo_mp3_ruta = os.path.join(self.current_folder, f"{video_title}.mp3")

                        if self.check_tiempo_inicial.isChecked() and self.check_tiempo_final.isChecked():
                            min_inicio = self.slider_tiempo_inicial_min.value()
                            sec_inicio = self.slider_tiempo_inicial_seg.value()
                            min_final = self.slider_tiempo_final_min.value()
                            sec_final = self.slider_tiempo_final_seg.value()
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
                                        'metadata:g:3':f"composer={video_compositor}",
                                        }
                                    ).run()
                            else:
                                os.remove(archivo_mp4_ruta)
                                return f"El tiempo de inicio debe ser menor al tiempo final"
                        elif self.check_tiempo_inicial.isChecked():
                            min_inicio = self.slider_tiempo_inicial_min.value()
                            sec_inicio = self.slider_tiempo_inicial_seg.value()
                            start_time = self.tiempo_inicial_func(min_inicio, sec_inicio)
                            ffmpeg.input(archivo_mp4_ruta).output(
                                archivo_mp3_ruta, 
                                audio_bitrate=self.calidad_audio, 
                                ss=start_time,
                                **{ 'metadata:g:0':f"title={video_title}", 
                                    'metadata:g:1':f"artist={video_artista}", 
                                    'metadata:g:2':f"genre={video_genero}",
                                    'metadata:g:3':f"composer={video_compositor}",
                                    }
                                ).run()
                        elif self.check_tiempo_final.isChecked():
                            min_final = self.slider_tiempo_final_min.value()
                            sec_final = self.slider_tiempo_final_seg.value()
                            end_time = self.tiempo_final_func(min_final, sec_final)
                            ffmpeg.input(archivo_mp4_ruta).output(
                                archivo_mp3_ruta, 
                                audio_bitrate=self.calidad_audio, 
                                to=end_time,
                                **{ 'metadata:g:0':f"title={video_title}", 
                                    'metadata:g:1':f"artist={video_artista}", 
                                    'metadata:g:2':f"genre={video_genero}",
                                    'metadata:g:3':f"composer={video_compositor}",
                                    }
                                ).run()
                        else:
                            ffmpeg.input(archivo_mp4_ruta).output(
                                archivo_mp3_ruta, 
                                audio_bitrate=self.calidad_audio,
                                **{ 'metadata:g:0':f"title={video_title}", 
                                    'metadata:g:1':f"artist={video_artista}", 
                                    'metadata:g:2':f"genre={video_genero}",
                                    'metadata:g:3':f"composer={video_compositor}",
                                    }
                                ).run()
                        os.remove(archivo_mp4_ruta)
                        self.borrar_url(self.input_url)
                        self.borrar_metadatos()
                        return (f"DESCARGA EXITOSA: \n{video_title}")
                    else:
                        self.mostrar_mensaje("No se encontró un archivo de audio disponible.")
                except Exception as e:
                    self.mostrar_mensaje(f"Error al descargar: {str(e)}")
            else:
                self.mostrar_mensaje("Agregue un título a la canción.")
        else:
            self.mostrar_mensaje("La URL de YouTube no es válida.")

    def start_stop_download(self):
        self.url_youtube = self.obtener_url()
        self.video_title = self.validar_titulo()
        self.video_artista = self.artista_metadata.text()
        self.video_genero = self.genero_metadata.text()
        self.video_compositor = self.compositor_metadata.text()
        
        if self.download_thread is None or not self.download_thread.isRunning():

            if self.validar_url_youtube(self.url_youtube):
                if self.video_title:
                     # Crear e iniciar un nuevo hilo de descarga
                    self.download_thread = DownloadThread(
                        self.url_youtube, 
                        self.check_tiempo_inicial,
                        self.check_tiempo_final,
                        self.current_folder,
                        self.calidad_audio,
                        self.video_title,
                        self.video_artista,
                        self.video_genero,
                        self.video_compositor,
                        )
                    self.download_thread.progress_signal.connect(self.update_progress)
                    self.download_thread.download_finished_signal.connect(self.download_finished)
                    self.download_thread.start()
                    #self.lbl_progreso.setText('Descargando...')

                else:
                    self.mostrar_mensaje("Agregue un título a la canción.")
            else:
                self.mostrar_mensaje("La URL de YouTube no es válida.")
        else:
            # Detener la descarga
            self.download_thread.stop()
            self.download_thread.wait()  # Esperar a que el hilo se detenga completamente
            #self.lbl_progreso.setText('Iniciar Descarga')

    def update_progress(self, value):
        time.sleep(0.5)
        while True:
            for i in range(1, 11):
                self.lbl_progreso.setText(f"{'*' * i}")
                time.sleep(0.5)
            time.sleep(0.5)

    def download_finished(self):
        # Método que se llama cuando la descarga ha finalizado
        self.lbl_progreso.setText('')
        self.borrar_url(self.input_url)
        self.borrar_metadatos()
        # return (f"DESCARGA EXITOSA: \n{self.video_title}")
        self.mostrar_mensaje(f"DESCARGA EXITOSA: \n{self.video_title}")

    def volver_function(self):
        print("Volver al menú principal")
        self.pos_ventana = self.ui_descargar_youtube.pos()
        self.ui_descargar_youtube.hide()
        self.ui_ppal.move(self.pos_ventana)
        self.ui_ppal.show()

    def salir_function(self):
        self.ui_ppal.salir_function()