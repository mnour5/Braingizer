import os
import AppConfig
from time import time
from datetime import datetime
from PyQt4 import QtCore, QtGui
from XmlParser_Class import XmlParser
from TrainingFileClass import TrainingFileClass

class DetectionSessionControl (QtCore.QObject):
    def __init__(self, MainWindow):
        QtCore.QObject.__init__(self)
        
        # Connecting to controls
        self.MW = MainWindow
    
    def getTrainingFile(self):
        Idx             = self.MW.TrainingFile_ComboBox.currentIndex()
        TrainingFile    = self.MW.TrainingFileCtrl.TrainingFiles['Path'][Idx]
        
        return TrainingFile
    
    def getAutorunSessionDetails(self):
        # Initializing
        Session = {}
        
        # Training File
        Session["TrainingFile"] = AppConfig.Autorun_TrainingFile
        filepath = AppConfig.TrainingFolder + "/" + Session["TrainingFile"]
        
        # Profile Name
        Session["ProfileName"] = TrainingFileClass.getName(filepath)
        
        # Classifier Name
        Session["Classifiers"] = str( AppConfig.Autorun_Classifier )
        
        # Classes Names
        ClassesNames = TrainingFileClass.getClasses(filepath)
        Session["ClassesNames"] = []
        
        for s in AppConfig.SortedClasses:
            for c in ClassesNames:
                if(c==s):
                    Session["ClassesNames"].append(c)
        
        # Number of Trials & Classes
        Session["nTrials"]          = AppConfig.Autorun_nTrials
        Session["nClasses"]         = len( Session["ClassesNames"] )
        Session["nTrials_Total"]    = Session["nTrials"] * Session["nClasses"]
        
        # Timing Details
        Session["BlankTime"]            = AppConfig.Autorun_BlankTime
        Session["SteadyTime"]           = AppConfig.Autorun_SteadyTime
        Session["RecordingTime"]        = AppConfig.Autorun_RecordingTime
        Session["PostRecordingTime"]    = AppConfig.Autorun_PostRecordingTime
        
        Session["TrialTime"]        = Session["BlankTime"] + Session["SteadyTime"] + Session["RecordingTime"] + Session["PostRecordingTime"]
        Session["TimeTotal"]        = Session["TrialTime"] * Session["nTrials_Total"]
        
        # Done Trials
        Session["DoneTrials"]       = {}
        for c in Session["ClassesNames"]:
            Session["DoneTrials"][c]= 0
        
        Session["DoneTrials_Total"] = 0
        
        print Session
        
        return Session
    
    def getSessionDetails(self):
        # Initializing
        Session = {}
        
        # Training File
        Session["TrainingFile"] = self.getTrainingFile()
        filepath = AppConfig.TrainingFolder + "/" + Session["TrainingFile"]
        
        # Profile Name
        Session["ProfileName"] = TrainingFileClass.getName(filepath)
        
        # Classifier Name
        Session["Classifiers"] = str( self.MW.Classifiers_ComboBox.currentText() )
        
        # Classes Names
        
        # Classes Names
        ClassesNames = TrainingFileClass.getClasses(filepath)
        Session["ClassesNames"] = []
        
        for s in AppConfig.SortedClasses:
            for c in ClassesNames:
                if(c==s):
                    Session["ClassesNames"].append(c)
        
        # Number of Trials & Classes
        Session["nTrials"]          = int( self.MW.NumberOfTrials_LineEdit.text() )
        Session["nClasses"]         = len( Session["ClassesNames"] )
        Session["nTrials_Total"]    = Session["nTrials"] * Session["nClasses"]
        
        # Timing Details
        Session["BlankTime"]            = int( self.MW.BlankTime_LineEdit.text() )
        Session["SteadyTime"]           = int( self.MW.SteadyTime_LineEdit.text() )
        Session["RecordingTime"]        = int( self.MW.RecordingTime_LineEdit.text() )
        Session["PostRecordingTime"]    = int( self.MW.PostRecordingTime_LineEdit.text() )
        
        Session["TrialTime"]        = Session["BlankTime"] + Session["SteadyTime"] + Session["RecordingTime"] + Session["PostRecordingTime"]
        Session["TimeTotal"]        = Session["TrialTime"] * Session["nTrials_Total"]
        
        # Done Trials
        Session["DoneTrials"]       = {}
        for c in Session["ClassesNames"]:
            Session["DoneTrials"][c]= 0
        
        Session["DoneTrials_Total"] = 0
        
        print Session
        
        return Session