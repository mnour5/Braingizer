import os
import AppConfig
from PyQt4 import QtCore, QtGui
from XmlParser_Class import XmlParser

class TrainingFileControl (QtCore.QObject):
    def __init__(self, MainWindow):
        QtCore.QObject.__init__(self)
        
        self.MW = MainWindow
        
        # Get stored Sessions and Profiles
        self.parser             = XmlParser()
        self.Profiles           = self.parser.getElements('Profile')
        self.TrainingSessions   = self.parser.getElements('TrainingSession')        
        
        # Populating Sessions_ComboBox with stored sessions
        for Session in self.TrainingSessions:
            self.MW.Sessions_ComboBox.addItem(Session.attrib['Name'])
        
        # Populating Profile_ComboBox with stored profiles
        for profile in self.Profiles:
            self.MW.Profile_ComboBox.addItem(profile.attrib['Name'])
        
        #EVENTS
        self.MW.Sessions_ComboBox.currentIndexChanged['QString'].connect(self.Sessions_ComboBox_CurrentIndexChanged)
        self.MW.Profile_ComboBox.currentIndexChanged['QString'].connect(self.Profile_ComboBox_CurrentIndexChanged)
        self.MW.TrainingFile_ComboBox.currentIndexChanged['QString'].connect(self.TrainingFile_ComboBox_CurrentIndexChanged)
        
        self.MW.Sessions_RadioButton.toggled.connect(self.Sessions_RadioButton_Clicked)
        self.MW.Profile_RadioButton.toggled.connect(self.Profile_RadioButton_Clicked)
    
    def setEnabled(self, opt):
        self.MW.TrainingFile_Group.setEnabled(opt)
        self.MW.Profile_RadioButton.setEnabled(opt)
        self.MW.Sessions_RadioButton.setEnabled(opt)
        
        if(self.MW.Profile_RadioButton.isChecked()):
            self.MW.Profile_ComboBox.setEnabled(opt)
        else:
            self.MW.Profile_ComboBox.setEnabled(False)
        
        if(self.MW.Sessions_RadioButton.isChecked()):
            self.MW.Sessions_ComboBox.setEnabled(opt)
        else:
            self.MW.Sessions_ComboBox.setEnabled(False)
    
    def Sessions_RadioButton_Clicked(self, enabled):
        self.MW.Sessions_ComboBox.setEnabled(enabled)
        
        if enabled:
            self.Sessions_ComboBox_CurrentIndexChanged()
    
    def Profile_RadioButton_Clicked(self, enabled):
        self.MW.Profile_ComboBox.setEnabled(enabled)
        
        if enabled:
            self.Profile_ComboBox_CurrentIndexChanged()
    
    def getTrainingFiles_Sessions(self, SessionName):
        # Initializing TrainingFiles
        TrainingFiles_Profile   = {}
        TrainingFiles_Path      = []
        
        # Get Session-Path
        SessionPath = AppConfig.TrainingFolder + "/" + SessionName
        
        # Get Training-files
        TrainingFiles_Name = os.listdir(SessionPath)
        TrainingFiles_Name.sort()
        
        for FileName in TrainingFiles_Name:
            FileShortPath = SessionName + "/" + FileName
            TrainingFiles_Path.append(FileShortPath)
        
        # Return TrainingFiles
        TrainingFiles_Profile['Path']   = TrainingFiles_Path
        TrainingFiles_Profile['Name']   = TrainingFiles_Name
        
        return TrainingFiles_Profile
    
    def getTrainingFiles_Profile(self, ProfileName):
        # Initializing TrainingFiles
        TrainingFiles_Profile   = {}
        TrainingFiles_Path      = []
        TrainingFiles_Name      = []
        
        # Get Training Sessions
        TrainingSessions = self.parser.getElements('TrainingSession')
        
        for Session in TrainingSessions:
            SessionName = Session.attrib['Name']
            SessionPath = AppConfig.TrainingFolder + "/" + SessionName
            
            # Get Training-files for this session
            TrainingFiles = os.listdir(SessionPath)
            
            # Find a Training-File with needed Profile-Name
            FindAttr    = "Name:"
            
            for FileName in TrainingFiles:
                FilePath = SessionPath + "/" + FileName
                
                with open(FilePath, 'r') as infile:
                    for line in infile:
                        if(line.startswith(FindAttr)):
                            FoundProfileName = line[len(FindAttr):].strip()
                            
                            if(FoundProfileName == ProfileName):
                                FileShortPath = SessionName + "/" + FileName
                                TrainingFiles_Path.append(FileShortPath)
        
        TrainingFiles_Path.sort()
        
        if(len(TrainingFiles_Path) != 0):
            TrainingFiles_Path.sort()
            
            for FilePath in TrainingFiles_Path:
                TrainingFiles_Name.append(FilePath.split("/")[-1])
        
        # Return TrainingFiles
        TrainingFiles_Profile['Path']   = TrainingFiles_Path
        TrainingFiles_Profile['Name']   = TrainingFiles_Name
        
        return TrainingFiles_Profile
    
    def TrainingFile_ComboBox_CurrentIndexChanged(self):
        Idx = self.MW.TrainingFile_ComboBox.currentIndex()
        print self.TrainingFiles['Path'][Idx]
    
    def Profile_ComboBox_CurrentIndexChanged(self):        
        ProfileName         = self.MW.Profile_ComboBox.currentText()
        self.TrainingFiles  = self.getTrainingFiles_Profile(ProfileName)
        TrainingFiles_Names = self.TrainingFiles['Name']
        
        if(len(self.TrainingFiles) != 0):
            self.MW.TrainingFile_ComboBox.clear()
            self.MW.TrainingFile_ComboBox.addItems(TrainingFiles_Names)
            self.CurrentProfileIdx = self.MW.Profile_ComboBox.currentIndex()
        else:
            self.MW.showMessageBox('Error', ProfileName + ' has no training files.')
            self.MW.Profile_ComboBox.setCurrentIndex(self.CurrentProfileIdx)
    
    def Sessions_ComboBox_CurrentIndexChanged(self):
        # Session-Name from ComboBox
        SessionName = self.MW.Sessions_ComboBox.currentText()
        self.TrainingFiles  = self.getTrainingFiles_Sessions(SessionName)
        TrainingFiles_Names = self.TrainingFiles['Name']
        
        if(len(self.TrainingFiles) != 0):
            self.MW.TrainingFile_ComboBox.clear()
            self.MW.TrainingFile_ComboBox.addItems(TrainingFiles_Names)
            self.CurrentSessionIdx = self.MW.Sessions_ComboBox.currentIndex()
        else:
            self.showMessageBox('Error', SessionName + ' has no training files.')
            self.MW.Sessions_ComboBox.setCurrentIndex(self.CurrentSessionIdx)