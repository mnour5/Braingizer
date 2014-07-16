import os
import AppConfig
from time import time
from datetime import datetime
from PyQt4 import QtCore, QtGui
from XmlParser_Class import XmlParser

class SessionControl (QtCore.QObject):
    def __init__(self, MainWindow):
        QtCore.QObject.__init__(self)
        
        # Connecting to controls
        self.SessionDetails_Group   = MainWindow.SessionDetails_Group
        self.SessionSub1_Group      = MainWindow.SessionSub1_Group
        self.SessionSub2_Group      = MainWindow.SessionSub2_Group
        self.Right_CheckBox         = MainWindow.Right_CheckBox
        self.Left_CheckBox          = MainWindow.Left_CheckBox
        self.Forward_CheckBox       = MainWindow.Forward_CheckBox
        self.Back_CheckBox          = MainWindow.Back_CheckBox
        self.Neutral_CheckBox       = MainWindow.Neutral_CheckBox
        self.NumberOfTrials_LineEdit= MainWindow.NumberOfTrials_LineEdit
        self.BlankTime_LineEdit     = MainWindow.BlankTime_LineEdit
        self.SteadyTime_LineEdit    = MainWindow.SteadyTime_LineEdit
        self.TrainingTime_LineEdit  = MainWindow.TrainingTime_LineEdit
        self.Sessions_ComboBox      = MainWindow.Sessions_ComboBox
        self.Description_TextEdit   = MainWindow.Description_TextEdit
        self.showMessageBox         = MainWindow.showMessageBox
        self.showQuestionMessageBox = MainWindow.showQuestionMessageBox
        
        # Initializing Settings from AppConfig
        self.IntializeTrainingOptions()
        
        # Get stored sessions
        self.parser = XmlParser()
        self.TrainingSessions = self.parser.getElements('TrainingSession')        
        
        # Populating Sessions_ComboBox with stored sessions
        for Session in self.TrainingSessions:
            self.Sessions_ComboBox.addItem(Session.attrib['Name'])
        
        #EVENTS
        self.Sessions_ComboBox.currentIndexChanged['QString'].connect(self.Sessions_ComboBox_CurrentIndexChanged)
        
        # Selecting Default Session from AppConfig
        if(self.parser.elementExist('TrainingSession', AppConfig.Default_Session )):
            self.Sessions_ComboBox.setCurrentIndex( self.Sessions_ComboBox.findText( AppConfig.Default_Session ) )
        elif(len(self.TrainingSessions) != 0):
            self.Sessions_ComboBox.setCurrentIndex( self.Sessions_ComboBox.findText( self.TrainingSessions[-1].attrib['Name'] ) )
    
    def isNumber(self, value):
        try:
            test_int = int(value)
            if(test_int<1):
                return False
            else:
                return True
        except ValueError:
            return False
    
    def checkInputs(self):
        if(self.Sessions_ComboBox.currentIndex() == 0):
            TrainingClassesCheck = self.Back_CheckBox.isChecked() \
                                    or self.Forward_CheckBox.isChecked() \
                                    or self.Left_CheckBox.isChecked() \
                                    or self.Neutral_CheckBox.isChecked() \
                                    or self.Right_CheckBox.isChecked()
            
            if(not self.isNumber(self.NumberOfTrials_LineEdit.text())):
                self.showMessageBox("Error", "Number of trials has to be a number > 0.")
                self.NumberOfTrials_LineEdit.setFocus()
                return False
            elif(not self.isNumber(self.BlankTime_LineEdit.text())):
                self.showMessageBox("Error", "Blank Time has to be a number > 0.")
                self.BlankTime_LineEdit.setFocus()
                return False
            elif(not self.isNumber(self.BlankTime_LineEdit.text())):
                self.showMessageBox("Error", "Steady Time has to be a number > 0.")
                self.SteadyTime_LineEdit.setFocus()
                return False
            elif(not self.isNumber(self.TrainingTime_LineEdit.text())):
                self.showMessageBox("Error", "Training Time has to be a number > 0.")
                self.TrainingTime_LineEdit.setFocus()
                return False
            elif(not TrainingClassesCheck):
                self.showMessageBox("Error", "You have to choose at least one training class.")
                return False
            else:
                return True
            
        else:
            idx = self.Sessions_ComboBox.currentIndex() - 1
            DateString = self.TrainingSessions[idx].attrib['Name'].split("_")
            SessionDate = datetime(year=int(DateString[1]), month=int(DateString[2]), day=int(DateString[3]))
            
            if(SessionDate.date() != datetime.today().date()):
                reply = self.showQuestionMessageBox("Warning", "The session date is not today, are you sure you want to continue?")
                
                if(not reply):
                    return False
            
            return True
    
    def IntializeTrainingOptions(self):
        #Initializing Training Classes
        self.Right_CheckBox.setChecked(AppConfig.Train_Right)
        self.Left_CheckBox.setChecked(AppConfig.Train_Left)
        self.Forward_CheckBox.setChecked(AppConfig.Train_Forward)
        self.Back_CheckBox.setChecked(AppConfig.Train_Back)
        self.Neutral_CheckBox.setChecked(AppConfig.Train_Neutral)
        
        #Initializing Training Time
        self.NumberOfTrials_LineEdit.setText(str(AppConfig.Number_of_Trials))
        self.BlankTime_LineEdit.setText(str(AppConfig.Blank_Time))
        self.SteadyTime_LineEdit.setText(str(AppConfig.Steady_Time))
        self.TrainingTime_LineEdit.setText(str(AppConfig.Training_Time))
    
    def setEnabled(self, opt):
        self.SessionDetails_Group.setEnabled(opt)
        if(self.Sessions_ComboBox.currentIndex() == 0):
            self.SessionSub1_Group.setEnabled(opt)
            self.SessionSub2_Group.setEnabled(opt)
        else:
            self.SessionSub1_Group.setEnabled(False)
            self.SessionSub2_Group.setEnabled(False)
    
    def generateSessionName(self):
        # Session_(year)_(month)_(day)_(number of seconds)
        # Example: Session_2013_04_07_5432
        
        date = datetime.fromtimestamp(time()).strftime('%Y_%m_%d')
        seconds = str( (datetime.now() - datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).seconds )
        return "Session_" + date + "_" + seconds
    
    def getSession(self):
        if(self.Sessions_ComboBox.currentIndex() == 0):
            # Generate Session name for new session
            SessionName = self.generateSessionName()
        else:
            # Get session name from the ComboBox
            SessionName = self.Sessions_ComboBox.currentText()
        
        Session = {}
        Session["Name"]         = SessionName
        Session["Description"]  = self.Description_TextEdit.toPlainText()
        Session["SubElement"]   = {}
        
        Session["SubElement"]["TrainingClasses"]    = {}
        Session["SubElement"]["TrainingClasses"]["RIGHT"]           = str(self.Right_CheckBox.isChecked())
        Session["SubElement"]["TrainingClasses"]["LEFT"]            = str(self.Left_CheckBox.isChecked())
        Session["SubElement"]["TrainingClasses"]["FORWARD"]         = str(self.Forward_CheckBox.isChecked())
        Session["SubElement"]["TrainingClasses"]["BACK"]            = str(self.Back_CheckBox.isChecked())
        Session["SubElement"]["TrainingClasses"]["NEUTRAL"]         = str(self.Neutral_CheckBox.isChecked())
        
        Session["SubElement"]["TimingOptions"]      = {}
        Session["SubElement"]["TimingOptions"]["BlankTime"]         = self.BlankTime_LineEdit.text()
        Session["SubElement"]["TimingOptions"]["NumberOfTrials"]    = self.NumberOfTrials_LineEdit.text()
        Session["SubElement"]["TimingOptions"]["SteadyTime"]        = self.SteadyTime_LineEdit.text()
        Session["SubElement"]["TimingOptions"]["TrainingTime"]      = self.TrainingTime_LineEdit.text()
        
        if(self.Sessions_ComboBox.currentIndex() == 0):
            # Storing in the XML file if it's new and create a folder for it
            self.parser.addElement("TrainingSession", Session)
            os.mkdir(AppConfig.TrainingFolder + "/" + SessionName)
            
            # Adding new session to ComboBox and selecting it
            if(self.Sessions_ComboBox.currentIndex() == 0):
                self.Sessions_ComboBox.addItem( SessionName )
                self.TrainingSessions = self.parser.getElements('TrainingSession')
                self.Sessions_ComboBox.setCurrentIndex( self.Sessions_ComboBox.findText( SessionName ) )
            
        return Session
    
    def Str2Bool(self, opt):
        if(opt == "True"):
            return True
        else:
            return False
    
    
    def Sessions_ComboBox_CurrentIndexChanged(self):
        if(self.Sessions_ComboBox.currentIndex() == 0):
            # Enable GroupBoxes
            self.SessionSub1_Group.setEnabled(True)
            self.SessionSub2_Group.setEnabled(True)
            
            # Reset New-Session Inputs
            self.Description_TextEdit.setText("")
            self.IntializeTrainingOptions()
        else:
            # Disable GroupBoxes
            self.SessionSub1_Group.setEnabled(False)
            self.SessionSub2_Group.setEnabled(False)
            
            # Get the index
            idx = self.Sessions_ComboBox.currentIndex() - 1
            
            # Get TimingOptions from XML
            TimingOptions = self.TrainingSessions[idx].findall('TimingOptions')[0].attrib
            self.NumberOfTrials_LineEdit.setText(TimingOptions["NumberOfTrials"])
            self.BlankTime_LineEdit.setText(TimingOptions["BlankTime"])
            self.SteadyTime_LineEdit.setText(TimingOptions["SteadyTime"])
            self.TrainingTime_LineEdit.setText(TimingOptions["TrainingTime"])
            
            # Get TrainingClasses from XML
            TrainingClasses = self.TrainingSessions[idx].findall('TrainingClasses')[0].attrib
            self.Right_CheckBox.setChecked(self.Str2Bool( TrainingClasses["RIGHT"] ))
            self.Left_CheckBox.setChecked(self.Str2Bool( TrainingClasses["LEFT"] ))
            self.Forward_CheckBox.setChecked(self.Str2Bool( TrainingClasses["FORWARD"] ))
            self.Back_CheckBox.setChecked(self.Str2Bool( TrainingClasses["BACK"] ))
            self.Neutral_CheckBox.setChecked(self.Str2Bool( TrainingClasses["NEUTRAL"] ))
            
            # Get TrainingClasses from XML
            Description = self.TrainingSessions[idx].findall('Description')[0]
            if(Description.text):
                self.Description_TextEdit.setText( Description.text.strip() )
            else:
                self.Description_TextEdit.setText( "" )