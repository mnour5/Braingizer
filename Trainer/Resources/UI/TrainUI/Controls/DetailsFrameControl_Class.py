import AppConfig
from PyQt4 import QtCore, QtGui

class DetailsFrameControl (QtCore.QObject):
    def __init__(self, TrainWindow):
        QtCore.QObject.__init__(self)
        
        # Connecting to Train Window
        self.TW = TrainWindow
        
        # Events
        self.TW.toggleIcon.mouseReleaseEvent = self.toggleIcon_Clicked
        self.TW.untoggleIcon.mouseReleaseEvent = self.untoggleIcon_Clicked
    
    def initializeComponents(self):
        self.Session = self.TW.SessionDetails
        
        self.updateName_Label()
        self.updateNumberOfTrials_Label()
        self.updateEstimatedTime_Label()
        self.updateClassesNames_Label()
        self.updateFinished_ProgBar()
    
    def update(self):
        self.updateNumberOfTrials_Label()
        self.updateEstimatedTime_Label()
        self.updateFinished_ProgBar()

    def updateName_Label(self):
        self.TW.Name_Label.setText(self.Session["ProfileName"])
    
    def updateNumberOfTrials_Label(self):
        self.TW.NumberOfTrials_Label.setText("<html><head/><body><p> " + str(self.Session["DoneTrials_Total"]) + "/" + str(self.Session["nTrials_Total"]) + " <span style=\" color:#9a9a9a;\">(" + str(self.Session["nClasses"]) + "x" + str(self.Session["nTrials"]) + ")</span></p></body></html>")
    
    def updateEstimatedTime_Label(self):
        TimeRemaining = self.Session["TimeTotal"] - self.Session["DoneTrials_Total"] * self.Session["TrialTime"]
        
        if(TimeRemaining > 60*60):
            TimeRemainingText   = str(TimeRemaining/(60*60)) + " hour"
        elif(TimeRemaining > 60):
            TimeRemainingText   = str(TimeRemaining/(60)) + " min."
        else:
            TimeRemainingText   = str(TimeRemaining) + " sec."
        
        self.TW.EstimatedTime_Label.setText(TimeRemainingText)
    
    def updateClassesNames_Label(self):
        ClassesNamesText = ""
        if(self.Session["nClasses"] > 1):
            for i, c in enumerate(self.Session["ClassesNames"]):
                if i == self.Session["nClasses"]-1:
                    ClassesNamesText = ClassesNamesText + " & "
                elif i != 0:
                    ClassesNamesText = ClassesNamesText + ", "
                
                ClassesNamesText = ClassesNamesText + c[0]
        else:
            ClassesNamesText = self.Session["ClassesNames"][0][0]
        
        self.TW.ClassesNames_Label.setText(ClassesNamesText)
    
    def updateFinished_ProgBar(self):
        self.TW.Finished_ProgBar.setValue(int(100 * self.Session["DoneTrials_Total"]/self.Session["nTrials_Total"]))
    
    def resetControlsPosition(self):
        self.TW.detalisParent_Frame.setGeometry(QtCore.QRect(10, 10, self.TW.centralwidget.width()-20, 60))
        self.TW.details_Line.setGeometry(QtCore.QRect(0, 50, self.TW.detalisParent_Frame.width(), 16))
        self.TW.detalisChild_Frame.setGeometry(QtCore.QRect(0, 0, self.TW.detalisParent_Frame.width()-30, 50))
        self.TW.toggleIcon.setGeometry(QtCore.QRect(self.TW.detalisChild_Frame.width(), 0, 24, 24))
        self.TW.untoggleIcon.setGeometry(QtCore.QRect(self.TW.detalisChild_Frame.width()+10, 10, 24, 24))
    
    # Events
    def untoggleIcon_Clicked(self, event):
        self.TW.detalisParent_Frame.setVisible(True)

    def toggleIcon_Clicked(self, event):
        self.TW.detalisParent_Frame.setVisible(False)