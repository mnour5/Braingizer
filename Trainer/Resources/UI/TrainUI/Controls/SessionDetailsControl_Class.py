import AppConfig
from PyQt4 import QtCore, QtGui
from random import randint

class SessionDetailsControl (QtCore.QObject):
    def __init__(self, TrainWindow):
        QtCore.QObject.__init__(self)
        
        # Connecting to Train Window
        self.TW         = TrainWindow
    
    def addDoneTrial(self):
        self.Session["DoneTrials"][self.TW.RndClass] += 1
        
        DoneTrials_Total = 0
        
        for c in self.Session["ClassesNames"]:
            DoneTrials_Total += self.Session["DoneTrials"][c]
        
        self.Session["DoneTrials_Total"] = DoneTrials_Total
        
        # Debug
        if(AppConfig.DebugTrainingSession):
            print ""
            for c in self.Session["ClassesNames"]: print c, self.Session["DoneTrials"][c]
            print ""
    
    def getClassNumber(self, ClassName):
        ClassNumber = 0
        
        for i, c in enumerate(self.Session["ClassesNames"]):
            if(ClassName == c):
                ClassNumber = i+1
        
        return ClassNumber
    
    def getRandomClass(self):
        RemainingClasses = []
        
        # Get Remaining Classes
        for c in self.Session["ClassesNames"]:
            if( self.Session["DoneTrials"][c] < self.Session["nTrials"] ):
                RemainingClasses.append(c)
        
        # Select Randome Class
        RndInt = randint(0, len(RemainingClasses)-1)
        
        ClassNumber = 0
        
        for i, c in enumerate(self.Session["ClassesNames"]):
            if(RemainingClasses[RndInt] == c):
                ClassNumber = i+1
        
        return RemainingClasses[RndInt], ClassNumber
    
    def getSessionDetails(self, Profile, Session):
        # Initializing
        self.TW.SessionDetails = {}
        self.Session = self.TW.SessionDetails
        
        # Profile Name
        self.Session["ProfileName"]  = Profile["Name"]
        
        # Session Name
        self.Session["SessionName"]  = Session["Name"]
        
        # Classes Names
        self.Session["ClassesNames"] = []
        
        for s in AppConfig.SortedClasses:
            for c in Session["SubElement"]["TrainingClasses"]:
                if((Session["SubElement"]["TrainingClasses"][c] == "True") and (c==s)):
                    self.Session["ClassesNames"].append(c)
        
        # Number of Trials & Classes
        self.Session["nTrials"]          = int( Session["SubElement"]["TimingOptions"]["NumberOfTrials"] )
        self.Session["nClasses"]         = len( self.Session["ClassesNames"] )
        self.Session["nTrials_Total"]    = self.Session["nTrials"] * self.Session["nClasses"]
        
        # Timing Details
        self.Session["BlankTime"]        = int( Session["SubElement"]["TimingOptions"]["BlankTime"] )
        self.Session["SteadyTime"]       = int( Session["SubElement"]["TimingOptions"]["SteadyTime"] )
        self.Session["TrainingTime"]     = int( Session["SubElement"]["TimingOptions"]["TrainingTime"] )
        
        self.Session["TrialTime"]        = self.Session["BlankTime"] + self.Session["SteadyTime"] + self.Session["TrainingTime"]
        self.Session["TimeTotal"]        = self.Session["TrialTime"] * self.Session["nTrials_Total"]
        
        # Done Trials
        self.Session["DoneTrials"]       = {}
        for c in self.Session["ClassesNames"]:
            self.Session["DoneTrials"][c]= 0
        
        self.Session["DoneTrials_Total"] = 0