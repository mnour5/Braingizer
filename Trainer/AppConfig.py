import os

#Training folder
DataFolder          = os.getcwd() + "/../Data"
TrainingFolder      = DataFolder + "/TrainingData"

#Profiles and Sessions Files
Profiles_File           = DataFolder + "/" + "_Profiles.xml"
TrainingSessions_File   = DataFolder + "/" + "_TrainingSessions.xml"

#Default Session's Options
Number_of_Trials    = 50
Blank_Time          = 2
Steady_Time         = 1
Training_Time       = 4
Train_Right         = True
Train_Left          = True
Train_Forward       = False
Train_Back          = False
Train_Neutral       = True

#The classes order in the training file
SortedClasses = ["RIGHT", "LEFT", "NEUTRAL", "FORWARD", "BACK"]

#Time to wait after recording the data
PostFinishTime      = 2

#Default Profile
Default_Profile     = ""            #Change to "Islam Maher" for example

#Default Session
Default_Session     = ""

#Print on the terminal
PrintDataStream         = True
PrintDataStream_Rate    = 100       #100 = update the screen every 0.1 sec

#Debug
DebugTrainingSession    = True