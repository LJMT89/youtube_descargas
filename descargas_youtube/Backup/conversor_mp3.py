import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
import ffmpeg
import os

class ConvertidorWmaMp3:
    def __init__(self):
        self.archivo_wma_ruta = None
        self.calidad_audio = '256k'

    def seleccionar_carpeta(self):
        carpeta_seleccionada = QFileDialog.getExistingDirectory(None, "Seleccionar carpeta", "/media/jose/90980D73980D58DC/PAPA/Música")
        if carpeta_seleccionada:
            self.archivo_wma_ruta = carpeta_seleccionada
            self.convertir_wma_a_mp3()

    def convertir_wma_a_mp3(self):
        if self.archivo_wma_ruta:
            archivos_wma = [f for f in os.listdir(self.archivo_wma_ruta) if f.lower().endswith('.wma')]
            for archivo_wma in archivos_wma:
                try:
                    input_path = os.path.join(self.archivo_wma_ruta, archivo_wma)
                    output_path = os.path.join(self.archivo_wma_ruta, os.path.splitext(archivo_wma)[0] + '.mp3')

                    ffmpeg.input(input_path).output(
                        output_path,
                        audio_bitrate=self.calidad_audio,
                        codec='libmp3lame',
                    ).run()
                    
                    print(f"La conversión de {archivo_wma} a {os.path.splitext(archivo_wma)[0]}.mp3 se ha completado con éxito.")
                except ffmpeg.Error as e:
                    print(f"Error durante la conversión de {archivo_wma}: {e.stderr}")

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Convertidor WMA a MP3')
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel('Selecciona la carpeta con archivos WMA:')
        self.btn_seleccionar_carpeta = QPushButton('Seleccionar Carpeta', self)
        self.btn_seleccionar_carpeta.clicked.connect(self.seleccionar_carpeta)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn_seleccionar_carpeta)

        self.convertidor = ConvertidorWmaMp3()

    def seleccionar_carpeta(self):
        self.convertidor.seleccionar_carpeta()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = App()
    ventana.show()
    sys.exit(app.exec_())