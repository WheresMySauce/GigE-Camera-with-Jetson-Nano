import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import cv2
import requests

import PySpin
# os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

class CameraGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera Capture & Object Detection")
        self.resize(1300,700)

        # UI Elements
        self.camera_label = QLabel("Camera Feed")
        self.camera_label.setAlignment(Qt.AlignCenter)

        self.detect_button = QPushButton("Detect")
        self.detect_button.clicked.connect(self.detect_result)

        self.result_label = QLabel("Detection Result")
        self.result_label.setAlignment(Qt.AlignCenter)

        # self.image_label = QLabel("Text label")
        self.text_label = QLabel('Prediction: ')
        self.text_label.setAlignment(Qt.AlignCenter)
        self.classsify_button = QPushButton('Classify')
        self.classsify_button.clicked.connect(self.classify_result)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.camera_label)
        layout.addWidget(self.detect_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.text_label)
        layout.addWidget(self.classsify_button)

        self.setLayout(layout)


        # Camera Setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        # self.cap = cv2.VideoCapture(0)  # 0 for default camera
        #--------------------------------------------------#

        # Retrieve singleton reference to system object
        self.system = PySpin.System.GetInstance()

        # Retrieve list of cameras from the system
        self.cam_list = self.system.GetCameras()

        for i, self.cam in enumerate(self.cam_list):
            self.cam.Init()
            self.nodemap = self.cam.GetNodeMap()
            try:  
                node_jumbo_package = PySpin.CIntegerPtr(self.nodemap.GetNode('GevSCPSPacketSize'))
                node_jumbo_package.SetValue(9000)

                node_pixel_format = PySpin.CEnumerationPtr(self.nodemap.GetNode('PixelFormat'))
                node_pixel_format_RGB = node_pixel_format.GetEntryByName('RGB8Packed')
                node_pixel_format.SetIntValue(node_pixel_format_RGB.GetValue())

                node_acquisition_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
                node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
                node_acquisition_mode.SetIntValue(node_acquisition_mode_continuous.GetValue())
            except:
                print("Cannot set mode.")   
            self.cam.BeginAcquisition()    
        #--------------------------------------------------#
        self.timer.start(100)  # Update every 30 milliseconds

    def update_frame(self):
        # ret, frame = self.cap.read()
        #Read camera
        display_frame = self.cam.GetNextImage(1000)
        display_frame_data = display_frame.GetNDArray()

        # color_image = cv2.cvtColor(display_frame_data, cv2.COLOR_BGR2RGB)
        # h = 1200, w = 1600, ch = 3, byte per line = ch*w
        Qt_format = QImage(display_frame_data, 1600, 1200, QImage.Format_RGB888)
        pixmap_format = QPixmap.fromImage(Qt_format)
        self.camera_label.setPixmap(pixmap_format.scaled(self.camera_label.size(), Qt.KeepAspectRatio))

    def detect_result(self):
        detect_frame = self.cam.GetNextImage(1000)
        detect_frame_data = detect_frame.GetNDArray()
        # detect_frame_data_color = cv2.cvtColor(detect_frame_data, cv2.COLOR_BGR2RGB)

        _, img_encoded = cv2.imencode('.jpg', detect_frame_data)
        response = requests.post('http://192.168.0.101:5000/detect', data=img_encoded.tobytes())
        if response.status_code == 200:
            img_bytes = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes)
            self.result_label.setPixmap(pixmap.scaled(self.result_label.size(), Qt.KeepAspectRatio))

    def classify_result(self):
        classify_frame = self.cam.GetNextImage(1000)
        classify_frame_data = classify_frame.GetNDArray()
        # color_image = cv2.cvtColor(frame_data, cv2.COLOR_BGR2RGB)

        _, img_encoded = cv2.imencode('.jpg', classify_frame_data)
        response = requests.post('http://192.168.0.101:5000/classify', files={'file': img_encoded.tobytes()})
        if response.status_code == 200:
            prediction = response.json().get('prediction', 'Error')
            self.text_label.setText(f'Prediction: {prediction}')

    def closeEvent(self, event):
        self.cam.EndAcquisition()
        # Deinitialize camera
        self.cam.DeInit()
        del self.cam
        self.cam_list.Clear()
        self.system.ReleaseInstance()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = CameraGUI()
    gui.show()
    sys.exit(app.exec_())
