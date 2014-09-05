import AppConfig
import paramiko
import os

class AppConfigFile():
    def __init__(self, Filename):
        self.Filename = Filename
    
    def editConfig(self, FindAttribute, Value, Tabs):
        CommnetAdded = False
        FindAttr    = FindAttribute + "="
        tmpfile     = self.Filename + "_tmp"
        
        with open(tmpfile, 'w') as outfile:
            with open(self.Filename, 'r') as infile:
                for line in infile:
                    line_tmp = line.replace(" ","")
                    
                    if(line_tmp.startswith(FindAttr)):
                        CommnetAdded = True
                        newline = FindAttribute + Tabs + "= " + Value + "\n"
                        outfile.write(newline)
                    else:
                        outfile.write(line)
        
        if(CommnetAdded):
            self.removeFile(self.Filename)
            self.renameFile(tmpfile, self.Filename)
        else:
            self.removeFile(tmpfile)
        
        return CommnetAdded
    
    def removeFile(self, filename):
        try:
            os.remove(filename)
        except:
            raise
    
    def renameFile(self, filename, newfilename):
        try:
            os.rename(filename, newfilename)
        except:
            raise

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

if __name__ == '__main__':
    radxa = RadxaInterface()
    radxa.connect()
    
    if(radxa.Connected):
        radxa.sendCommand('ls')
        #radxa.sendTrainingFile("Session_2014_07_05_58392/[T][2014-07-05 19-03-28] Walid Ezzat.csv")
        
        Classifier      = "LEASTSQUARES_nClasses"
        TrainingFile    = "Session_2014_07_05_58392/[T][2014-07-05 19-03-28] Walid Ezzat.csv"
        RecordingTime   = 2
        
        radxa.configRadxa(Classifier, TrainingFile, RecordingTime)
        radxa.disconnect()