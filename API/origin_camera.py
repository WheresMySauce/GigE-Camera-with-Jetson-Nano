import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import cv2
import requests

class CameraGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera Capture & Object Detection")
        self.resize(800, 600)

        # UI Elements
        self.camera_label = QLabel("Camera Feed")
        self.camera_label.setAlignment(Qt.AlignCenter)

        self.capture_button = QPushButton("Capture & Detect")
        self.capture_button.clicked.connect(self.capture_and_send)

        self.result_label = QLabel("Detection Result")
        self.result_label.setAlignment(Qt.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.camera_label)
        layout.addWidget(self.capture_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

        # Camera Setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.cap = cv2.VideoCapture(0)  # 0 for default camera
        self.timer.start(30)  # Update every 30 milliseconds

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.camera_label.setPixmap(pixmap.scaled(self.camera_label.size(), Qt.KeepAspectRatio))

    def capture_and_send(self):
        ret, frame = self.cap.read()
        if ret:
            _, img_encoded = cv2.imencode('.jpg', frame)
            response = requests.post('http://127.0.0.1:5000/detect', data=img_encoded.tobytes())
            if response.status_code == 200:
                img_bytes = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(img_bytes)
                self.result_label.setPixmap(pixmap.scaled(self.result_label.size(), Qt.KeepAspectRatio))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = CameraGUI()
    gui.show()
    sys.exit(app.exec_())
