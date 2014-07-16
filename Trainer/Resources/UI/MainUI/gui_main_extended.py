import os
from PyQt4 import QtCore, QtGui
from gui_main import Ui_MainWindow
from gui_sensors_extended import Ui_SensorsWindow_Extended
from gui_train_extended import Ui_TrainWindow_Extended
from EEGConnector_Trianer_Class import EEGConnector_Trianer
from ProfileControl_Class import ProfileControl
from SessionControl_Class import SessionControl
import AppConfig

class Ui_MainWindow_Extended(Ui_MainWindow):
    def InitializeUI(self, MainWindow, app):
        self.ProfileCtrl = ProfileControl(self)
        self.SessionCtrl = SessionControl(self)
        
        #Used with MessageBoxes
        self.MainWindow = MainWindow
        
        #Used in exit
        self.app = app
        
        #Python-Emotiv Wrraped Class
        self.EEG = EEGConnector_Trianer()
        
        #UIs (Sensors and Train)
        
        self.InitializeSensorsUI()
        self.InitializeTrainUI()
        
        #EVENTS
        self.MainWindow.closeEvent = self.onClose
        self.Connect_Button.clicked.connect(self.Connect_Button_Clicked)
        self.Disconnect_Button.clicked.connect(self.Disconnect_Button_Clicked)
        self.Start_Button.clicked.connect(self.Start_Button_Clicked)
        QtCore.QObject.connect(self.EEG, QtCore.SIGNAL("error()"), self.EEG_Error)
        
        #Battery Update Timer
        self.BatteryTimer = QtCore.QTimer()
        self.BatteryTimer.timeout.connect(self.BatteryTimer_Timeout)
    
    def InitializeSensorsUI(self):
        self.SensorsWindow = QtGui.QMainWindow()
        self.ui_sensors = Ui_SensorsWindow_Extended()
        self.ui_sensors.setupUi(self.SensorsWindow)
        self.ui_sensors.InitializeUI(self.EEG)
    
    def InitializeTrainUI(self):
        self.TrainWindow = QtGui.QMainWindow()
        self.ui_train = Ui_TrainWindow_Extended()
        self.ui_train.setupUi(self.TrainWindow)
        self.ui_train.InitializeUI(self.TrainWindow, self.EEG)
        
        QtCore.QObject.connect(self.TrainWindow, QtCore.SIGNAL("TrainingCanceled()"), self.TrainWindow_TrainingCanceled)
    
    def showMessageBox(self, title, message):
        reply = QtGui.QMessageBox.about(self.MainWindow, title, message)
    
    def showQuestionMessageBox(self, title, message):
        reply = QtGui.QMessageBox.question(self.MainWindow, title, message,
                                           QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return False
        else:
            return True
    
    def enableControls(self, opt):
        self.ProfileCtrl.setEnabled(opt)
        self.SessionCtrl.setEnabled(opt)
        self.Start_Button.setEnabled(opt)
        self.Disconnect_Button.setEnabled(opt)
        self.Connect_Button.setEnabled(not opt)
    
    #EVENTS
    def BatteryTimer_Timeout(self):
        if(self.EEG.connected):
            self.Battery_ProgBar.setValue(self.EEG.eeg_battery)
        else:
            self.Battery_ProgBar.setValue(0)
    
    def EEG_Error(self):
        self.Disconnect_Button_Clicked()
        
        self.Status_Label.setText("Headset is disconnected")
        self.showMessageBox("Error", "The headset is disconnected.")
        
        #DELETE ALL
        self.MainWindow.setWindowState(QtCore.Qt.WindowActive)
    
    def TrainWindow_TrainingCanceled(self):
        self.Disconnect_Button_Clicked()        
        self.Status_Label.setText("Training is canceled")
        
        #DELETE ALL
        self.MainWindow.setWindowState(QtCore.Qt.WindowActive)
        
    def Connect_Button_Clicked(self):
        status = self.EEG.connect()
        
        if(status == "Connected"):
            self.enableControls(True)
            self.BatteryTimer.start(1000)
            self.SensorsWindow.showNormal()
            self.SensorsWindow.setFocus()
        
        self.Status_Label.setText(status)
    
    def Disconnect_Button_Clicked(self):
        # Disonnect the EEG
        self.EEG.disconnect()
        
        # Stop training
        self.ui_train.stopTraining()
        
        # Disable the session and profile GroupBoxes
        self.enableControls(False)
        
        # Hide Train and Sensors Windows
        self.SensorsWindow.hide()
        self.TrainWindow.hide()
    
    def Start_Button_Clicked(self):
        if(self.ProfileCtrl.checkInputs()):
            if(self.SessionCtrl.checkInputs()):
                if(self.EEG.connected):
                    Profile = self.ProfileCtrl.getProfile()
                    Session = self.SessionCtrl.getSession()
                    
                    self.TrainWindow.show()
                    self.ui_train.initializeTraining(Profile, Session)
                    
                    # Minimize MainWindow and SensorsWindow
                    self.MainWindow.setWindowState(QtCore.Qt.WindowMinimized)
                    self.SensorsWindow.setWindowState(QtCore.Qt.WindowMinimized)
                    #self.MainWindow.showMinimized()
                    #self.SensorsWindow.showMinimized()
    
    def onClose(self, event):
        # Exit the app on MainWindow Close
        # But check first if there is no training session is running
        
        if(self.ui_train.TrainingStarted):
            reply = self.ui_train.showQuestionMessageBox("Warning", "Are you sure you want to exit the training session?")
            
            if(reply):
                self.app.exit()
            else:
                event.ignore()
        else:
            self.app.exit()