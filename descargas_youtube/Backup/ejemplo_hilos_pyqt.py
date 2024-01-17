import sys
from time import sleep

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        """Long-running task."""
        for i in range(5):
            sleep(1)
            self.progress.emit(i + 1)
        self.finished.emit()

# Step 1: Create a worker class
class Worker2(QObject):
    finished2 = pyqtSignal()
    progress2 = pyqtSignal(int)

    def run(self):
        """Long-running task."""
        for i in range(5):
            sleep(1)
            self.progress2.emit(i + 1)
        self.finished2.emit()

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running Step: 0")
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel2 = QLabel("Long-Running 2 Step: 0")
        self.stepLabel2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)
        self.longRunningBtn2 = QPushButton("Long-Running Task 2!", self)
        self.longRunningBtn2.clicked.connect(self.runLongTask2)
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.stepLabel2)
        layout.addWidget(self.longRunningBtn)
        layout.addWidget(self.longRunningBtn2)
        self.centralWidget.setLayout(layout)

    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    def reportProgress(self, n):
        self.stepLabel.setText(f"Long-Running Step: {n}")
    
    def reportProgress2(self, n):
        self.stepLabel2.setText(f"Long-Running 2 Step: {n}")

    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )

    def runLongTask2(self):
        # Step 2: Create a QThread object
        self.thread2 = QThread()
        # Step 3: Create a worker object
        self.worker2 = Worker2()
        # Step 4: Move worker to the thread
        self.worker2.moveToThread(self.thread2)
        # Step 5: Connect signals and slots
        self.thread2.started.connect(self.worker2.run)
        self.worker2.finished2.connect(self.thread2.quit)
        self.worker2.finished2.connect(self.worker2.deleteLater)
        self.thread2.finished.connect(self.thread2.deleteLater)
        self.worker2.progress2.connect(self.reportProgress2)
        # Step 6: Start the thread
        self.thread2.start()

        # Final resets
        self.longRunningBtn2.setEnabled(False)
        self.thread2.finished.connect(
            lambda: self.longRunningBtn2.setEnabled(True)
        )
        self.thread2.finished.connect(
            lambda: self.stepLabel2.setText("Long-Running 2 Step: 0")
        )

app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())