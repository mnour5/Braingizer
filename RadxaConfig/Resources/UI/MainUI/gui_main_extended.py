import os
from TrainingFileClass import TrainingFileClass

from PyQt4 import QtCore, QtGui
from gui_main import Ui_MainWindow

from ClassifiersClass import Classifiers

from TrainingFileControl_Class import TrainingFileControl

from XmlParser_Class import XmlParser

from RadxaInterface_Class import RadxaInterface

import AppConfig

class Ui_MainWindow_Extended(Ui_MainWindow):
    def InitializeUI(self, MainWindow): 
        #Used with MessageBoxes
        self.MainWindow = MainWindow
        
        #Scripts ComboBox
        self.addComboBoxesData()
        
        # UI-Controls
        self.TrainingFileCtrl = TrainingFileControl(self)
        
        self.Radxa = RadxaInterface()
        
        #EVENTS
        self.shutdownButton.clicked.connect(self.shutdownButton_Clicked)
        self.rebootButton.clicked.connect(self.rebootButton_Clicked)
        self.configButton.clicked.connect(self.configButton_Clicked)
    
    def addComboBoxesData(self):
        #Classifiers scripts
        C = Classifiers()
        self.Classifiers_ComboBox.addItems(C.getClassifiers())
        self.Classifiers_ComboBox.setCurrentIndex(C.getClassifiers().index(AppConfig.Default_Classifier))
    
    def getTrainingFile(self):
        Idx             = self.TrainingFile_ComboBox.currentIndex()
        TrainingFile    = self.TrainingFileCtrl.TrainingFiles['Path'][Idx]
        
        return TrainingFile
    
    def showMessageBox(self, title, message):
        reply = QtGui.QMessageBox.about(self.MainWindow, title, message)

    #EVENTS
    def shutdownButton_Clicked(self):
        self.Radxa.connect()
        
        if(self.Radxa.Connected):
            self.Radxa.shutdown()
    
    def rebootButton_Clicked(self):
        self.Radxa.connect()
        
        if(self.Radxa.Connected):
            self.Radxa.reboot()
    
    def configButton_Clicked(self):
        self.Radxa.connect()
        
        if(self.Radxa.Connected):
            Classifier      = str( self.Classifiers_ComboBox.currentText() )
            TrainingFile    = str( self.getTrainingFile() )
            RecordingTime   = str( self.RecordingTime_LineEdit.text() )
            
            self.Radxa.configRadxa(Classifier, TrainingFile, RecordingTime)
            self.Radxa.disconnect()