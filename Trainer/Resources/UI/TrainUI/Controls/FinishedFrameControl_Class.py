from PyQt4 import QtCore, QtGui

class FinishedFrameControl (QtCore.QObject):
    def __init__(self, TrainWindow):
        QtCore.QObject.__init__(self)
        
        # Connecting to Train Window
        self.TW = TrainWindow
    
    def centerPosition(self):
        x = (self.TW.centralwidget.width() - self.TW.FinishedNote_Frame.width()) / 2
        y = (self.TW.centralwidget.height() - self.TW.FinishedNote_Frame.height()) / 2
        self.TW.FinishedNote_Frame.move(x, y)
    
    def hideFrame(self):
        self.TW.FinishedNote_Frame.setVisible(False)
    
    def showFrame(self, filename):
        SessionName = self.TW.SessionDetails["SessionName"]
        
        self.TW.FinishedNote_Label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">Thank you for your participation.</span></p><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Data saved to: </span><span style=\" font-size:10pt;\">TrainingData</span><span style=\" font-size:10pt; font-weight:600;\">/</span><span style=\" font-size:10pt;\">" + SessionName + "</span><span style=\" font-size:10pt; font-weight:600;\">/</span><span style=\" font-size:10pt;\">"+ filename +"</span></p></body></html>")
        self.TW.FinishedNote_Frame.setVisible(True)