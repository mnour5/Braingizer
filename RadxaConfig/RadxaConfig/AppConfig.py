import os

# Trained-data
DataFolder          = os.getcwd() + "/../Data"
TrainingFolder      = DataFolder + "/TrainingData"

#Profiles and Sessions Files
Profiles_File           = DataFolder + "/" + "_Profiles.xml"
TrainingSessions_File   = DataFolder + "/" + "_TrainingSessions.xml"

# Radxa's credentials
IP_Radxa        = "192.168.2.4"
Username_Radxa  = "rock"
Password_Radxa  = "rock"

# Radxa's paths
BraingizerFolder_Radxa  = "/home/rock/Work/Braingizer"
TmpDataFolderName_Radxa = "TmpData"
TmpDataFolder_Radxa     = BraingizerFolder_Radxa + "/Data/TrainingData/" + TmpDataFolderName_Radxa

# Autorun
Autorun_Classifier          = "LEASTSQUARES_nClasses"
Autorun_RecordingTime       = 2

# Print on the terminal
PrintSSH        = True