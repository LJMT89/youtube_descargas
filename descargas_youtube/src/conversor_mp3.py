import os, time, ffmpeg
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject

basedir = os.path.dirname(__file__)

class WorkerProgress(QObject):
    finalizar_progreso = pyqtSignal()
    actualizar_progreso = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.stopped = False

    def run(self):
        time.sleep(0.5)
        while not self.stopped:
            for i in range(1, 11):
                if self.stopped:
                    break
                self.actualizar_progreso.emit(f"{'*' * i}")
                time.sleep(0.5)
            if self.stopped:
                break
            self.actualizar_progreso.emit("")
            time.sleep(0.5)
        self.finalizar_progreso.emit()

    def stop(self):
        self.stopped = True

class WorkerConvertMp3(QObject):
    finalizar_conversion = pyqtSignal()

    def __init__(self):
        super().__init__()

class ConvertidorWmaMp3UI(QMainWindow):
    def __init__(self, ui_ppal):
        super().__init__()
        # UI Qt Designer
        self.ui_ppal = ui_ppal
        self.ui_conversor_mp3 = uic.loadUi(os.path.join(basedir, "../ui", "conversor_mp3.ui"), self)

        # Personalizar el marco de las ventanas para que solo muestre un título
        self.ui_conversor_mp3.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.carpeta_actual = None
        self.calidad_audio = '256k'
        self.archivos = list()
        self.archivos_wma = list()

        #Elementos ui de configuración
        self.btn_sel_carpeta = self.ui_conversor_mp3.btn_sel_carpeta
        self.btn_convertir = self.ui_conversor_mp3.btn_convertir
        self.lbl_canciones_seleccionadas = self.ui_conversor_mp3.lbl_canciones_seleccionadas

        self.btn_volver = self.ui_conversor_mp3.btn_atras
        self.btn_minimizar = self.ui_conversor_mp3.btn_minimizar
        self.btn_salir = self.ui_conversor_mp3.btn_salir

        #Controladores ui de configuración
        self.btn_sel_carpeta.clicked.connect(self.seleccionar_carpeta)
        self.btn_convertir.clicked.connect(self.convertir_wma_a_mp3_hilo)
        self.btn_convertir.setEnabled(False)

        self.btn_volver.clicked.connect(self.volver_function)
        self.btn_minimizar.clicked.connect(self.ui_conversor_mp3.showMinimized)
        self.btn_salir.clicked.connect(self.salir_function)

    def ejecutar_hilos(self):
        self.barra_progreso_hilo()
        self.convertir_wma_a_mp3_hilo()

    def parar_hilo_progreso(self):
        self.worker_progreso.stop()

    def update_status_label(self, message):
        # Método que se llama para actualizar el QLabel desde el hilo secundario
        self.lbl_progreso.setText(message)

    def barra_progreso_hilo(self):
        self.thread_progreso = QThread()
        # Step 3: Create a worker object
        self.worker_progreso = WorkerProgress()
        # Step 4: Move worker to the thread
        self.worker_progreso.moveToThread(self.thread_progreso)
        # Step 5: Connect signals and slots
        self.thread_progreso.started.connect(self.worker_progreso.run)
        self.worker_progreso.finalizar_progreso.connect(self.thread_progreso.quit)
        self.worker_progreso.finalizar_progreso.connect(self.worker_progreso.deleteLater)
        self.thread_progreso.finished.connect(self.thread_progreso.deleteLater)
        self.worker_progreso.update_signal.connect(self.update_status_label)
        # Step 6: Start the thread
        self.thread_progreso.start()

        self.thread_progreso.finished.connect(
            lambda: self.lbl_progreso.setText("")
        )

    def seleccionar_carpeta(self):
        carpeta_seleccionada = QFileDialog.getExistingDirectory(None, "Seleccionar carpeta", "/media/jose/90980D73980D58DC/PAPA/Música")
        if carpeta_seleccionada:
            self.carpeta_actual = carpeta_seleccionada
            self.archivos = os.listdir(self.carpeta_actual)
            self.archivos_wma = [f for f in os.listdir(self.carpeta_actual) if f.lower().endswith('.wma')]
            self.lbl_canciones_seleccionadas.setText("\n".join(self.archivos_wma))
            self.lbl_canciones_convertidas.setText("")
        
        if self.archivos_wma:
            self.btn_convertir.setEnabled(True)
        else:
            self.btn_convertir.setEnabled(False)
            self.mostrar_mensaje("No hay archivos seleccionados")

    def convertir_wma_a_mp3_hilo(self):
        canciones_convertidas_list = list()
        for archivo_wma in self.archivos_wma:
            try:
                input_path = os.path.join(self.carpeta_actual, archivo_wma)
                cancion_mp3 = os.path.splitext(archivo_wma)[0] + '.mp3'
                output_path = os.path.join(self.carpeta_actual, cancion_mp3)
                
                if not cancion_mp3 in self.archivos:
                    self.btn_convertir.setEnabled(False)
                    ffmpeg.input(input_path).output(
                        output_path,
                        audio_bitrate=self.calidad_audio,
                        codec='libmp3lame',
                    ).run()
                    canciones_convertidas_list.append(cancion_mp3)
                    print(f"La conversión de {archivo_wma} a {os.path.splitext(archivo_wma)[0]}.mp3 se ha completado con éxito.")
                else:
                    self.mostrar_mensaje(f"La canción {archivo_wma} ya está convertida en formato mp3.")
            except ffmpeg.Error as e:
                print(f"Error durante la conversión de {archivo_wma}: {e.stderr}")
        self.lbl_canciones_convertidas.setText("\n".join(canciones_convertidas_list))

    def mostrar_mensaje(self, mensaje):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Mensaje')
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(mensaje)
        msg_box.setStyleSheet('background-color: white;')
        msg_box.exec_()
    
    def volver_function(self):
        print("Volver al menú principal")
        self.pos_ventana = self.ui_conversor_mp3.pos()
        self.ui_conversor_mp3.hide()
        self.ui_ppal.move(self.pos_ventana)
        self.ui_ppal.show()

    def salir_function(self):
        self.ui_ppal.salir_function()