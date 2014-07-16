import AppConfig
from PyQt4 import QtCore, QtGui

class ArrowFrameControl (QtCore.QObject):
    def __init__(self, DetectWindow):
        QtCore.QObject.__init__(self)
        
        # Connecting to Train Window
        self.TW = DetectWindow
    
    def initializeArrows(self):
        self.Arrows = {}
        self.GreyImgs   = {}
        self.BlueImgs   = {}
        self.RedImgs    = {}
        self.GreenImgs  = {}
        
        # Check if it's only RIGHT and LEFT classes
        if(self.isOnlyLeftAndRight()):
            # The arrows frame
            self.Arrows_Frame       = self.TW.Arrows_Frame_Normal
            
            # To arrows
            self.Arrows['RIGHT']    = self.TW.RightArrow_Normal
            self.Arrows['LEFT']     = self.TW.LeftArrow_Normal
            
            # Grey Arrow Imgs
            self.GreyImgs['RIGHT']  = "Resources/IMGs/DetectUI_RightArrow_Normal_Grey.png"
            self.GreyImgs['LEFT']   = "Resources/IMGs/DetectUI_LeftArrow_Normal_Grey.png"
            
            # Blue Arrow Imgs
            self.BlueImgs['RIGHT']  = "Resources/IMGs/DetectUI_RightArrow_Normal_Blue.png"
            self.BlueImgs['LEFT']   = "Resources/IMGs/DetectUI_LeftArrow_Normal_Blue.png"
            
            # Red Arrow Imgs
            self.RedImgs['RIGHT']  = "Resources/IMGs/DetectUI_RightArrow_Normal_Red.png"
            self.RedImgs['LEFT']   = "Resources/IMGs/DetectUI_LeftArrow_Normal_Red.png"
            
            # Green Arrow Imgs
            self.GreenImgs['RIGHT']  = "Resources/IMGs/DetectUI_RightArrow_Normal_Green.png"
            self.GreenImgs['LEFT']   = "Resources/IMGs/DetectUI_LeftArrow_Normal_Green.png"
            
        else:
            # The arrows frame
            self.Arrows_Frame = self.TW.Arrows_Frame
            
            # To arrows
            self.Arrows['RIGHT']        = self.TW.RightArrow
            self.Arrows['LEFT']         = self.TW.LeftArrow
            self.Arrows['BACK']         = self.TW.BwdArrow
            self.Arrows['FORWARD']      = self.TW.FwdArrow
            self.Arrows['NEUTRAL']      = self.TW.StopCircle
            
            # Grey Arrow Imgs
            self.GreyImgs['RIGHT']          = "Resources/IMGs/DetectUI_RightArrow_Grey.png"
            self.GreyImgs['LEFT']           = "Resources/IMGs/DetectUI_LeftArrow_Grey.png"
            self.GreyImgs['BACK']           = "Resources/IMGs/DetectUI_BackArrow_Grey.png"
            self.GreyImgs['FORWARD']        = "Resources/IMGs/DetectUI_FWDArrow_Grey.png"
            self.GreyImgs['NEUTRAL']        = "Resources/IMGs/DetectUI_Stop_Grey.png"
            
            # Blue Arrow Imgs
            self.BlueImgs['RIGHT']          = "Resources/IMGs/DetectUI_RightArrow_Blue.png"
            self.BlueImgs['LEFT']           = "Resources/IMGs/DetectUI_LeftArrow_Blue.png"
            self.BlueImgs['BACK']           = "Resources/IMGs/DetectUI_BackArrow_Blue.png"
            self.BlueImgs['FORWARD']        = "Resources/IMGs/DetectUI_FWDArrow_Blue.png"
            self.BlueImgs['NEUTRAL']        = "Resources/IMGs/DetectUI_Stop_Blue.png"
            
            # Red Arrow Imgs
            self.RedImgs['RIGHT']          = "Resources/IMGs/DetectUI_RightArrow_Red.png"
            self.RedImgs['LEFT']           = "Resources/IMGs/DetectUI_LeftArrow_Red.png"
            self.RedImgs['BACK']           = "Resources/IMGs/DetectUI_BackArrow_Red.png"
            self.RedImgs['FORWARD']        = "Resources/IMGs/DetectUI_FWDArrow_Red.png"
            self.RedImgs['NEUTRAL']        = "Resources/IMGs/DetectUI_Stop_Red.png"
            
            # Green Arrow Imgs
            self.GreenImgs['RIGHT']          = "Resources/IMGs/DetectUI_RightArrow_Green.png"
            self.GreenImgs['LEFT']           = "Resources/IMGs/DetectUI_LeftArrow_Green.png"
            self.GreenImgs['BACK']           = "Resources/IMGs/DetectUI_BackArrow_Green.png"
            self.GreenImgs['FORWARD']        = "Resources/IMGs/DetectUI_FWDArrow_Green.png"
            self.GreenImgs['NEUTRAL']        = "Resources/IMGs/DetectUI_Stop_Green.png"
        
        # Hide arrows
        self.TW.Arrows_Frame.setVisible(False)
        self.TW.Arrows_Frame_Normal.setVisible(False)
        
        # Center Frame
        self.centerPosition()
        
        # Show all arrows
        for arrow in self.Arrows:
            self.Arrows[arrow].setVisible(True)
            self.Arrows[arrow].setPixmap(QtGui.QPixmap( self.GreyImgs[arrow] ))
        
        # Show arrows for selected classes only
        '''
        for arrow in self.Arrows:
            self.Arrows[arrow].setVisible(False)
        
        ClassesNames = self.TW.SessionDetails["ClassesNames"]
        
        for c in ClassesNames:
            self.Arrows[c].setVisible(True)
            self.Arrows[c].setPixmap(QtGui.QPixmap( self.GreyImgs[c] ))
        '''
    
    def hideFrame(self):
        self.Arrows_Frame.setVisible(False)
    
    def showFrame(self):
        self.Arrows_Frame.setVisible(True)
    
    def hideArrows(self):
        for arrow in self.Arrows:
            self.Arrows[arrow].setVisible(False)
    
    def resetArrows(self):
        ClassesNames = self.TW.SessionDetails["ClassesNames"]
        
        for c in ClassesNames:
            self.Arrows[c].setPixmap(QtGui.QPixmap( self.GreyImgs[c] ))
    
    def showArrow(self, direction, color="BLUE"):
        if(color == "RED"):
            self.Arrows[direction].setPixmap(QtGui.QPixmap( self.RedImgs[direction] ))
        elif(color == "GREEN"):
            self.Arrows[direction].setPixmap(QtGui.QPixmap( self.GreenImgs[direction] ))
        else:
            self.Arrows[direction].setPixmap(QtGui.QPixmap( self.BlueImgs[direction] ))
    
    def centerPosition(self):
        x = (self.TW.centralwidget.width() - self.TW.Arrows_Frame.width()) / 2
        y = (self.TW.centralwidget.height() - self.TW.Arrows_Frame.height()) / 2
        self.TW.Arrows_Frame.move(x, y)
        
        x = (self.TW.centralwidget.width() - self.TW.Arrows_Frame_Normal.width()) / 2
        y = (self.TW.centralwidget.height() - self.TW.Arrows_Frame_Normal.height()) / 2
        self.TW.Arrows_Frame_Normal.move(x, y)
    
    def isOnlyLeftAndRight(self):
        for c in self.TW.SessionDetails["ClassesNames"]:
            if(c != "RIGHT" and c != "LEFT"):
                print c
                return False
        
        return True