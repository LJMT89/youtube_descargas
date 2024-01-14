import sys, os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt

basedir = os.path.dirname(__file__)

class Descargar_Youtube_UI(QMainWindow):
    def __init__(self, ui_ppal):
        super().__init__()
        # UI Qt Designer
        self.ui_ppal = ui_ppal
        self.ui_descargar_youtube = uic.loadUi(os.path.join(basedir, "../ui", "descargar_youtube.ui"), self)

        # Personalizar el marco de las ventanas para que solo muestre un título
        self.ui_descargar_youtube.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

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

        self.btn_volver = self.ui_descargar_youtube.btn_atras
        self.btn_minimizar = self.ui_descargar_youtube.btn_minimizar
        self.btn_salir = self.ui_descargar_youtube.btn_salir

        #Controladores ui de configuración
        self.frame_tiempo_inicial.setVisible(False)
        self.frame_tiempo_final.setVisible(False)
        self.btn_volver.clicked.connect(self.volver_function)
        self.btn_minimizar.clicked.connect(self.ui_descargar_youtube.showMinimized)
        self.btn_salir.clicked.connect(self.salir_function)

        # Conectar la señal valueChanged del slider a la función actualizar_label
        self.slider_temp_inicial_min.valueChanged.connect(self.actualizar_lbl_temp_inicial_min)
        self.slider_temp_inicial_seg.valueChanged.connect(self.actualizar_lbl_temp_inicial_seg)
        self.slider_temp_final_min.valueChanged.connect(self.actualizar_lbl_temp_final_min)
        self.slider_temp_final_seg.valueChanged.connect(self.actualizar_lbl_temp_final_seg)

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

    
    def volver_function(self):
        print("Volver al menú principal")
        self.pos_ventana = self.ui_descargar_youtube.pos()
        self.ui_descargar_youtube.hide()
        self.ui_ppal.move(self.pos_ventana)
        self.ui_ppal.show()

    def salir_function(self):
        self.ui_ppal.salir_function()