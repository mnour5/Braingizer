from random import randint
import time
from PyQt4 import QtCore, QtGui
from gui_detect import Ui_DetectWindow

from DetectorClass import Detector
from MotorDriverClass import MotorDriver
import AppConfig

#Controls
from WelcomeFrameControl_Class import WelcomeFrameControl
from ArrowFrameControl_Class import ArrowFrameControl

class Ui_DetectWindow_Extended(Ui_DetectWindow):
    def InitializeUI(self, EEG):
        # Controls
        self.ArrowFrameControl      = ArrowFrameControl(self)
        
        self.EEG = EEG
        self.Detector = None
        self.finishedDetect = True
        self.detectedDirection = ""
        
        self.detectBufferSize = 3
        self.lastDetected = ""
        self.lastDetectedItr = 0
        
        #Creating Motor
        if(AppConfig.EnableMotors):
            self.motor = MotorDriver()
            self.motor.connect()
        
        self.resetControlsPosition()
        
        #Trial Data Timer
        self.TrialDataTimer = QtCore.QTimer()
        self.TrialDataTimer.timeout.connect(self.TrialDataTimer_Timeout)
        
        #EVENTS
        
        self.centralwidget.resizeEvent = self.onResize
        self.toggleIcon.mouseReleaseEvent = self.toggleIcon_Clicked
        self.untoggleIcon.mouseReleaseEvent = self.untoggleIcon_Clicked

    def hideEvent(self, event):
        print "test"

    def initializeDetection(self, SessionDetails):
        if(self.EEG.connected):
            self.SessionDetails = SessionDetails
            
            # Initalize Arrows
            self.ArrowFrameControl.initializeArrows()
            self.ArrowFrameControl.showFrame()
            
            self.AvgDetectionTime = 0.00
            
            self.Name_Label.setText(SessionDetails["ProfileName"])
            self.ClassifierName_Label.setText( SessionDetails["Classifiers"] )
            
            self.Detector = Detector(SessionDetails["TrainingFile"], SessionDetails["Classifiers"])
            self.Detector.startDetection()
            
            QtCore.QObject.connect(self.Detector.DetectThread, QtCore.SIGNAL('detected(PyQt_PyObject)'), self.DetectThread_Detected)
            
            self.TrialDataTimer.start(100)

    def stopDetection(self):
        if(self.Detector):
            if(self.Detector.DetectionStarted):
                self.Detector.stopDetection()
                self.TrialDataTimer.stop()
    
    def resetControlsPosition(self):
        self.ArrowFrameControl.centerPosition()
        x = (self.centralwidget.width() - self.Arrows_Frame_Normal.width()) / 2
        y = (self.centralwidget.height() - self.Arrows_Frame_Normal.height()) / 2
        
        y += self.Arrows_Frame_Normal.height() + 30
        
        self.NoteFrame_3.move(x, y)
        
        self.detalisParent_Frame.setGeometry(QtCore.QRect(10, 10, self.centralwidget.width()-20, 60))
        self.details_Line.setGeometry(QtCore.QRect(0, 50, self.detalisParent_Frame.width(), 16))
        self.detalisChild_Frame.setGeometry(QtCore.QRect(0, 0, self.detalisParent_Frame.width()-30, 50))
        self.toggleIcon.setGeometry(QtCore.QRect(self.detalisChild_Frame.width(), 0, 24, 24))
        self.untoggleIcon.setGeometry(QtCore.QRect(self.detalisChild_Frame.width()+10, 10, 24, 24))
    
    def setNote3_Label(self, direction):
        self.Note3_Label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">" + direction + " detected.</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Wrong? Press escape, spacebar or hit this button:</span></p></body></html>")
    
    def setAvgTime_Label(self):
        self.AvgTime_Label.setText( str("%.2f" % self.AvgDetectionTime) + " sec" )
    
    def getSessionDetails(self):
        SessionDetails = {}
        
        SessionDetails["TrainingSource"]    = self.SessionDetails["TrainingFile"]
        SessionDetails["Name"]              = self.SessionDetails["ProfileName"]
        SessionDetails["NumberOfTrials"]    = self.NumberOfTrials
        SessionDetails["PreRecordingTime"]  = self.BlankTime + self.SteadyTime
        SessionDetails["RecordingTime"]     = self.RecordingTime
        SessionDetails["PostRecordingTime"] = self.PostRecordingTime
        SessionDetails["AvgDetectTime"]     = self.AvgDetectionTime
        SessionDetails["Classifier"]        = self.SessionDetails["Classifiers"]
        SessionDetails["Classes"]           = self.SessionDetails["ClassesNames"]
        
        return SessionDetails
    
    def TrialDataTimer_Timeout(self):
        self.RecordingTime = 4
        if(len(self.EEG.eeg_counter) >= (self.EEG.fps * self.RecordingTime)):
            self.isDetecting = True
            self.Start_DetectionTime = time.time()
            #TrialData = self.EEG.getLastTrial(self.RecordingTime)
            TrialData = self.EEG.getLastData(self.RecordingTime)
            self.Detector.detect(TrialData)
            self.TrialDataTimer.stop()
    
    def DetectThread_Detected(self, DetectOut):
        self.End_DetectionTime = time.time()
        New_DetectionTime = self.End_DetectionTime - self.Start_DetectionTime
        #self.AvgDetectionTime = ((self.AvgDetectionTime * self.NumberOfDoneTrials) + New_DetectionTime) / (self.NumberOfDoneTrials + 1)
        
        print DetectOut
        
        if(DetectOut != self.detectedDirection):
            if(DetectOut != self.lastDetected):
                self.lastDetectedItr = 0
                self.lastDetected = DetectOut
            else:
                self.lastDetectedItr = self.lastDetectedItr + 1
                
                if(self.lastDetectedItr == self.detectBufferSize):
                    print "GO ", DetectOut
                    self.detectedDirection = DetectOut
                    
                    self.ArrowFrameControl.resetArrows()
                    self.ArrowFrameControl.showArrow(self.detectedDirection, "GREEN")
                
                    self.setNote3_Label(self.detectedDirection.title())
                    
                    if(AppConfig.EnableMotors):
                        if(self.detectedDirection == "RIGHT"):
                            self.motor.goRight()
                            #time.sleep(AppConfig.MotorStopDelay)
                            #self.motor.stop()
                        
                        elif(self.detectedDirection == "LEFT"):
                            self.motor.goLeft()
                            #time.sleep(AppConfig.MotorStopDelay)
                            #self.motor.stop()
                        
                        elif(self.detectedDirection == "FORWARD"):
                            self.motor.goForward()
                        
                        else:
                            self.motor.stop()
        
        if(AppConfig.PrintSessionDetails):
            print self.detectedDirection + " Detected in " + str("%.2f" % self.AvgDetectionTime) + " sec"
        
        self.finishedDetect = True
        
        self.TrialDataTimer.start(100)

    def untoggleIcon_Clicked(self, event):
        self.detalisParent_Frame.setVisible(True)

    def toggleIcon_Clicked(self, event):
        self.detalisParent_Frame.setVisible(False)

    def onResize(self, event):
        self.resetControlsPosition()
