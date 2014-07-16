import os
from TrainingFileClass import TrainingFileClass

from PyQt4 import QtCore, QtGui
from gui_main import Ui_MainWindow
from gui_sensors_extended import Ui_SensorsWindow_Extended
from gui_detect_extended import Ui_DetectWindow_Extended

from ClassifiersClass import Classifiers
from EEGConnectorClass import EEGConnector

from TrainingFileControl_Class import TrainingFileControl
from DetectionSessionControl_Class import DetectionSessionControl

from XmlParser_Class import XmlParser

import AppConfig

class Ui_MainWindow_Extended(Ui_MainWindow):
    def InitializeUI(self, MainWindow):
        #Python-Emotiv Wrraped Class
        self.EEG = EEGConnector()
        
        #Used with MessageBoxes
        self.MainWindow = MainWindow
        
        #Connected flag
        self.connected = False
        
        #Training-Files and Scripts ComboBoxes
        self.addComboBoxesData()
        
        #Battery Update Timer
        self.BatteryTimer = QtCore.QTimer()
        self.BatteryTimer.timeout.connect(self.BatteryTimer_Timeout)
        
        # UI-Controls
        self.TrainingFileCtrl       = TrainingFileControl(self)
        self.DetectionSessionCtrl   = DetectionSessionControl(self)
        
        #UIs (Sensors and Detect)
        self.InitializeSensorsUI()
        self.InitializeDetectUI()
        
        #EVENTS
        self.connectButton.clicked.connect(self.connectButton_Clicked)
        self.disconnectButton.clicked.connect(self.disconnectButton_Clicked)
        self.startButton.clicked.connect(self.startButton_Clicked)
        QtCore.QObject.connect(self.EEG, QtCore.SIGNAL("error()"), self.EEG_Error)
        
        #DELETE THIS
        self.DetectionOptionsGroup.setVisible(False)
        
        if(AppConfig.Autorun):
            self.autorun()
    
    def InitializeSensorsUI(self):
        self.SensorsWindow = QtGui.QMainWindow()
        self.ui_sensors = Ui_SensorsWindow_Extended()
        self.ui_sensors.setupUi(self.SensorsWindow)
        self.ui_sensors.InitializeUI(self.EEG)

    def InitializeDetectUI(self):
        self.DetectWindow = QtGui.QMainWindow()
        self.ui_detect = Ui_DetectWindow_Extended()
        self.ui_detect.setupUi(self.DetectWindow)
        self.ui_detect.InitializeUI(self.MainWindow, self.SensorsWindow, self.DetectWindow, self.EEG)
    
    def autorun(self):
        status = ""
        while(status != "Connected"):
            status = self.EEG.connect()
            if(status == "Connected"):
                self.enableControls(True)        
                self.SensorsWindow.show()
                self.BatteryTimer.start(1000)
        
        if(self.EEG.connected):
            self.DetectWindow.show()
            
            SessionDetails = self.DetectionSessionCtrl.getAutorunSessionDetails()
            self.ui_detect.initializeDetection(SessionDetails)
    
    def addComboBoxesData(self):
        '''
        #TrainingData files
        TrainingFiles = os.listdir('TrainingData')
        self.TrainingFile_ComboBox.clear()
        self.TrainingFile_ComboBox.addItems(TrainingFiles)
        '''
        #Classifiers scripts
        C = Classifiers()
        self.Classifiers_ComboBox.addItems(C.getClassifiers())
    
    def showMessageBox(self, title, message):
        reply = QtGui.QMessageBox.about(self.MainWindow, title, message)
    
    def enableControls(self, opt):
        self.TimingOptionsGroup.setEnabled(opt)
        self.DetectionOptionsGroup.setEnabled(opt)
        self.startButton.setEnabled(opt)
        self.disconnectButton.setEnabled(opt)
        self.connectButton.setEnabled(not opt)
        
        self.TrainingFileCtrl.setEnabled(opt)

    #EVENTS
    def BatteryTimer_Timeout(self):
        if(self.EEG.connected):
            self.batteryBar.setValue(self.EEG.eeg_battery)
        else:
            self.batteryBar.setValue(0)

    def EEG_Error(self):
        self.EEG.disconnect()
        
        self.enableControls(False)
        
        self.SensorsWindow.hide()
        
        self.ui_detect.stopDetection()
        self.DetectWindow.hide()
        self.MainWindow.show()
        
        self.statusLabel.setText("ERROR: Headset is disconnected")

    def connectButton_Clicked(self):
        status = self.EEG.connect()
        if(status == "Connected"):
            self.enableControls(True)        
            self.SensorsWindow.show()
            self.BatteryTimer.start(1000)
        
        self.statusLabel.setText(status)

    def disconnectButton_Clicked(self):
        self.EEG.disconnect()
        
        self.enableControls(False)
        
        self.SensorsWindow.hide()
        
        self.ui_detect.stopDetection()
        self.DetectWindow.hide()

    def startButton_Clicked(self):
        if(self.EEG.connected):
            self.DetectWindow.show()
            
            if(AppConfig.Autorun):
                self.MainWindow.hide()
                self.SensorsWindow.hide()
            
            SessionDetails = self.DetectionSessionCtrl.getSessionDetails()
            
            """
            Details = {}
            filepath = AppConfig.TrainingFolder + "/" + TrainingFile
            TrainingFileClass.getClasses(filepath)
            
            print filepath
            
            Details["SubjectName"]          = TrainingFileClass.getName(filepath)
            Details["NumberOfTrials"]       = int(self.NumberOfTrials_LineEdit.text())
            Details["NumberOfTrials"]       = int(self.NumberOfTrials_LineEdit.text())
            '''
            Details["PreRecordingTime"]     = int(self.PreRecordingTime_LineEdit.text())
            Details["RecordingTime"]        = int(self.RecordingTime_LineEdit.text())
            Details["PostRecordingTime"]    = int(self.PostRecordingTime_LineEdit.text())
            '''
            Details["BlankTime"]            = int(self.BlankTime_LineEdit.text())
            Details["SteadyTime"]           = int(self.SteadyTime_LineEdit.text())
            Details["RecordingTime"]        = int(self.RecordingTime_LineEdit.text())
            Details["PostRecordingTime"]    = int(self.PostRecordingTime_LineEdit.text())
            Details["Classes"]              = TrainingFileClass.getClasses(filepath)
            """
            
            self.ui_detect.initializeDetection(SessionDetails)