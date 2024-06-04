# -*- coding: utf-8 -*-
# System
import sys

# GUI
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Jetson nano pinouts
import Jetson.GPIO as GPIO

# Image processing
import cv2
import requests

# Camera processing
import PySpin

class Ui_MainWindow(object):
    def setupUi(self, MainWindow): #setupUi i.e fonts, location,....
        self.CAMERA_STATE = True

        # Window initialize
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        MainWindow.resize(1366, 768)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        # Set up fonts
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(16)

        small_font = QFont()
        small_font.setFamily(u"Arial")
        small_font.setPointSize(10)

        bold_font = QFont()
        bold_font.setFamily(u"Arial")
        bold_font.setPointSize(16)
        bold_font.setBold(True)
        bold_font.setWeight(75)

        # The lines
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
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
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(0, 500, 1110, 20))
        self.line_2.setFont(font)
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QFrame.HLine)
        
        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(0, 100, 1110, 3))
        self.line_3.setFont(font)
        self.line_3.setFrameShadow(QFrame.Plain)
        self.line_3.setLineWidth(3)
        self.line_3.setFrameShape(QFrame.HLine)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(1110, 240, 1110, 20))
        self.line_4.setFont(font)
        self.line_4.setFrameShadow(QFrame.Plain)
        self.line_4.setLineWidth(3)
        self.line_4.setFrameShape(QFrame.HLine)
        
        # Camera feed
        self.camera_feed = QLabel(self.centralwidget)
        self.camera_feed.setObjectName(u"Camera Feed")
        self.camera_feed.setGeometry(QRect(20, 160, 500, 248))
        self.camera_feed.setFont(font)
        self.camera_feed.setFrameShape(QFrame.Box)
        # self.camera_feed.setPixmap(QPixmap(u"data/5.PNG"))

        # Result image
        self.image_feed = QLabel(self.centralwidget)
        self.image_feed.setObjectName(u"Result image")
        self.image_feed.setGeometry(QRect(590, 160, 500, 248))
        self.image_feed.setFont(font)
        self.image_feed.setFrameShape(QFrame.Box)
        # self.image_feed.setPixmap(QPixmap(u"data/4.PNG"))

        # Camera feed label
        self.camera_feed_label = QLabel(self.centralwidget)
        self.camera_feed_label.setObjectName(u"Camera Feed Label")
        self.camera_feed_label.setGeometry(QRect(190, 430, 121, 51))
        self.camera_feed_label.setFont(bold_font)
        self.camera_feed_label.setTextFormat(Qt.AutoText)
        self.camera_feed_label.setAlignment(Qt.AlignCenter)

        # Result image label
        self.image_feed_label = QLabel(self.centralwidget)
        self.image_feed_label.setObjectName(u"Image Feed Label")
        self.image_feed_label.setGeometry(QRect(750, 430, 181, 51))
        self.image_feed_label.setFont(bold_font)
        self.image_feed_label.setLayoutDirection(Qt.LeftToRight)
        self.image_feed_label.setAlignment(Qt.AlignCenter)

        # Send image to classify button
        self.classify_button = QPushButton(self.centralwidget)
        self.classify_button.setObjectName(u"Classify")
        self.classify_button.setGeometry(QRect(1120, 350, 241, 61))
        self.classify_button.setFont(font)
        self.classify_button.clicked.connect(self.classify)

        # Send image to detect defects button
        self.detect_button = QPushButton(self.centralwidget)
        self.detect_button.setObjectName(u"Detect")
        self.detect_button.setGeometry(QRect(1120, 420, 241, 61))
        self.detect_button.setFont(font)
        self.detect_button.clicked.connect(self.detect)

        # Test result for label
        self.classify_result_section = QLabel(self.centralwidget)
        self.classify_result_section.setObjectName(u"Classify Section")
        self.classify_result_section.setGeometry(QRect(20, 530, 60, 30))
        self.classify_result_section.setFont(font)

        self.classify_result_text = QLabel(self.centralwidget)
        self.classify_result_text.setObjectName(u"Classify Text")
        self.classify_result_text.setGeometry(QRect(100, 530, 491, 30))
        self.classify_result_text.setFont(font)

        self.detect_result_section = QLabel(self.centralwidget)
        self.detect_result_section.setObjectName(u"Detect Section")
        self.detect_result_section.setGeometry(QRect(20, 580, 60, 30))
        self.detect_result_section.setFont(font)

        self.detect_result_text = QLabel(self.centralwidget)
        self.detect_result_text.setObjectName(u"Detect Text")
        self.detect_result_text.setGeometry(QRect(100, 580, 500, 30))
        self.detect_result_text.setFont(font)

        # The trigger button
        self.trigger_camera = QPushButton(self.centralwidget)
        self.trigger_camera.setObjectName(u"Camera On/Off")
        self.trigger_camera.setGeometry(QRect(1160, 60, 160, 40))
        self.trigger_camera.setFont(font)
        self.trigger_camera.clicked.connect(self.toggle_camera)

        self.trigger_light = QPushButton(self.centralwidget)
        self.trigger_light.setObjectName(u"Light On/Off")
        self.trigger_light.setGeometry(QRect(1160, 110, 160, 40))
        self.trigger_light.setFont(font)
        self.trigger_light.clicked.connect(self.toggleLight)

        self.camera_temperature = QLabel(self.centralwidget)
        self.camera_temperature.setObjectName(u"Camera temperature")
        self.camera_temperature.setGeometry(QRect(1160, 160, 160, 40))
        self.camera_temperature.setFont(small_font)

        self.jetson_temperature = QLabel(self.centralwidget)
        self.jetson_temperature.setObjectName(u"CPU temperature")
        self.jetson_temperature.setGeometry(QRect(1160, 180, 160, 40))
        self.jetson_temperature.setFont(small_font)

        # The capture button
        self.CAPTURE = QPushButton(self.centralwidget)
        self.CAPTURE.setObjectName(u"Capture Image")
        self.CAPTURE.setGeometry(QRect(1120, 280, 241, 61))
        self.CAPTURE.setFont(font)
        self.CAPTURE.clicked.connect(self.capture_and_display)

        # self.advice_section = QLabel(self.centralwidget)
        # self.advice_section.setObjectName(u"Advice Section")
        # self.advice_section.setGeometry(QRect(20, 640, 71, 30))
        # self.advice_section.setFont(font)

        # self.advice_content = QLabel(self.centralwidget)
        # self.advice_content.setObjectName(u"Advice Content")
        # self.advice_content.setGeometry(QRect(100, 640, 500, 30))
        # self.advice_content.setFont(font)

        # Save file button
        # self.Save_file = QPushButton(self.centralwidget)
        # self.Save_file.setObjectName(u"Save_file")
        # self.Save_file.setGeometry(QRect(1120, 490, 241, 61))
        # self.Save_file.setFont(font)

        # Show saved file button
        # self.file_saved = QPushButton(self.centralwidget)
        # self.file_saved.setObjectName(u"file_saved")
        # self.file_saved.setGeometry(QRect(1120, 560, 241, 61))
        # self.file_saved.setFont(font)

        # Input for name and ID
        # self.name = QLineEdit(self.centralwidget)
        # self.name.setObjectName(u"name")
        # self.name.setGeometry(QRect(100, 30, 271, 41))
        # self.name.setFont(font)
        # self.mssv = QLineEdit(self.centralwidget)
        # self.mssv.setObjectName(u"mssv")
        # self.mssv.setGeometry(QRect(510, 30, 271, 41))
        # self.mssv.setFont(font)
        # self.label_name = QLabel(self.centralwidget)
        # self.label_name.setObjectName(u"label_name")
        # self.label_name.setGeometry(QRect(10, 40, 81, 21))
        # self.label_name.setFont(font)
        # self.label_mssv = QLabel(self.centralwidget)
        # self.label_mssv.setObjectName(u"label_mssv")
        # self.label_mssv.setGeometry(QRect(420, 40, 81, 21))
        # self.label_mssv.setFont(font)

        # Submit button
        # self.pushButton_submit = QPushButton(self.centralwidget)
        # self.pushButton_submit.setObjectName(u"pushButton_submit")
        # self.pushButton_submit.setGeometry(QRect(840, 20, 211, 61))
        # self.pushButton_submit.setFont(font)

        #--------------------------------------------------#
        # Retrieve singleton reference to system object
        self.system = PySpin.System.GetInstance()
        # Retrieve list of cameras from the system
        self.cam_list = self.system.GetCameras()
        for i, self.cam in enumerate(self.cam_list):
            self.cam.Init()
            self.nodemap = self.cam.GetNodeMap()
            try:  
                # Width = 744
                # Height = 300
                # Offset X = 330
                # Offset Y = 330

                node_jumbo_package = PySpin.CIntegerPtr(self.nodemap.GetNode('GevSCPSPacketSize'))
                node_jumbo_package.SetValue(9000)

                node_width = PySpin.CIntegerPtr(self.nodemap.GetNode('Width'))
                node_width.SetValue(744)

                node_height = PySpin.CIntegerPtr(self.nodemap.GetNode('Height'))
                node_height.SetValue(300)

                node_offsetX = PySpin.CIntegerPtr(self.nodemap.GetNode('OffsetX'))
                node_offsetX.SetValue(380)

                node_offsetY = PySpin.CIntegerPtr(self.nodemap.GetNode('OffsetY'))
                node_offsetY.SetValue(384)

                node_pixel_format = PySpin.CEnumerationPtr(self.nodemap.GetNode('PixelFormat'))
                node_pixel_format_RGB = node_pixel_format.GetEntryByName('RGB8Packed')
                node_pixel_format.SetIntValue(node_pixel_format_RGB.GetValue())

                node_acquisition_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
                node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
                node_acquisition_mode.SetIntValue(node_acquisition_mode_continuous.GetValue())
            except:
                print("Cannot set mode.")   
            self.cam.BeginAcquisition()
            self.CAMERA_IS_ON = True

        #--------------------------------------------------#
        # Set timer for update frame:
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1366, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow): ## Intergrate the widgets into window
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Camera Capture & Object Detection", None))
        self.camera_feed.setText("")
        self.image_feed.setText("")
        self.camera_feed_label.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.image_feed_label.setText(QCoreApplication.translate("MainWindow", u"Image result", None))

        self.classify_button.setText(QCoreApplication.translate("MainWindow", u"Classify", None))
        self.detect_button.setText(QCoreApplication.translate("MainWindow", u"Detect Defect", None))

        self.classify_result_section.setText(QCoreApplication.translate("MainWindow", u"Class:", None))
        self.detect_result_section.setText(QCoreApplication.translate("MainWindow", u"Defects:", None))
        self.classify_result_text.setText(QCoreApplication.translate("MainWindow", u"waiting for result", None))
        self.detect_result_text.setText(QCoreApplication.translate("MainWindow", u"waiting for result", None))

        self.trigger_camera.setText(QCoreApplication.translate("MainWindow", u"Camera On/Off", None))
        self.trigger_light.setText(QCoreApplication.translate("MainWindow", u"Light On/Off", None))
        self.camera_temperature.setText(QCoreApplication.translate("MainWindow", u"Camera temperature: 37℃", None))
        self.jetson_temperature.setText(QCoreApplication.translate("MainWindow", u"CPU temperature: 37℃", None))
        
        self.CAPTURE.setText(QCoreApplication.translate("MainWindow", u"CAPTURE", None))

        # self.Save_file.setText(QCoreApplication.translate("MainWindow", u"Save file", None))
        # self.file_saved.setText(QCoreApplication.translate("MainWindow", u"Open saved file", None))
        # self.label_name.setText(QCoreApplication.translate("MainWindow", u"NAME:", None))
        # self.label_mssv.setText(QCoreApplication.translate("MainWindow", u"MSSV:", None))
        # self.pushButton_submit.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
        
        
    def toggle_camera(self):
        
        return
    
    def toggle_light(self):

        return
    def update_frame(self):
        #Read camera
        display_frame = self.cam.GetNextImage(1000)
        display_frame_data = display_frame.GetNDArray()
        # h = 1200, w = 1600, ch = 3, byte per line = ch*w
        Qt_format = QImage(display_frame_data, 744, 300, QImage.Format_RGB888)
        pixmap_format = QPixmap.fromImage(Qt_format)
        self.camera_feed.setPixmap(pixmap_format.scaled(self.camera_feed.size(), Qt.KeepAspectRatio))

    def detect(self):
        if self.prediction == "C" or self.prediction == "D":
            self.label_2.setText(QCoreApplication.translate("MainWindow", u"Class C and D does not have to detect defects", None))
            return
        _, img_encoded = cv2.imencode('.jpg', self.capture_frame_data)
        response = requests.post('http://192.168.1.121:5000/detect', data=img_encoded.tobytes())
        if response.status_code == 200:
            img_bytes = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes)
            self.image_feed.setPixmap(pixmap.scaled(self.image_feed.size(), Qt.KeepAspectRatio))

    def capture_and_display(self):
        capture_frame = self.cam.GetNextImage(1000)
        self.capture_frame_data = capture_frame.GetNDArray()
        capture_Qt_format = QImage(self.capture_frame_data, 744, 300, QImage.Format_RGB888)
        capture_pixmap_format = QPixmap.fromImage(capture_Qt_format)
        self.image_feed.setPixmap(capture_pixmap_format.scaled(self.image_feed.size(), Qt.KeepAspectRatio))

    def classify(self): # Send and return image from classification task
        _, img_encoded = cv2.imencode('.jpg', self.capture_frame_data)
        response = requests.post('http://192.168.1.121:5000/classify', files={'file': img_encoded.tobytes()})
        if response.status_code == 200:
            self.prediction = response.json().get('prediction', 'Error')
            self.label.setText(f'{self.prediction}')

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

