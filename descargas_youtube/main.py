import sys, os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow
from PyQt5.QtCore import Qt

from src.descargar_youtube import Descargar_Youtube_UI
from src.conversor_mp3 import Conversor_mp3_UI

basedir = os.path.dirname(__file__)

class Iniciar_UI(QMainWindow):
	def __init__(self):
		super().__init__()
		# UI Qt Designer
		self.ui_ppal = uic.loadUi(os.path.join(basedir, "ui", "principal.ui"), self)
		self.ui_descargar_youtube = Descargar_Youtube_UI(self.ui_ppal)
		self.ui_conversor_mp3 = Conversor_mp3_UI(self.ui_ppal)

		# Personalizar el marco de las ventanas para que solo muestre un título
		self.ui_ppal.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

		# Elementos ui principal
		self.btn_descargar_youtube = self.ui_ppal.btn_descarga_youtube
		self.btn_conversor_mp3 = self.ui_ppal.btn_conversor_mp3
		self.btn_minimizar = self.ui_ppal.btn_minimizar
		self.btn_salir = self.ui_ppal.btn_salir

		#Controladores ui principal
		self.btn_descargar_youtube.clicked.connect(self.descargar_youtube_function)
		self.btn_conversor_mp3.clicked.connect(self.conversor_mp3_function)
		self.btn_minimizar.clicked.connect(self.ui_ppal.showMinimized)
		self.btn_salir.clicked.connect(self.salir_function)

		#Iniciar con el botón "PARAR" deshabilitado
		# self.btn_parar.setEnabled(False)

    #Función para ir a la ventana de descargar de youtube
	def descargar_youtube_function(self):
		print("Descargar de Youtube")
		self.pos_ventana = self.ui_ppal.pos()
		self.ui_ppal.hide()
		self.ui_descargar_youtube.move(self.pos_ventana)
		self.ui_descargar_youtube.show()
		
    #Función para ir a la ventana de conversor mp3
	def conversor_mp3_function(self):
		print("Conversor mp3")
		self.pos_ventana = self.ui_ppal.pos()
		self.ui_ppal.hide()
		self.ui_conversor_mp3.move(self.pos_ventana)
		self.ui_conversor_mp3.show()
		
    #Función que finaliza la aplicación - Salir
	def salir_function(self):
		self.btn_salir.setEnabled(False)
		try:
			# Enviar la señal para detener el hilo
			self.thread.buscar_msjes = False
			self.thread.wait()
			print("Thread cerrado correctamente")
		except:
			print("No hay Threads abiertos")
		print("Finalizando")
		sys.exit()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Iniciar_UI()
	# Obtener el tamaño de la pantalla
	screen = QDesktopWidget().screenGeometry()
	# Obtener el tamaño de la ventana
	size = window.geometry()
	# Calcular la posición para centrado en la pantalla
	x = int((screen.width() - size.width()) / 2)
	y = int((screen.height() - size.height()) / 2)
	# Mover la ventana a la posición calculada
	window.move(x, y)
	window.show()
	sys.exit(app.exec_())