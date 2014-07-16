import AppConfig
from PyQt4 import QtCore, QtGui

class TimerControl (QtCore.QObject):
    def __init__(self, TrainWindow):
        QtCore.QObject.__init__(self)
        
        # Connecting to Train Window
        self.TW = TrainWindow
        
        #Training Timer
        self.TW.TrainingTimer = QtCore.QTimer()
        self.TW.TrainingTimer.timeout.connect(self.TrainingTimer_Timeout)
        
        # Connecting Train Window with Events
        QtCore.QObject.connect(self, QtCore.SIGNAL("NewTrialFlag()"), self.TW.TimerCtrl_NewTrialFlag)
        QtCore.QObject.connect(self, QtCore.SIGNAL("BlankFlag()"), self.TW.TimerCtrl_BlankFlag)
        QtCore.QObject.connect(self, QtCore.SIGNAL("SteadyFlag()"), self.TW.TimerCtrl_SteadyFlag)
        QtCore.QObject.connect(self, QtCore.SIGNAL("RecordingFlag()"), self.TW.TimerCtrl_RecordingFlag)
        QtCore.QObject.connect(self, QtCore.SIGNAL("TrainingFinishedFlag()"), self.TW.TimerCtrl_TrainingFinishedFlag)
    
    def initializeTimer(self):
        # Timer variables
        self.Time = 0
        self.flag = ""

    def StartTimer(self):
        self.TW.TrainingTimer.start(1000)
    
    def StopTimer(self):
        self.TW.TrainingTimer.stop()
        self.initializeTimer()
    
    def TrainingTimer_Timeout(self):
        SessionDetails = self.TW.SessionDetails
        
        nTrials_Total       = SessionDetails["nTrials_Total"]
        DoneTrials_Total    = SessionDetails["DoneTrials_Total"]
        
        BlankTime       = SessionDetails["BlankTime"]
        SteadyTime      = SessionDetails["SteadyTime"]
        TrainingTime    = SessionDetails["TrainingTime"]
        
        if(DoneTrials_Total < nTrials_Total):
            Time_abs = self.Time - DoneTrials_Total * (BlankTime + SteadyTime + TrainingTime)
            
            if(Time_abs >= BlankTime + SteadyTime + TrainingTime):
                if(self.flag != "Blank"):
                    self.flag = "Blank"
                    self.emit( QtCore.SIGNAL('NewTrialFlag()') )
            
            elif(Time_abs >= BlankTime + SteadyTime):
                if(self.flag != "Recording"):
                    self.flag = "Recording"
                    self.finishedDetect = False
                    self.emit( QtCore.SIGNAL('RecordingFlag()') )
            
            elif(Time_abs >= BlankTime):
                if(self.flag != "Steady"):
                    self.flag = "Steady"
                    self.emit( QtCore.SIGNAL('SteadyFlag()') )
            
            elif(Time_abs >= 0):
                if(self.flag != "Blank"):
                    self.flag = "Blank"
                    self.emit( QtCore.SIGNAL('BlankFlag()') )
            
        else:
            Time_abs = self.Time - nTrials_Total * (BlankTime + SteadyTime + TrainingTime)
            # Hide all frames
            
            if(Time_abs > AppConfig.PostFinishTime):
                self.emit( QtCore.SIGNAL('TrainingFinishedFlag()') )
                self.TW.TrainingTimer.stop()
        
        self.Time += 1