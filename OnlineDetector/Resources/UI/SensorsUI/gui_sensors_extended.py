from PyQt4 import QtCore, QtGui
from gui_sensors import Ui_SensorsWindow
from epoc import *
import math

class Ui_SensorsWindow_Extended(Ui_SensorsWindow):
    def InitializeUI(self, EEG):
        self.addSensorControls()
        self.EEG = EEG
        
        #QTimer
        self.SensorsTimer = QtCore.QTimer()
        self.SensorsTimer.timeout.connect(self.SensorsTimer_Timeout)
        self.SensorsTimer.start(1000)
    
    def addSensorControls(self):
        self.sensors = SensorsControlList(self)
    
    def SensorsTimer_Timeout(self):
        if(self.EEG.connected):
            self.quality = self.EEG.eeg_quality
            self.sensors.updateSensorsControlList(self.quality)

class SensorsControlList():
    def __init__(self, ui):
        self.sensors = {
            'F3':   SensorControl(ui,   'F3',   175, 158),
            'FC6':  SensorControl(ui,   'FC6',  374, 197),
            'P7':   SensorControl(ui,   'P7',   102, 355),
            'T8':   SensorControl(ui,   'T8',   430, 252),
            'F7':   SensorControl(ui,   'F7',   108, 144),
            'F8':   SensorControl(ui,   'F8',   391, 144),
            'T7':   SensorControl(ui,   'T7',    73, 252),
            'P8':   SensorControl(ui,   'P8',   398, 355),
            'F4':   SensorControl(ui,   'F4',   324, 158),
            'AF4':  SensorControl(ui,   'AF4',  303, 119),
            'AF3':  SensorControl(ui,   'AF3',  196, 119),
            'O2':   SensorControl(ui,   'O2',   306, 421),
            'O1':   SensorControl(ui,   'O1',   197, 421),
            'FC5':  SensorControl(ui,   'FC5',  126, 197)
        }
    
    def updateSensorsControlList(self, quality):
        if(quality):
            for i, channel in enumerate(EPOC.channels):
                if(quality[channel]):
                    if(quality[channel][-1]):
                        self.sensors[channel].updateSensorControl(quality[channel][-1])

class SensorControl():
    def __init__(self, ui, SensorName, x, y):
        self.SensorName = SensorName
        self.createCircle(ui, x, y)
        self.createLabel(ui, x, y)

    def updateSensorControl(self, SensorQuality):
        '''
        From emotiv SDK
        GOOD: 4
        FAIR: 3
        POOR: 2
        VERY_BAD: 1
        NO_SIGNAL: 0
        '''

        GOOD = 11
        FAIR = 7
        POOR = 5
        VERY_BAD = 3
        #NO_SIGNAL = 0
        
        self.changeLabelText(str(math.ceil(SensorQuality*100)/100))
        
        if(SensorQuality > GOOD):
            self.setColor("GREEN")
        elif(SensorQuality > FAIR):
            self.setColor("YELLOW")
        elif(SensorQuality > POOR):
            self.setColor("ORANGE")
        elif(SensorQuality > VERY_BAD):
            self.setColor("RED")
        else:
            self.setColor("BLACK")

    def createCircle(self, ui, x, y):
        self.circle = QtGui.QLabel(ui.centralwidget)
        self.circle.setGeometry(QtCore.QRect(x, y, 36, 36))
        self.circle.setText("")
        self.circle.setPixmap(QtGui.QPixmap("Resources/IMGs/SensorsUI_SensorBlack.png"))

    def createLabel(self, ui, x, y):
        self.label = QtGui.QLabel(ui.centralwidget)
        self.label.setGeometry(QtCore.QRect(x, y+12, 36, 40))
        #self.label.setStyleSheet("background-color:rgb(85, 255, 0);")
        labelText = "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600; color:#ffffff;\">" + self.SensorName + "</span></p></body></html>"
        self.label.setText(labelText)
    
    def changeLabelText(self, Text):
        labelText = "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600; color:#ffffff;\">" + self.SensorName + "<p align=\"center\"><span style=\" font-size:8pt; font-weight:600; color:#000000;\">" + Text + "</span></p></body></html>"
        self.label.setText(labelText)
    
    def setColor(self, color):
        if(color == "RED"):
            self.circle.setPixmap(QtGui.QPixmap("Resources/IMGs/SensorsUI_SensorRed.png"))
        elif(color == "GREEN"):
            self.circle.setPixmap(QtGui.QPixmap("Resources/IMGs/SensorsUI_SensorGreen.png"))
        elif(color == "BLACK"):
            self.circle.setPixmap(QtGui.QPixmap("Resources/IMGs/SensorsUI_SensorBlack.png"))
        elif(color == "YELLOW"):
            self.circle.setPixmap(QtGui.QPixmap("Resources/IMGs/SensorsUI_SensorYellow.png"))
        elif(color == "ORANGE"):
            self.circle.setPixmap(QtGui.QPixmap("Resources/IMGs/SensorsUI_SensorYellow.png"))
        else:
            self.circle.setPixmap(QtGui.QPixmap("Resources/IMGs/SensorsUI_SensorGrey.png"))