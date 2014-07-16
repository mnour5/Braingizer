from PyQt4 import QtCore, QtGui
from gui_train import Ui_TrainWindow

from TrainingFileCreator_Class import TrainingFileCreator

#Controls
from DetailsFrameControl_Class import DetailsFrameControl
from ArrowFrameControl_Class import ArrowFrameControl
from SessionDetailsControl_Class import SessionDetailsControl
from TimerControl_Class import TimerControl
from WelcomeFrameControl_Class import WelcomeFrameControl
from FinishedFrameControl_Class import FinishedFrameControl

import AppConfig

class Ui_TrainWindow_Extended(Ui_TrainWindow):
    def InitializeUI(self, TrainWindow, EEG):
        # Controls
        self.DetailsFrameCtrl       = DetailsFrameControl(self)
        self.ArrowFrameCtrl         = ArrowFrameControl(self)
        self.WelcomeFrameCtrl       = WelcomeFrameControl(self)
        self.SessionDetailsCtrl     = SessionDetailsControl(self)
        self.FinishedFrameControl   = FinishedFrameControl(self)
        self.TimerCtrl              = TimerControl(self)
        
        # Used with MessageBoxes and closeEvent
        self.TrainWindow = TrainWindow
        
        # EEG
        self.EEG = EEG
        
        # EVENTS
        self.TrainWindow.closeEvent = self.onClose
        self.centralwidget.resizeEvent = self.onResize
        self.Start_Button.clicked.connect(self.Start_Button_Clicked)
        self.AddComments_Button.clicked.connect(self.AddComments_Button_Clicked)
        self.Clipboard_Button.clicked.connect(self.Clipboard_Button_Clicked)
        QtCore.QObject.connect(self.EEG, QtCore.SIGNAL('DataSaved(PyQt_PyObject)'), self.EEG_DataSaved)
        
        # Flags
        self.TrainingStarted = False
    
    def initializeTraining(self, Profile, Session):
        if(self.EEG.connected):
            # Get needed session details
            self.SessionDetailsCtrl.getSessionDetails(Profile, Session)
            
            # Training file
            self.TrainingFile = TrainingFileCreator()
            
            # The details frame on the top of the window
            self.DetailsFrameCtrl.initializeComponents()
            
            # The timer control wich controls the training sequnce
            self.TimerCtrl.initializeTimer()
            
            # The arrows
            self.ArrowFrameCtrl.initializeArrows()
            self.ArrowFrameCtrl.hideFrame()
            
            # The welcome note
            self.WelcomeFrameCtrl.initializeWelcomeNote()
            self.WelcomeFrameCtrl.showFrame()
            
            # The finished note
            self.FinishedFrameControl.hideFrame()
            
            # Centring the elements in the window
            self.centerPosition()
    
    def startTraining(self):
        self.TrainingStarted = True
        self.TimerCtrl.StartTimer()
    
    def stopTraining(self):
        self.TrainingStarted = False
        self.TimerCtrl.StopTimer()
    
    def centerPosition(self):
        self.DetailsFrameCtrl.resetControlsPosition()
        self.ArrowFrameCtrl.centerPosition()
        self.WelcomeFrameCtrl.centerPosition()
        self.FinishedFrameControl.centerPosition()
    
    def showQuestionMessageBox(self, title, message):
        reply = QtGui.QMessageBox.question(self.TrainWindow, title, message,
                                           QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return False
        else:
            return True
    
    # EVENTS
    def onResize(self, event):
        self.centerPosition()
    
    def onClose(self, event):        
        if(self.TrainingStarted):
            reply = self.showQuestionMessageBox("Warning", "Are you sure you want to exit the training session?")
            
            if(reply):
                self.TrainingStarted = False
                self.TimerCtrl.StopTimer()
                self.TrainWindow.emit( QtCore.SIGNAL('TrainingCanceled()') )
            else:
                event.ignore()
        else:
            self.TrainWindow.emit( QtCore.SIGNAL('TrainingCanceled()') )
    
    def EEG_DataSaved(self, returnval):
        filename = returnval["FileName"]
        self.FilePath = returnval["FilePath"]
        # Stop training flag
        self.stopTraining()
        self.FinishedFrameControl.showFrame(filename)
        
        # Debug
        if(AppConfig.DebugTrainingSession): print "Finished and file saved to: ", filename
    
    def TimerCtrl_TrainingFinishedFlag(self):
        # Start saving thread
        filename = self.EEG.saveToFile(self.SessionDetails)

    def TimerCtrl_NewTrialFlag(self):
        self.SessionDetailsCtrl.addDoneTrial()
        
        self.DetailsFrameCtrl.update()
        
        self.ArrowFrameCtrl.hideFrame()
        
        if(self.SessionDetails["DoneTrials_Total"] != self.SessionDetails["nTrials_Total"]):
            self.RndClass, ClassNumber = self.SessionDetailsCtrl.getRandomClass()
            self.EEG.setClassType(ClassNumber)
            
            # Debug
            if(AppConfig.DebugTrainingSession): print "New Trial:", self.RndClass
    
    def TimerCtrl_RecordingFlag(self):
        self.ArrowFrameCtrl.showArrow(self.RndClass)
        self.EEG.setTrigger()
        
        # Debug
        if(AppConfig.DebugTrainingSession): print "\tRecording..."

    def TimerCtrl_SteadyFlag(self):
        self.ArrowFrameCtrl.showFrame()
        self.ArrowFrameCtrl.resetArrows()
        
        # Debug
        if(AppConfig.DebugTrainingSession): print "\tSteady..."

    def TimerCtrl_BlankFlag(self):
        self.ArrowFrameCtrl.hideFrame()
        self.RndClass, ClassNumber = self.SessionDetailsCtrl.getRandomClass()
        self.EEG.setClassType(ClassNumber)
        
        # Debug
        if(AppConfig.DebugTrainingSession): print "New Trial:", self.RndClass
    
    def Start_Button_Clicked(self):
        self.WelcomeFrameCtrl.hideFrame()
        self.startTraining()
    
    def Clipboard_Button_Clicked(self):
        cb = QtGui.QApplication.clipboard()
        cb.setText(self.FilePath)
    
    def AddComments_Button_Clicked(self):
        self.TrainingFile.AddComments(self.FilePath, self.Comments_LineEdit.text())
        self.onClose(self)