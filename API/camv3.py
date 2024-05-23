import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import cv2
import requests

import PySpin
os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

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

        self.close_button = QPushButton("Close Application")
        self.close_button.clicked.connect(self.close_event)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.camera_label)
        layout.addWidget(self.capture_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.close_button)

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
        self.num_cameras = self.cam_list.GetSize()
        for i, cam in enumerate(self.cam_list):
            self.cam = cam.Init()
            self.nodemap = self.cam.GetNodeMap()
        try:
            node_pixel_format = PySpin.CEnumerationPtr(self.nodemap.GetNode('PixelFormat'))
            if PySpin.IsAvailable(node_pixel_format) and PySpin.IsWritable(node_pixel_format):
                # Retrieve the desired entry node from the enumeration node
                node_pixel_format_BayerRG16 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName('BayerRG8'))
                if PySpin.IsAvailable(node_pixel_format_BayerRG16) and PySpin.IsReadable(node_pixel_format_BayerRG16):
                    # Retrieve the integer value from the entry node
                    pixel_format_BayerRG16 = node_pixel_format_BayerRG16.GetValue()
                    # Set integer as new value for enumeration node
                    node_pixel_format.SetIntValue(pixel_format_BayerRG16)
                    print('Pixel format set to %s...' % node_pixel_format.GetCurrentEntry().GetSymbolic())
                else:
                    print('Pixel format BayerRG16 not available...')
            else:
                print('Pixel format not available...')   

            self.cam.BeginAcquisition()
              

        except:
            print("Error.")       
        #--------------------------------------------------#
        self.timer.start(100)  # Update every 30 milliseconds

    def update_frame(self):
        # ret, frame = self.cap.read()
        #Read camera
        frame = self.cam.GetNextImage(1000)
        frame_data = frame.GetNDArray()
        frame = cv2.cvtColor(frame_data, cv2.COLOR_BayerRG2RGB)

        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        self.camera_label.setPixmap(pixmap.scaled(self.camera_label.size(), Qt.KeepAspectRatio))

        frame.Release()
    def capture_and_send(self):
        # ret, frame = self.cap.read()
        frame = self.cam.GetNextImage(1000)
        frame_data = frame.GetNDArray()
        frame = cv2.cvtColor(frame_data, cv2.COLOR_BayerRG2RGB)

        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post('http://127.0.0.1:5000/detect', data=img_encoded.tobytes())
        if response.status_code == 200:
            img_bytes = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes)
            self.result_label.setPixmap(pixmap.scaled(self.result_label.size(), Qt.KeepAspectRatio))

    def close_event(self):

        self.cam.EndAcquisition()
        # Deinitialize camera
        self.cam.DeInit()
        del self.cam
        self.cam_list.Clear()
        self.system.ReleaseInstance()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = CameraGUI()
    gui.show()
    sys.exit(app.exec_())
