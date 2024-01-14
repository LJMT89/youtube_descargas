import sys, os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt

basedir = os.path.dirname(__file__)

class Conversor_mp3_UI(QMainWindow):
    def __init__(self, ui_ppal):
        super().__init__()
        # UI Qt Designer
        self.ui_ppal = ui_ppal
        self.ui_conversor_mp3 = uic.loadUi(os.path.join(basedir, "../ui", "conversor_mp3.ui"), self)

        # Personalizar el marco de las ventanas para que solo muestre un título
        self.ui_conversor_mp3.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        #Elementos ui de configuración
        self.btn_volver = self.ui_conversor_mp3.btn_atras
        self.btn_minimizar = self.ui_conversor_mp3.btn_minimizar
        self.btn_salir = self.ui_conversor_mp3.btn_salir

        #Controladores ui de configuración
        self.btn_volver.clicked.connect(self.volver_function)
        self.btn_minimizar.clicked.connect(self.ui_conversor_mp3.showMinimized)
        self.btn_salir.clicked.connect(self.salir_function)

    def volver_function(self):
        print("Volver al menú principal")
        self.pos_ventana = self.ui_conversor_mp3.pos()
        self.ui_conversor_mp3.hide()
        self.ui_ppal.move(self.pos_ventana)
        self.ui_ppal.show()

    def salir_function(self):
        self.ui_ppal.salir_function()