import AppConfig
from PyQt4 import QtCore, QtGui
from XmlParser_Class import XmlParser

class ProfileControl (QtCore.QObject):
    def __init__(self, MainWindow):
        QtCore.QObject.__init__(self)
        
        self.PersonalDetails_Group  = MainWindow.PersonalDetails_Group
        self.Profile_ComboBox       = MainWindow.Profile_ComboBox
        self.NewProfile_GroupBox    = MainWindow.NewProfile_GroupBox
        self.Name_LineEdit          = MainWindow.Name_LineEdit
        self.Age_LineEdit           = MainWindow.Age_LineEdit
        self.Gender_ComboBox        = MainWindow.Gender_ComboBox
        self.showMessageBox         = MainWindow.showMessageBox
        
        # Get stored profiles
        self.parser = XmlParser()
        self.Profiles = self.parser.getElements('Profile')
        
        # Populating Profile_ComboBox with stored profiles
        for profile in self.Profiles:
            self.Profile_ComboBox.addItem(profile.attrib['Name'])
        
        #EVENTS
        self.Profile_ComboBox.currentIndexChanged['QString'].connect(self.Profile_ComboBox_CurrentIndexChanged)
        
        # Selecting Default Profile from AppConfig
        if(self.parser.elementExist('Profile', AppConfig.Default_Profile )):
            self.Profile_ComboBox.setCurrentIndex( self.Profile_ComboBox.findText( AppConfig.Default_Profile ) )
    
    def checkInputs(self):
        if(self.Profile_ComboBox.currentIndex() == 0):
            if(self.Name_LineEdit.text() == ""):
                self.showMessageBox("Error", "You have to enter the profile name.")
                self.Name_LineEdit.setFocus()
                return False
            elif(self.checkExistence(self.Name_LineEdit.text())):
                self.showMessageBox("Error", "The name \"" + self.Name_LineEdit.text() + "\" already exists.")
                self.Name_LineEdit.setFocus()
                return False
            else:
                return True
        else:
            return True
    
    def Profile_ComboBox_CurrentIndexChanged(self):
        if(self.Profile_ComboBox.currentIndex() == 0):
            # Enable GroupBoxes
            self.NewProfile_GroupBox.setEnabled(True)
            
            # Reset New-Profile Inputs
            self.Name_LineEdit.setText("")
            self.Age_LineEdit.setText("")
        else:
            # Disable GroupBoxes
            self.NewProfile_GroupBox.setEnabled(False)
            
            # Get the index
            idx = self.Profile_ComboBox.currentIndex() - 1
            
            # Get Profile from XML
            Attributes = self.Profiles[idx].attrib
            self.Name_LineEdit.setText(Attributes['Name'])
            self.Age_LineEdit.setText(Attributes['Age'])
            self.Gender_ComboBox.setCurrentIndex( self.Gender_ComboBox.findText( Attributes['Gender'] ) )
    
    def setEnabled(self, opt):
        self.PersonalDetails_Group.setEnabled(opt)
        if(self.Profile_ComboBox.currentIndex() == 0):
            self.NewProfile_GroupBox.setEnabled(opt)
        else:
            self.NewProfile_GroupBox.setEnabled(False)
    
    def getProfile(self):
        Profile = {}
        Profile["Name"]     = self.Name_LineEdit.text()
        Profile["Age"]      = self.Age_LineEdit.text()
        Profile["Gender"]   = self.Gender_ComboBox.itemText(self.Gender_ComboBox.currentIndex())
        
        if(self.Profile_ComboBox.currentIndex() == 0):
            # Storing in the XML file if it's new
            self.parser.addElement("Profile", Profile)
        
        return Profile
    
    def checkExistence(self, ProfileName):
        if(self.parser.elementExist('Profile', ProfileName )):
            return True
        else:
            return False