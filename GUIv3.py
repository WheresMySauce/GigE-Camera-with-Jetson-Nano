# -*- coding: utf-8 -*-
# System
import sys

# GUI
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Image processing
import cv2
import requests

# Camera processing
import PySpin

class Ui_MainWindow(object):
    def setupUi(self, MainWindow): #setupUi i.e fonts, location,....

        # Window initialize
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        MainWindow.resize(1366, 768)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        # Set up fonts
        font = QFont()
        font.setFamily(u"Times New Roman")
        font.setPointSize(16)

        bold_font = QFont()
        bold_font.setFamily(u"Times New Roman")
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
        
        # Camera feed
        self.CAMERA = QLabel(self.centralwidget)
        self.CAMERA.setObjectName(u"Camera Feed")
        self.CAMERA.setGeometry(QRect(20, 160, 500, 248))
        self.CAMERA.setFont(font)
        self.CAMERA.setFrameShape(QFrame.Box)
        # self.CAMERA.setPixmap(QPixmap(u"data/5.PNG"))

        # Result image
        self.image = QLabel(self.centralwidget)
        self.image.setObjectName(u"Result image")
        self.image.setGeometry(QRect(590, 160, 500, 248))
        self.image.setFont(font)
        self.image.setFrameShape(QFrame.Box)
        # self.image.setPixmap(QPixmap(u"data/4.PNG"))

        # Camera feed label
        self.label_camera = QLabel(self.centralwidget)
        self.label_camera.setObjectName(u"label_camera")
        self.label_camera.setGeometry(QRect(190, 430, 121, 51))
        self.label_camera.setFont(bold_font)
        self.label_camera.setTextFormat(Qt.AutoText)
        self.label_camera.setAlignment(Qt.AlignCenter)

        # Result image label
        self.label_image_result = QLabel(self.centralwidget)
        self.label_image_result.setObjectName(u"label_image_result")
        self.label_image_result.setGeometry(QRect(750, 430, 181, 51))
        self.label_image_result.setFont(bold_font)
        self.label_image_result.setLayoutDirection(Qt.LeftToRight)
        self.label_image_result.setAlignment(Qt.AlignCenter)

        # Send image to classify button
        self.Classification = QPushButton(self.centralwidget)
        self.Classification.setObjectName(u"Classification")
        self.Classification.setGeometry(QRect(1120, 350, 241, 61))
        self.Classification.setFont(font)
        self.Classification.clicked.connect(self.classify_result)

        # Send image to detect defects button
        self.Defect_detecton = QPushButton(self.centralwidget)
        self.Defect_detecton.setObjectName(u"Defect_detecton")
        self.Defect_detecton.setGeometry(QRect(1120, 420, 241, 61))
        self.Defect_detecton.setFont(font)
        self.Defect_detecton.clicked.connect(self.detect_result)

        # Save file button
        self.Save_file = QPushButton(self.centralwidget)
        self.Save_file.setObjectName(u"Save_file")
        self.Save_file.setGeometry(QRect(1120, 490, 241, 61))
        self.Save_file.setFont(font)

        # Show saved file button
        self.file_saved = QPushButton(self.centralwidget)
        self.file_saved.setObjectName(u"file_saved")
        self.file_saved.setGeometry(QRect(1120, 560, 241, 61))
        self.file_saved.setFont(font)

        # Input for name and ID
        self.name = QLineEdit(self.centralwidget)
        self.name.setObjectName(u"name")
        self.name.setGeometry(QRect(100, 30, 271, 41))
        self.name.setFont(font)
        self.mssv = QLineEdit(self.centralwidget)
        self.mssv.setObjectName(u"mssv")
        self.mssv.setGeometry(QRect(510, 30, 271, 41))
        self.mssv.setFont(font)
        self.label_name = QLabel(self.centralwidget)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setGeometry(QRect(10, 40, 81, 21))
        self.label_name.setFont(font)
        self.label_mssv = QLabel(self.centralwidget)
        self.label_mssv.setObjectName(u"label_mssv")
        self.label_mssv.setGeometry(QRect(420, 40, 81, 21))
        self.label_mssv.setFont(font)

        # Submit button
        self.pushButton_submit = QPushButton(self.centralwidget)
        self.pushButton_submit.setObjectName(u"pushButton_submit")
        self.pushButton_submit.setGeometry(QRect(840, 20, 211, 61))

        self.pushButton_submit.setFont(font)

        # Test result for label
        self.label_class = QLabel(self.centralwidget)
        self.label_class.setObjectName(u"label_class")
        self.label_class.setGeometry(QRect(20, 530, 60, 30))
        self.label_class.setFont(font)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(100, 530, 491, 30))
        self.label.setFont(font)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(100, 580, 60, 30))
        self.label_2.setFont(font)
        self.label_error_2 = QLabel(self.centralwidget)
        self.label_error_2.setObjectName(u"label_error_2")
        self.label_error_2.setGeometry(QRect(20, 640, 71, 30))
        self.label_error_2.setFont(font)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(100, 640, 500, 30))
        self.label_3.setFont(font)
        self.label_error = QLabel(self.centralwidget)
        self.label_error.setObjectName(u"label_error")
        self.label_error.setGeometry(QRect(20, 580, 60, 30))
        self.label_error.setFont(font)

        # The error button
        # self.ERROR1 = QPushButton(self.centralwidget)
        # self.ERROR1.setObjectName(u"ERROR1")
        # self.ERROR1.setGeometry(QRect(1160, 60, 160, 40))
        # self.ERROR1.setFont(font)
        # self.ERROR2 = QPushButton(self.centralwidget)
        # self.ERROR2.setObjectName(u"ERROR2")
        # self.ERROR2.setGeometry(QRect(1160, 110, 160, 40))
        # self.ERROR2.setFont(font)
        # self.ERROR3 = QPushButton(self.centralwidget)
        # self.ERROR3.setObjectName(u"ERROR3")
        # self.ERROR3.setGeometry(QRect(1160, 160, 160, 40))
        # self.ERROR3.setFont(font)
        # self.ERROR4 = QPushButton(self.centralwidget)
        # self.ERROR4.setObjectName(u"ERROR4")
        # self.ERROR4.setGeometry(QRect(1160, 210, 160, 40))
        # self.ERROR4.setFont(font)

        # The capture button
        # self.CAPTURE = QPushButton(self.centralwidget)
        # self.CAPTURE.setObjectName(u"CAPTURE")
        # self.CAPTURE.setGeometry(QRect(1120, 280, 241, 61))
        # self.CAPTURE.setFont(font)

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
        self.CAMERA.setText("")
        self.image.setText("")
        self.label_camera.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.label_image_result.setText(QCoreApplication.translate("MainWindow", u"Image result", None))

        self.Classification.setText(QCoreApplication.translate("MainWindow", u"Classify", None))
        self.Defect_detecton.setText(QCoreApplication.translate("MainWindow", u"Detect Defect", None))
        self.Save_file.setText(QCoreApplication.translate("MainWindow", u"Save file", None))
        self.file_saved.setText(QCoreApplication.translate("MainWindow", u"Open saved file", None))
        self.label_name.setText(QCoreApplication.translate("MainWindow", u"NAME:", None))
        self.label_mssv.setText(QCoreApplication.translate("MainWindow", u"MSSV:", None))
        self.pushButton_submit.setText(QCoreApplication.translate("MainWindow", u"Submit", None))

        
        self.label_class.setText(QCoreApplication.translate("MainWindow", u"Class:", None))
        self.label_error.setText(QCoreApplication.translate("MainWindow", u"Defects:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"test", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"test", None))
        # self.ERROR1.setText(QCoreApplication.translate("MainWindow", u"ERROR1", None))
        # self.ERROR2.setText(QCoreApplication.translate("MainWindow", u"ERROR2", None))
        # self.ERROR3.setText(QCoreApplication.translate("MainWindow", u"ERROR3", None))
        # self.ERROR4.setText(QCoreApplication.translate("MainWindow", u"ERROR4", None))
        # self.CAPTURE.setText(QCoreApplication.translate("MainWindow", u"CAPTURE", None))
    
    def update_frame(self):
        # ret, frame = self.cap.read()
        #Read camera
        display_frame = self.cam.GetNextImage(1000)
        display_frame_data = display_frame.GetNDArray()

        # color_image = cv2.cvtColor(display_frame_data, cv2.COLOR_BGR2RGB)
        # h = 1200, w = 1600, ch = 3, byte per line = ch*w
        Qt_format = QImage(display_frame_data, 1600, 1200, QImage.Format_RGB888)
        pixmap_format = QPixmap.fromImage(Qt_format)
        self.CAMERA.setPixmap(pixmap_format.scaled(self.CAMERA.size(), Qt.IgnoreAspectRatio))

    def detect_result(self):
        detect_frame = self.cam.GetNextImage(1000)
        detect_frame_data = detect_frame.GetNDArray()
        # detect_frame_data_color = cv2.cvtColor(detect_frame_data, cv2.COLOR_BGR2RGB)

        _, img_encoded = cv2.imencode('.jpg', detect_frame_data)
        response = requests.post('http://192.168.1.121:5000/detect', data=img_encoded.tobytes())
        if response.status_code == 200:
            img_bytes = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes)
            self.image.setPixmap(pixmap.scaled(self.image.size(), Qt.IgnoreAspectRatio))

    def classify_result(self):
        classify_frame = self.cam.GetNextImage(1000)
        classify_frame_data = classify_frame.GetNDArray()
        # color_image = cv2.cvtColor(frame_data, cv2.COLOR_BGR2RGB)

        _, img_encoded = cv2.imencode('.jpg', classify_frame_data)
        response = requests.post('http://192.168.1.121:5000/classify', files={'file': img_encoded.tobytes()})
        if response.status_code == 200:
            prediction = response.json().get('prediction', 'Error')
            self.label.setText(f'{prediction}')

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

