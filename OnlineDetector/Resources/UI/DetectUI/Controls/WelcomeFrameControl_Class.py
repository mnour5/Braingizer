from PyQt4 import QtCore, QtGui

class WelcomeFrameControl (QtCore.QObject):
    def __init__(self, DetectWindow):
        QtCore.QObject.__init__(self)
        
        # Connecting to Detect Window
        self.DW = DetectWindow
    
    def initializeWelcomeNote(self):
        Session = self.DW.SessionDetails
        Name = Session["ProfileName"]
        nTrials_total = str(Session["nTrials_Total"])
        
        if(Session["nClasses"] > 1):
            nClasses = str(Session["nClasses"])+ " classes"
        else:
            nClasses = "1 class"
        
        ClassesNames = ""
        for i, c in enumerate(Session["ClassesNames"]):
            ClassesNames = ClassesNames + "<li>" + c.capitalize() + "</li>"
        
        self.DW.WelcomeNote_Label.setText("<html><head/><body><p align=\"justify\">Welcome " + Name + ",</p><p align=\"justify\"><span style=\" font-weight:400;\">Kindly set in a comfortable chair with armrests.</span></p><p align=\"justify\"><span style=\" font-weight:400;\">You will have a number of </span>" + nTrials_total + " trials<span style=\" font-weight:400;\"> for </span>" + nClasses + "<span style=\" font-weight:400;\">:</span></p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">" + ClassesNames + "</ul><p align=\"justify\"><span style=\" font-weight:400;\">Thank you for your participation, click the start button whenever you are ready.</span></p></body></html>")
    
    def centerPosition(self):
        x = (self.DW.centralwidget.width() - self.DW.Welcome_Frame.width()) / 2
        y = (self.DW.centralwidget.height() - self.DW.Welcome_Frame.height()) / 2
        self.DW.Welcome_Frame.move(x, y)
    
    def hideFrame(self):
        self.DW.Welcome_Frame.setVisible(False)
    
    def showFrame(self):
        self.DW.Welcome_Frame.setVisible(True)
    