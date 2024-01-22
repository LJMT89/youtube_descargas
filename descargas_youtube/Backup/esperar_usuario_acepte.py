from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMessageBox, QPushButton
from PyQt5.QtCore import pyqtSignal, QThread, QEventLoop
import time

class MiVentana(QWidget):
    cancion_convertida = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.label = QLabel('Esperando a que el usuario acepte...')

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.show()

    def ejecutar_hilo(self, archivo_wma):
        # Emite la señal para informar al usuario
        self.cancion_convertida.emit(f"La canción {archivo_wma} ya está convertida en formato mp3.")

        # Muestra el cuadro de diálogo modal de manera asíncrona
        self.mostrar_dialogo_asincrono()

        # Continúa con la ejecución del hilo después de que el usuario haya hecho clic en Aceptar
        print(f"Proceso de conversión para {archivo_wma} continuando...")

    def mostrar_dialogo_asincrono(self):
        # Crea un cuadro de diálogo modal
        msg_box = QMessageBox(self)
        msg_box.setText("Haz clic en Aceptar para continuar.")
        msg_box.addButton(QPushButton('Aceptar', self), QMessageBox.AcceptRole)

        # Configura un bucle de eventos para esperar la respuesta del usuario
        loop = QEventLoop()
        msg_box.accepted.connect(loop.quit)

        # Muestra el cuadro de diálogo y espera a que el usuario haga clic en Aceptar
        msg_box.exec_()
        loop.exec_()

class HiloConversion(QThread):
    def __init__(self, ventana, archivo_wma):
        super().__init__()
        self.ventana = ventana
        self.archivo_wma = archivo_wma

    def run(self):
        # Realiza alguna tarea de conversión aquí...

        # Muestra el cuadro de diálogo modal
        self.ventana.ejecutar_hilo(self.archivo_wma)

if __name__ == '__main__':
    app = QApplication([])

    ventana = MiVentana()

    archivo_wma = "mi_cancion.wma"
    hilo_conversion = HiloConversion(ventana, archivo_wma)

    # Inicia el hilo
    hilo_conversion.start()

    app.exec_()
