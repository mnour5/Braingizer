import AppConfig
import paramiko
import os

from AppConfigFile_Class import AppConfigFile

class RadxaInterface():
    def __init__(self):
        self.Client     = None
        self.Connected  = False
        self.HasError   = False
        
    def connect(self):
        try:
            if(AppConfig.PrintSSH):
                print "Radxa: Connecting..."
            
            self.Client = paramiko.SSHClient()
            self.Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.Client.connect(AppConfig.IP_Radxa, username=AppConfig.Username_Radxa, password=AppConfig.Password_Radxa)
            self.Connected = True
            self.HasError = False
            
        except:
            print "Radxa Error: Failed to connect, check your connection and try again."
            raise
    
    def configRadxa(self, Classifier, TrainingFile, RecordingTime):
        self.sendTrainingFile(TrainingFile)
        
        TrainingFile_Radxa = AppConfig.TmpDataFolderName_Radxa + "/" + TrainingFile.split("/")[-1]
        
        self.editAppConfigFile(Classifier, TrainingFile_Radxa, RecordingTime)
    
    def sendTrainingFile(self, TrainingFilePath):
        if(AppConfig.PrintSSH):
            print "Radxa: Sending Training-File: ", TrainingFilePath
        
        SourceFile = AppConfig.TrainingFolder + "/" + TrainingFilePath
        Destination = AppConfig.TmpDataFolder_Radxa + "/" + TrainingFilePath.split("/")[-1]
        
        self.sendFile(SourceFile, Destination)
    
    def editAppConfigFile(self, Classifier, TrainingFile, RecordingTime):
        # Get the AppConfing file from Radxa
        RemoteFile  = AppConfig.BraingizerFolder_Radxa + "/OnlineDetector/AppConfig.py"
        AppConfig_Temp = "AppConfig_Temp.py"
        self.getFile(RemoteFile, AppConfig_Temp)
        
        
        # Prepairing the configs
        Autorun_Classifier = "\"" + Classifier + "\""
        Autorun_TrainingFile = "\"" + TrainingFile + "\""
        Autorun_RecordingTime = str(RecordingTime)
        
        # Edit the AppConfing file
        ConfigFile = AppConfigFile(AppConfig_Temp)
        ConfigFile.editConfig("Autorun",                "True",                 "                     ")
        ConfigFile.editConfig("Autorun_Classifier",     Autorun_Classifier,     "          ")
        ConfigFile.editConfig("Autorun_TrainingFile",   Autorun_TrainingFile,   "        ")
        ConfigFile.editConfig("Autorun_RecordingTime",  Autorun_RecordingTime,  "       ")
        
        # Send the AppConfing file back to Radxa
        self.sendFile(AppConfig_Temp, RemoteFile)
    
    def sendFile(self, SourceFile, Destination):
        sftp = self.Client.open_sftp()
        sftp.put(SourceFile, Destination)
    
    def getFile(self, RemoteFile, Destination):
        sftp = self.Client.open_sftp()
        sftp.get(RemoteFile, Destination)
    
    def sendCommand(self, Command):
        if(self.Connected):
            try:
                if(AppConfig.PrintSSH):
                    print "Radxa: ", Command
                
                stdin,stdout,stderr = self.Client.exec_command(Command)
                
                stdin.close()
                
                error = str(stderr.read())
                
                if error:
                    self.HasError = True
                    print "Radxa Error: Failed to send command: ", Command
                    print "Radxa Error: ", error
                else:
                    result = str(stdout.read())
                    print "Radxa: ", result
                
            except:
                self.HasError = True
                print "Radxa Error: Failed to send command: ", Command
                raise
        else:
            self.HasError = True
            print "Radxa Error: Radxa is not connected, failed to send command: ", Command
    
    def reboot(self):
        if(self.Connected):
            try:
                self.sendCommand("sudo reboot")
            
            except:
                print "Radxa Error: Failed to reboot."
                raise
        else:
            print "Radxa Error: Radxa is not connected, failed to reboot."
    
    def shutdown(self):
        if(self.Connected):
            try:
                self.sendCommand("sudo shutdown now")
            
            except:
                print "Radxa Error: Failed to shutdown."
                raise
        else:
            print "Radxa Error: Radxa is not connected, failed to shutdown."
    
    def disconnect(self):
        if(self.Connected):
            try:
                self.Client.close()
                self.Connected = False
                
                if(AppConfig.PrintSSH):
                    print "Radxa: Disconnected."
            except:
                print "Radxa Error: Failed to disconnect."
                raise
        else:
            print "Radxa Error: Radxa is not connected, failed to disconnect."