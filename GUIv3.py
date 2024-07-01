# -*- coding: utf-8 -*-
# System
import base64
import sys
import os
# GUI
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# Image processing
import cv2
import requests
import time
# Camera processing
import PySpin
# Jetson nano pinouts
import Jetson.GPIO as GPIO

# Fix variable
SERVER_ADDRESS = 'https://flaskgg-6otzndbmqa-as.a.run.app'
CAMERA_PIN = 16
LIGHT_PIN = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CAMERA_PIN, GPIO.OUT, initial=GPIO.LOW)
time.sleep(10)
GPIO.setup(LIGHT_PIN, GPIO.OUT, initial=GPIO.LOW)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow): #setupUi i.e fonts, location,....
        self.CAMERA_PWR_IS_ON = True
        self.LIGHT_PWR_IS_ON = True
        # Window initialize
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")

        MainWindow.resize(1366, 768)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Set up fonts
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(16)

        small_font = QFont()
        small_font.setFamily("Arial")
        small_font.setPointSize(10)

        bold_font = QFont()
        bold_font.setFamily("Arial")
        bold_font.setPointSize(16)
        bold_font.setBold(True)
        bold_font.setWeight(75)

        # The lines
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName("line")
        self.line.setGeometry(QRect(1100, 0, 20, 766))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)

        self.line.setFont(font)
        self.line.setMouseTracking(False)
        self.line.setTabletTracking(True)
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(3)
        self.line.setMidLineWidth(3)
        self.line.setFrameShape(QFrame.VLine)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName("line_2")
        self.line_2.setGeometry(QRect(0, 500, 1110, 20))
        self.line_2.setFont(font)
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QFrame.HLine)
        
        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName("line_3")
        self.line_3.setGeometry(QRect(0, 100, 1110, 3))
        self.line_3.setFont(font)
        self.line_3.setFrameShadow(QFrame.Plain)
        self.line_3.setLineWidth(3)
        self.line_3.setFrameShape(QFrame.HLine)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName("line_4")
        self.line_4.setGeometry(QRect(1110, 240, 1110, 20))
        self.line_4.setFont(font)
        self.line_4.setFrameShadow(QFrame.Plain)
        self.line_4.setLineWidth(3)
        self.line_4.setFrameShape(QFrame.HLine)
        
        # Camera feed
        self.camera_feed = QLabel(self.centralwidget)
        self.camera_feed.setObjectName("Camera Feed")
        self.camera_feed.setGeometry(QRect(20, 160, 500, 248))
        self.camera_feed.setFont(font)
        self.camera_feed.setFrameShape(QFrame.Box)
        # self.camera_feed.setPixmap(QPixmap("data/5.PNG"))

        # Result image
        self.image_feed = QLabel(self.centralwidget)
        self.image_feed.setObjectName("Result image")
        self.image_feed.setGeometry(QRect(590, 160, 500, 248))
        self.image_feed.setFont(font)
        self.image_feed.setFrameShape(QFrame.Box)
        # self.image_feed.setPixmap(QPixmap("data/4.PNG"))

        # Camera feed label
        self.camera_feed_label = QLabel(self.centralwidget)
        self.camera_feed_label.setObjectName("Camera Feed Label")
        self.camera_feed_label.setGeometry(QRect(190, 430, 121, 51))
        self.camera_feed_label.setFont(bold_font)
        self.camera_feed_label.setTextFormat(Qt.AutoText)
        self.camera_feed_label.setAlignment(Qt.AlignCenter)

        # Result image label
        self.image_feed_label = QLabel(self.centralwidget)
        self.image_feed_label.setObjectName("Image Feed Label")
        self.image_feed_label.setGeometry(QRect(750, 430, 181, 51))
        self.image_feed_label.setFont(bold_font)
        self.image_feed_label.setLayoutDirection(Qt.LeftToRight)
        self.image_feed_label.setAlignment(Qt.AlignCenter)

        # Send image to classify button
        self.classify_button = QPushButton(self.centralwidget)
        self.classify_button.setObjectName("Classify")
        self.classify_button.setGeometry(QRect(1120, 350, 241, 61))
        self.classify_button.setFont(font)
        self.classify_button.clicked.connect(self.classify)

        # Send image to detect defects button
        self.detect_button = QPushButton(self.centralwidget)
        self.detect_button.setObjectName("Detect")
        self.detect_button.setGeometry(QRect(1120, 420, 241, 61))
        self.detect_button.setFont(font)
        self.detect_button.clicked.connect(self.detect)

        self.turn_off_button = QPushButton(self.centralwidget)
        self.turn_off_button.setObjectName("Turn off")
        self.turn_off_button.setGeometry(QRect(1120, 600, 241, 61))
        self.turn_off_button.setFont(font)
        self.turn_off_button.clicked.connect(self.turn_off)

        # Test result for label
        self.classify_result_section = QLabel(self.centralwidget)
        self.classify_result_section.setObjectName("Classify Section")
        self.classify_result_section.setGeometry(QRect(20, 530, 60, 30))
        self.classify_result_section.setFont(font)

        self.classify_result_text = QLabel(self.centralwidget)
        self.classify_result_text.setObjectName("Classify Text")
        self.classify_result_text.setGeometry(QRect(100, 530, 1000, 100))
        self.classify_result_text.setFont(font)
        self.classify_result_text.setWordWrap(True)
        self.classify_result_text.setAlignment(Qt.AlignTop)
        
        self.detect_result_section = QLabel(self.centralwidget)
        self.detect_result_section.setObjectName("Detect Section")
        self.detect_result_section.setGeometry(QRect(20, 580, 65, 30))
        self.detect_result_section.setFont(font)

        self.detect_result_text = QLabel(self.centralwidget)
        self.detect_result_text.setObjectName("Detect Text")
        self.detect_result_text.setGeometry(QRect(100, 580, 1000, 500))
        self.detect_result_text.setFont(font)
        self.detect_result_text.setWordWrap(True)
        self.detect_result_text.setAlignment(Qt.AlignTop)

        # The trigger button
        self.trigger_camera = QPushButton(self.centralwidget)
        self.trigger_camera.setObjectName("Camera On/Off")
        self.trigger_camera.setGeometry(QRect(1160, 60, 160, 40))
        self.trigger_camera.setFont(font)
        self.trigger_camera.clicked.connect(self.toggle_camera)

        self.trigger_light = QPushButton(self.centralwidget)
        self.trigger_light.setObjectName("Light On/Off")
        self.trigger_light.setGeometry(QRect(1160, 110, 160, 40))
        self.trigger_light.setFont(font)
        self.trigger_light.clicked.connect(self.toggle_light)

        self.camera_temperature = QLabel(self.centralwidget)
        self.camera_temperature.setObjectName("Camera temperature")
        self.camera_temperature.setGeometry(QRect(1160, 160, 160, 40))
        self.camera_temperature.setFont(small_font)

        self.jetson_temperature = QLabel(self.centralwidget)
        self.jetson_temperature.setObjectName("CPU temperature")
        self.jetson_temperature.setGeometry(QRect(1160, 180, 160, 40))
        self.jetson_temperature.setFont(small_font)

        # The capture button
        self.CAPTURE = QPushButton(self.centralwidget)
        self.CAPTURE.setObjectName("Capture Image")
        self.CAPTURE.setGeometry(QRect(1120, 280, 241, 61))
        self.CAPTURE.setFont(font)
        self.CAPTURE.clicked.connect(self.capture_and_display)

        # self.advice_section = QLabel(self.centralwidget)
        # self.advice_section.setObjectName("Advice Section")
        # self.advice_section.setGeometry(QRect(20, 640, 71, 30))
        # self.advice_section.setFont(font)

        # self.advice_content = QLabel(self.centralwidget)
        # self.advice_content.setObjectName("Advice Content")
        # self.advice_content.setGeometry(QRect(100, 640, 500, 30))
        # self.advice_content.setFont(font)

        # Save file button
        # self.Save_file = QPushButton(self.centralwidget)
        # self.Save_file.setObjectName("Save_file")
        # self.Save_file.setGeometry(QRect(1120, 490, 241, 61))
        # self.Save_file.setFont(font)

        # Show saved file button
        # self.file_saved = QPushButton(self.centralwidget)
        # self.file_saved.setObjectName("file_saved")
        # self.file_saved.setGeometry(QRect(1120, 560, 241, 61))
        # self.file_saved.setFont(font)

        # Input for name and ID
        # self.name = QLineEdit(self.centralwidget)
        # self.name.setObjectName("name")
        # self.name.setGeometry(QRect(100, 30, 271, 41))
        # self.name.setFont(font)
        # self.mssv = QLineEdit(self.centralwidget)
        # self.mssv.setObjectName("mssv")
        # self.mssv.setGeometry(QRect(510, 30, 271, 41))
        # self.mssv.setFont(font)
        # self.label_name = QLabel(self.centralwidget)
        # self.label_name.setObjectName("label_name")
        # self.label_name.setGeometry(QRect(10, 40, 81, 21))
        # self.label_name.setFont(font)
        # self.label_mssv = QLabel(self.centralwidget)
        # self.label_mssv.setObjectName("label_mssv")
        # self.label_mssv.setGeometry(QRect(420, 40, 81, 21))
        # self.label_mssv.setFont(font)

        # Submit button
        # self.pushButton_submit = QPushButton(self.centralwidget)
        # self.pushButton_submit.setObjectName("pushButton_submit")
        # self.pushButton_submit.setGeometry(QRect(840, 20, 211, 61))
        # self.pushButton_submit.setFont(font)

        #--------------------------------------------------#
        # Retrieve singleton reference to system object

        #--------------------------------------------------#
        # Set timer for update frame:
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.timeout.connect(self.update_temperature)
        self.timer.start(100)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1366, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.initialize_camera()
        QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow): ## Intergrate the widgets into window
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Camera Capture & Object Detection", None))
        self.camera_feed.setText("")
        self.image_feed.setText("")
        self.camera_feed_label.setText(QCoreApplication.translate("MainWindow", "Camera", None))
        self.image_feed_label.setText(QCoreApplication.translate("MainWindow", "Image result", None))

        self.classify_button.setText(QCoreApplication.translate("MainWindow", "Classify", None))
        self.detect_button.setText(QCoreApplication.translate("MainWindow", "Detect Defect", None))

        self.classify_result_section.setText(QCoreApplication.translate("MainWindow", "Class:", None))
        self.detect_result_section.setText(QCoreApplication.translate("MainWindow", "Advice:", None))
        self.classify_result_text.setText(QCoreApplication.translate("MainWindow", "waiting for result", None))
        self.detect_result_text.setText(QCoreApplication.translate("MainWindow", "waiting for result", None))

        self.trigger_camera.setText(QCoreApplication.translate("MainWindow", "Camera On/Off", None))
        self.trigger_light.setText(QCoreApplication.translate("MainWindow", "Light On/Off", None))
        self.camera_temperature.setText(QCoreApplication.translate("MainWindow", "Camera temperature:", None))
        self.jetson_temperature.setText(QCoreApplication.translate("MainWindow", "CPU temperature:", None))

        self.CAPTURE.setText(QCoreApplication.translate("MainWindow", "CAPTURE", None))

        # self.Save_file.setText(QCoreApplication.translate("MainWindow", "Save file", None))
        # self.file_saved.setText(QCoreApplication.translate("MainWindow", "Open saved file", None))
        # self.label_name.setText(QCoreApplication.translate("MainWindow", "NAME:", None))
        # self.label_mssv.setText(QCoreApplication.translate("MainWindow", "MSSV:", None))
        # self.pushButton_submit.setText(QCoreApplication.translate("MainWindow", "Submit", None))
        
    def initialize_camera(self):
        self.system = PySpin.System.GetInstance()
        # Retrieve list of cameras from the system
        self.cam_list = self.system.GetCameras()
        # for i, self.cam in enumerate(self.cam_list):
        self.cam = self.cam_list.GetByIndex(0) # Theres only 1 camera
        self.cam.Init()
        self.nodemap = self.cam.GetNodeMap()  
        try:
            node_jumbo_package = PySpin.CIntegerPtr(self.nodemap.GetNode('GevSCPSPacketSize'))
            node_jumbo_package.SetValue(9000)

            node_width = PySpin.CIntegerPtr(self.nodemap.GetNode('Width'))
            node_width.SetValue(744)

            node_height = PySpin.CIntegerPtr(self.nodemap.GetNode('Height'))
            node_height.SetValue(300)

            node_offsetX = PySpin.CIntegerPtr(self.nodemap.GetNode('OffsetX'))
            node_offsetX.SetValue(480)

            node_offsetY = PySpin.CIntegerPtr(self.nodemap.GetNode('OffsetY'))
            node_offsetY.SetValue(390)

            node_pixel_format = PySpin.CEnumerationPtr(self.nodemap.GetNode('PixelFormat'))
            node_pixel_format_RGB = node_pixel_format.GetEntryByName('RGB8Packed')
            node_pixel_format.SetIntValue(node_pixel_format_RGB.GetValue())

            node_acquisition_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
            node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
            node_acquisition_mode.SetIntValue(node_acquisition_mode_continuous.GetValue())
        except:
            print("Cannot set mode!") 
        self.cam.BeginAcquisition()

    def clean_up_camera(self):
        self.cam.EndAcquisition()
        self.cam.DeInit()
        del self.cam
        self.cam_list.Clear()
        self.system.ReleaseInstance()

    def toggle_camera(self):
        if self.CAMERA_PWR_IS_ON == True:
            self.CAMERA_PWR_IS_ON = False
            # self.clean_up_camera()
            # time.sleep(3)
            GPIO.output(CAMERA_PIN, GPIO.HIGH)
            # time.sleep(10)
        else:
            self.CAMERA_PWR_IS_ON = True
            GPIO.output(CAMERA_PIN, GPIO.LOW)
            time.sleep(15)
            self.initialize_camera()
    def toggle_light(self):
        if self.LIGHT_PWR_IS_ON == True:
            GPIO.output(LIGHT_PIN, GPIO.HIGH)
            self.LIGHT_PWR_IS_ON = False
        else:
            GPIO.output(LIGHT_PIN, GPIO.LOW)
            self.LIGHT_PWR_IS_ON = True
    
    def update_frame(self):
        #Read camera
        try:
            display_frame = self.cam.GetNextImage(1000)
            display_frame_data = display_frame.GetNDArray()
            # h = 1200, w = 1600, ch = 3, byte per line = ch*w
            Qt_format = QImage(display_frame_data, 744, 300, QImage.Format_RGB888)
            pixmap_format = QPixmap.fromImage(Qt_format)
            self.camera_feed.setPixmap(pixmap_format.scaled(self.camera_feed.size(), Qt.KeepAspectRatio))
        except:
            print("Waiting for camera")
    def update_temperature(self):
        try:
            node_temperature = PySpin.CFloatPtr(self.nodemap.GetNode("DeviceTemperature"))
            with open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r') as temp_file:
                jetson_temp = temp_file.read().strip()
            self.jetson_temperature.setText(
                QCoreApplication.translate("MainWindow", "CPU temperature: {:.2f} °C".format(float(jetson_temp) / 1000.0), None)
            )
            self.camera_temperature.setText(
                QCoreApplication.translate("MainWindow", "Camera temperature: {:.2f} °C".format(node_temperature.GetValue()), None)
            )
        except:
            print("Wating for camera...")
        
        return
    def detect(self):
        # if self.prediction == "C" or self.prediction == "D":
        #     self.label_2.setText(QCoreApplication.translate("MainWindow", "Class C and D does not have to detect defects", None))
        #     return
        _, img_encoded = cv2.imencode('.jpg', self.capture_frame_data)
        response = requests.post(f'{SERVER_ADDRESS}/detect', data=img_encoded.tobytes())
        if response.status_code == 200:
            data = response.json()
            advice = data['advice']
            img_base64 = data['image']
            img_bytes = base64.b64decode(img_base64)
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes)
            self.image_feed.setPixmap(pixmap.scaled(self.image_feed.size(), Qt.KeepAspectRatio))
            self.detect_result_text.setText(f'{advice}')
    def capture_and_display(self):
        capture_frame = self.cam.GetNextImage(1000)
        self.capture_frame_data = capture_frame.GetNDArray()
        _, img_encoded = cv2.imencode('.jpg', self.capture_frame_data)
        response = requests.post(f'{SERVER_ADDRESS}/weld_check', files={'file': img_encoded.tobytes()})
        if response.status_code == 200:
            self.weld_check = response.json().get('weld_check')
            self.classify_result_text.setText(f'{self.weld_check}')        
            
        capture_Qt_format = QImage(self.capture_frame_data, 744, 300, QImage.Format_RGB888)
        capture_pixmap_format = QPixmap.fromImage(capture_Qt_format)
        self.image_feed.setPixmap(capture_pixmap_format.scaled(self.image_feed.size(), Qt.KeepAspectRatio))

    def classify(self): # Send and return image from classification task
        _, img_encoded = cv2.imencode('.jpg', self.capture_frame_data)
        response = requests.post(f'{SERVER_ADDRESS}/classify', files={'file': img_encoded.tobytes()})
        if response.status_code == 200:
            self.prediction = response.json().get('prediction', 'Error')
            self.classify_result_text.setText(f'{self.prediction}')

    def turn_off(self):
        os.system("sudo shutdown now")
    def closeEvent(self, event):
        self.cam.EndAcquisition()
        # Deinitialize camera
        self.cam.DeInit()
        del self.cam
        self.cam_list.Clear()
        self.system.ReleaseInstance()
        event.accept()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

