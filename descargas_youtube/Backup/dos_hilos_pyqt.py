from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
import time

class Worker1(QThread):
    finished = pyqtSignal()

    def run(self):
        for i in range(5):
            time.sleep(1)
            print("Worker1: Doing task", i + 1)
        self.finished.emit()

class Worker2(QThread):
    finished = pyqtSignal()

    def run(self):
        for i in range(5):
            time.sleep(1)
            print("Worker2: Doing task", i + 1)
        self.finished.emit()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker1 = Worker1()
        self.worker2 = Worker2()

        layout = QVBoxLayout()

        btn_start1 = QPushButton("Start Worker1", self)
        btn_start1.clicked.connect(self.start_thread1)
        layout.addWidget(btn_start1)

        btn_start2 = QPushButton("Start Worker2", self)
        btn_start2.clicked.connect(self.start_thread2)
        layout.addWidget(btn_start2)

        btn_stop1 = QPushButton("Stop Worker1", self)
        btn_stop1.clicked.connect(self.stop_thread1)
        layout.addWidget(btn_stop1)

        btn_stop2 = QPushButton("Stop Worker2", self)
        btn_stop2.clicked.connect(self.stop_thread2)
        layout.addWidget(btn_stop2)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Conectar las señales de finalización de los workers a los métodos stop_thread1 y stop_thread2
        self.worker1.finished.connect(self.stop_thread1)
        self.worker2.finished.connect(self.stop_thread2)

    def start_thread1(self):
        self.worker1.start()

    def stop_thread1(self):
        if self.worker1.isRunning():
            self.worker1.terminate()
            self.worker1.wait()

    def start_thread2(self):
        self.worker2.start()

    def stop_thread2(self):
        if self.worker2.isRunning():
            self.worker2.terminate()
            self.worker2.wait()

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()
