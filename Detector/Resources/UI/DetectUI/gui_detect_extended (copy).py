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
        self.WelcomeFrameCtrl       = WelcomeFrameControl(self)
        self.ArrowFrameControl      = ArrowFrameControl(self)
        
        #DELETE
        self.Recording_ProgBar.setVisible(False)
        self.Note1_Label.setVisible(False)
        self.Note2_Label.setVisible(False)
        self.WrongButton.setVisible(False)
        
        self.EEG = EEG
        self.Detector = None
        self.finishedDetect = True
        
        #Creating Motor
        if(AppConfig.EnableMotors):
            self.motor = MotorDriver()
            self.motor.connect()
        
        #Notes Frames
        self.NoteFrame_1.setVisible(False)
        self.NoteFrame_2.setVisible(False)
        self.NoteFrame_3.setVisible(False)
        self.NoteFinished.setVisible(False)
        #self.Arrows_Frame.setVisible(True)
        
        self.resetControlsPosition()
        
        #Training Timer
        self.TrainingTimer = QtCore.QTimer()
        self.TrainingTimer.timeout.connect(self.TrainingTimer_Timeout)
        
        #Trial Data Timer
        self.TrialDataTimer = QtCore.QTimer()
        self.TrialDataTimer.timeout.connect(self.TrialDataTimer_Timeout)
        
        #Recording Progress-Bar Timer
        self.RecordingProgBarTimer = QtCore.QTimer()
        self.RecordingProgBarTimer.timeout.connect(self.RecordingProgBarTimer_Timeout)
        
        #EVENTS
        
        self.centralwidget.resizeEvent = self.onResize
        self.centralwidget.keyPressEvent = self.onkeyPress
        self.toggleIcon.mouseReleaseEvent = self.toggleIcon_Clicked
        self.untoggleIcon.mouseReleaseEvent = self.untoggleIcon_Clicked
        QtCore.QObject.connect(self.Start_Button, QtCore.SIGNAL("clicked()"), self.Start_Button_Clicked)
        QtCore.QObject.connect(self.WrongButton, QtCore.SIGNAL("clicked()"), self.WrongButton_Clicked)
        
        QtCore.QObject.connect(self.TrainingTimer, QtCore.SIGNAL("DetectFlag()"), self.TrainingTimer_DetectFlag)
        QtCore.QObject.connect(self.TrainingTimer, QtCore.SIGNAL("RecordingFlag()"), self.TrainingTimer_RecordingFlag)
        QtCore.QObject.connect(self.TrainingTimer, QtCore.SIGNAL("SteadyFlag()"), self.TrainingTimer_SteadyFlag)
        QtCore.QObject.connect(self.TrainingTimer, QtCore.SIGNAL("BlankFlag()"), self.TrainingTimer_BlankFlag)
        QtCore.QObject.connect(self.TrainingTimer, QtCore.SIGNAL("NewTrialFlag()"), self.TrainingTimer_NewTrialFlag)
        
        QtCore.QObject.connect(self.EEG.SaveThread, QtCore.SIGNAL('dataSaved(PyQt_PyObject)'), self.SaveThread_DataSaved)

    def hideEvent(self, event):
        print "test"

    def initializeDetection(self, SessionDetails):
        if(self.EEG.connected):
            self.SessionDetails = SessionDetails
            
            # Initalize Arrows
            self.ArrowFrameControl.initializeArrows()
            self.ArrowFrameControl.hideFrame()
            
            '''
            self.TrainingFile       = TrainingFile
            self.ClassifierScript   = ClassifierScript
            '''
            
            self.Time = 0
            self.flag = ""
            
            self.PostFinishTime = 3 #Wait time after finish
            
            self.NumberOfDoneTrials = 0
            self.NumberOfTrueTrials = 0
            self.AvgDetectionTime = 0.00
            
            self.NumberOfTrials     = SessionDetails["nTrials_Total"]     
            
            self.BlankTime          = SessionDetails["BlankTime"]
            self.SteadyTime         = SessionDetails["SteadyTime"]
            self.RecordingTime      = SessionDetails["RecordingTime"]
            self.PostRecordingTime  = SessionDetails["PostRecordingTime"]
            
            self.Name_Label.setText(SessionDetails["ProfileName"])
            self.ClassifierName_Label.setText( SessionDetails["Classifiers"] )
            self.updateDetails()
            
            self.Detector = Detector(SessionDetails["TrainingFile"], SessionDetails["Classifiers"])
            QtCore.QObject.connect(self.Detector.DetectThread, QtCore.SIGNAL('detected(PyQt_PyObject)'), self.DetectThread_Detected)
            
            self.NoteFrame_1.setVisible(False)
            self.NoteFrame_2.setVisible(False)
            self.NoteFrame_3.setVisible(False)
            self.NoteFinished.setVisible(False)
            
            # WelcomeFrame
            self.WelcomeFrameCtrl.initializeWelcomeNote()
            self.WelcomeFrameCtrl.showFrame()

    def stopDetection(self):
        if(self.Detector):
            if(self.Detector.DetectionStarted):
                self.Detector.stopDetection()
                self.TrainingTimer.stop()
                self.TrialDataTimer.stop()
    
    def triggerWrongTrial(self):
        if(self.trueDirection == "RIGHT"):
            self.trueDirection = "LEFT"
        elif(self.trueDirection == "LEFT"):
            self.trueDirection = "RIGHT"
        
        if(self.trueDirection == self.detectedDirection):
            color = "BLUE"
        else:
            color = "RED"
        
        self.ArrowFrameControl.showArrow(self.detectedDirection, color)
    
    def resetControlsPosition(self):
        self.ArrowFrameControl.centerPosition()
        x = (self.centralwidget.width() - self.Arrows_Frame_Normal.width()) / 2
        y = (self.centralwidget.height() - self.Arrows_Frame_Normal.height()) / 2
        
        y += self.Arrows_Frame_Normal.height() + 30
        self.NoteFrame_1.move(x, y)
        self.NoteFrame_2.move(x, y)
        self.NoteFrame_3.move(x, y)
        self.NoteFinished.move(x, y)
        
        self.WelcomeFrameCtrl.centerPosition()
        #x = (self.centralwidget.width() - self.WelcomeFrame.width()) / 2
        #y = (self.centralwidget.height() - self.WelcomeFrame.height()) / 2
        #self.WelcomeFrame.move(x, y)
        
        self.detalisParent_Frame.setGeometry(QtCore.QRect(10, 10, self.centralwidget.width()-20, 60))
        self.details_Line.setGeometry(QtCore.QRect(0, 50, self.detalisParent_Frame.width(), 16))
        self.detalisChild_Frame.setGeometry(QtCore.QRect(0, 0, self.detalisParent_Frame.width()-30, 50))
        self.toggleIcon.setGeometry(QtCore.QRect(self.detalisChild_Frame.width(), 0, 24, 24))
        self.untoggleIcon.setGeometry(QtCore.QRect(self.detalisChild_Frame.width()+10, 10, 24, 24))
        
        x = (self.centralwidget.width() - self.NoteFinished.width()) / 2
        y = (self.centralwidget.height() - self.NoteFinished.height()) / 2
        self.NoteFinished.move(x, y)

    def setNote2_Label(self, state):
        self.Note2_Label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">" + state + "</span></p></body></html>")

    def setNote3_Label(self, direction):
        self.Note3_Label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">" + direction + " detected.</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Wrong? Press escape, spacebar or hit this button:</span></p></body></html>")
    '''
    def setNote3_Label(self, direction):
        self.Note3_Label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">" + direction + " detected.</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Wrong? Press escape, spacebar or hit this button:</span></p></body></html>")
    '''
    def setNoteFinished_Label(self, FileName):
        self.NoteFinished_Label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">Thank you for your participation.</span></p><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Data saved to: </span><span style=\" font-size:10pt;\">" + FileName + "</span></p></body></html>")

    def setNumberOfTrials_Label(self):
        self.NumberOfTrials_Label.setText("<html><head/><body><p><span style=\" color:#9a9a9a;\">(" + str(self.NumberOfTrueTrials) + ")</span> " + str(self.NumberOfDoneTrials) + "/" + str(self.NumberOfTrials) + "</p></body></html>")

    def setTimeRemaining_Label(self):
        TimeRemaining = (self.BlankTime + self.SteadyTime + self.RecordingTime + self.PostRecordingTime + self.AvgDetectionTime) * (self.NumberOfTrials - self.NumberOfDoneTrials)
        ext = " sec"
        
        if(TimeRemaining > 3600):
            TimeRemaining /= 3600
            ext = " hr"
            
        elif(TimeRemaining > 60):
            TimeRemaining /= 60
            ext = " min"
        
        self.TimeRemaining_Label.setText( str(int(TimeRemaining)) + ext )

    def setAvgTime_Label(self):
        self.AvgTime_Label.setText( str("%.2f" % self.AvgDetectionTime) + " sec" )

    def setAccuracy_ProgBar(self):        
        if(self.NumberOfDoneTrials > 0):
            Accuracy = (self.NumberOfTrueTrials * 1.0 / self.NumberOfDoneTrials) * 100
        else:
            Accuracy = 0
        
        self.Accuracy_ProgBar.setValue( int(Accuracy) )

    def setFinished_ProgBar(self):
        Finished = (self.NumberOfDoneTrials * 1.0 / self.NumberOfTrials) * 100
        self.Finished_ProgBar.setValue( int(Finished) )

    def updateDetails(self):
        self.setNumberOfTrials_Label()
        self.setTimeRemaining_Label()
        self.setAvgTime_Label()
        self.setAccuracy_ProgBar()
        self.setFinished_ProgBar()

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

    #EVENTS

    def RecordingProgBarTimer_Timeout(self):
        self.Recording_ProgBar.setValue(self.Recording_ProgBar.value() + 1)

    def TrialDataTimer_Timeout(self):        
        if(self.EEG.eeg_triggers[-1]):
            if((len(self.EEG.eeg_counter) - self.EEG.eeg_triggers[-1]) >= (self.EEG.fps * self.RecordingTime)):
                self.setNote2_Label("Detecting...")
                
                self.isDetecting = True
                self.Start_DetectionTime = time.time()
                TrialData = self.EEG.getLastTrial(self.RecordingTime)
                self.Detector.detect(TrialData)
                self.TrialDataTimer.stop()

    def SaveThread_DataSaved(self, filename):
        self.NoteFinished_Label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">Thank you for your participation.</span></p><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Data saved to: </span><span style=\" font-size:10pt;\">" + filename + "</span></p></body></html>")
        
        if(AppConfig.PrintSessionDetails):
            print "Finished, data saved to " + filename

    def DetectThread_Detected(self, DetectOut):
        self.ArrowFrameControl.resetArrows()
        
        self.End_DetectionTime = time.time()
        New_DetectionTime = self.End_DetectionTime - self.Start_DetectionTime
        self.AvgDetectionTime = ((self.AvgDetectionTime * self.NumberOfDoneTrials) + New_DetectionTime) / (self.NumberOfDoneTrials + 1)
        
        self.detectedDirection = DetectOut
        #self.trueDirection = DetectOut
        
        if(self.detectedDirection == self.trueDirection):
            color = "GREEN"
        else:
            color = "RED"
        
        self.setNote3_Label(self.detectedDirection.title())
        
        print self.detectedDirection
        
        self.ArrowFrameControl.showArrow(self.detectedDirection, color)
        
        if(AppConfig.EnableMotors):
            if(self.detectedDirection == "RIGHT"):
                self.motor.goRight()
                time.sleep(AppConfig.MotorStopDelay)
                self.motor.stop()
            
            elif(self.detectedDirection == "LEFT"):
                self.motor.goLeft()
                time.sleep(AppConfig.MotorStopDelay)
                self.motor.stop()
            
            elif(self.detectedDirection == "FORWARD"):
                self.motor.goForward()
                time.sleep(AppConfig.FWDMotorStopDelay)
                self.motor.stop()
        
        if(AppConfig.PrintSessionDetails):
            print self.detectedDirection + " Detected in " + str("%.2f" % self.AvgDetectionTime) + " sec"
        
        self.NoteFrame_2.setVisible(False)
        self.NoteFrame_3.setVisible(True)
        
        self.WrongButton.setFocus(True)
        
        self.Time = self.NumberOfDoneTrials * (self.BlankTime + self.SteadyTime + self.RecordingTime + self.PostRecordingTime) + self.BlankTime + self.SteadyTime + self.RecordingTime
        self.finishedDetect = True

    def TrainingTimer_Timeout(self):
        if(self.finishedDetect):
            if(self.Detector):
                if(self.Detector.DetectionStarted):
                    if(self.NumberOfDoneTrials < self.NumberOfTrials):
                        Time_abs = self.Time - self.NumberOfDoneTrials * (self.BlankTime + self.SteadyTime + self.RecordingTime + self.PostRecordingTime)
                        
                        if(Time_abs >= self.BlankTime + self.SteadyTime + self.RecordingTime + self.PostRecordingTime):
                            if(self.flag != "Blank"):
                                self.flag = "Blank"
                                self.TrainingTimer.emit( QtCore.SIGNAL('NewTrialFlag()') )
                        
                        elif(Time_abs >= self.BlankTime + self.SteadyTime + self.RecordingTime):
                            if(self.flag != "Detect"):
                                self.flag = "Detect"
                                self.finishedDetect = False
                                self.TrainingTimer.emit( QtCore.SIGNAL('DetectFlag()') )
                        
                        elif(Time_abs >= self.BlankTime + self.SteadyTime):
                            if(self.flag != "Recording"):
                                self.flag = "Recording"
                                self.TrainingTimer.emit( QtCore.SIGNAL('RecordingFlag()') )
                                                
                        elif(Time_abs >= self.BlankTime):
                            if(self.flag != "Steady"):
                                self.flag = "Steady"
                                self.TrainingTimer.emit( QtCore.SIGNAL('SteadyFlag()') )
                        
                        elif(Time_abs >= 0):
                            if(self.flag != "Blank"):
                                self.flag = "Blank"
                                self.TrainingTimer.emit( QtCore.SIGNAL('BlankFlag()') )
                        
                    else:
                        Time_abs = self.Time - self.NumberOfDoneTrials * (self.BlankTime + self.SteadyTime + self.RecordingTime + self.PostRecordingTime)
                        self.NoteFrame_1.setVisible(False)
                        self.ArrowFrameControl.hideFrame()
                        
                        if(Time_abs > self.PostFinishTime):
                            self.TrainingTimer.stop()
                            self.EEG.saveToFile(self.getSessionDetails())
                            self.NoteFinished_Label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">Saving, please wait...</span></p></body></html>")
                            self.NoteFinished.setVisible(True)
                        
                        
                    self.Time += 1

    def TrainingTimer_NewTrialFlag(self):
        self.NumberOfDoneTrials += 1
        
        if(self.detectedDirection == self.trueDirection):
            self.NumberOfTrueTrials += 1
        
        self.updateDetails()
        
        self.EEG.setDetectedDirection(self.detectedDirection, self.trueDirection, self.SessionDetails["ClassesNames"])
        
        self.NoteFrame_3.setVisible(False)
        if(self.NumberOfDoneTrials != self.NumberOfTrials):
            self.NoteFrame_1.setVisible(True)
        self.ArrowFrameControl.resetArrows()
        self.detectedDirection = ""
        self.trueDirection = ""
        self.ArrowFrameControl.hideFrame()

    def TrainingTimer_DetectFlag(self):
        self.RecordingProgBarTimer.stop()
        self.Recording_ProgBar.setValue(100)
        self.TrialDataTimer.start(100)

    def TrainingTimer_RecordingFlag(self):
        self.NoteFrame_1.setVisible(False)
        self.NoteFrame_2.setVisible(True)
        self.setNote2_Label("Start!")
        self.Recording_ProgBar.setValue(0)
        self.RecordingProgBarTimer.start(self.RecordingTime * 1000 / 100)
        self.EEG.setTrigger()
        
        self.ArrowFrameControl.resetArrows()
        
        self.ArrowFrameControl.showArrow(self.trueDirection, "BLUE")
        
        '''
        if(self.trueDirection == "RIGHT"):
            self.setRightArrowColor("BLUE")
        elif(self.trueDirection == "LEFT"):
            self.setLeftArrowColor("BLUE")
        '''
        
        if(AppConfig.PrintSessionDetails):
            print "Recording..."
    
    def getRandomClass(self):
        RemainingClasses = []
        
        # Get Remaining Classes
        for c in self.SessionDetails["ClassesNames"]:
            if( self.SessionDetails["DoneTrials"][c] < self.SessionDetails["nTrials"] ):
                RemainingClasses.append(c)
        
        print RemainingClasses
        
        for c in self.SessionDetails["ClassesNames"]:
            print c, self.SessionDetails["DoneTrials"][c]
        
        # Select Randome Class
        RndInt = randint(0, len(RemainingClasses)-1)
        
        return RemainingClasses[RndInt]
    
    def TrainingTimer_SteadyFlag(self):
        self.ArrowFrameControl.showFrame()
        c = self.getRandomClass()
        self.trueDirection = c
        self.SessionDetails["DoneTrials"][c] = self.SessionDetails["DoneTrials"][c] + 1
    
    def TrainingTimer_BlankFlag(self):
        self.ArrowFrameControl.hideFrame()
        self.NoteFrame_3.setVisible(False)
        self.NoteFrame_1.setVisible(True)

    def untoggleIcon_Clicked(self, event):
        self.detalisParent_Frame.setVisible(True)

    def toggleIcon_Clicked(self, event):
        self.detalisParent_Frame.setVisible(False)

    def onResize(self, event):
        self.resetControlsPosition()

    def onkeyPress(self, event):
        if type(event) == QtGui.QKeyEvent and event.key() == QtCore.Qt.Key_Escape : 
            self.triggerWrongTrial()
        elif type(event) == QtGui.QKeyEvent and event.key() == QtCore.Qt.Key_Space : 
            self.triggerWrongTrial()

    def WrongButton_Clicked(self):
        self.triggerWrongTrial()

    def Start_Button_Clicked(self):
        #self.WelcomeFrame.setVisible(False)
        self.WelcomeFrameCtrl.hideFrame()
        self.ArrowFrameControl.showFrame()
        self.Detector.startDetection()
        self.TrainingTimer.start(1000)