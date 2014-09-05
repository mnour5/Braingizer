import os

# Trained-data, Detected-data and Octave-classifiers folders
DataFolder          = os.getcwd() + "/../Data"
TrainingFolder      = DataFolder + "/TrainingData"
DetectionFolder     = DataFolder + "/DetectionData"
ClassifiersFolder   = os.getcwd() + "/Classifiers"

#Profiles and Sessions Files
Profiles_File           = DataFolder + "/" + "_Profiles.xml"
TrainingSessions_File   = DataFolder + "/" + "_TrainingSessions.xml"

# Octave functions suffix
TrainSuffix         = "_Train"
DetectSuffix        = "_Detect"

# Autorun
Autorun                     = True
Autorun_Classifier          = "LEASTSQUARES_nClasses"
Autorun_TrainingFile        = "TmpData/[T][2014-07-05 19-03-28] Walid Ezzat.csv"
#Autorun_TrainingFile        = "Session_2014_06_27_73509/[T][2014-06-27 20-33-14] Ahmed Hemaly.csv"
Autorun_nTrials             = 20
Autorun_BlankTime           = 1
Autorun_SteadyTime          = 1
Autorun_RecordingTime       = 2
Autorun_PostRecordingTime   = 1

#The classes order in the training file
SortedClasses = ["RIGHT", "LEFT", "NEUTRAL", "FORWARD", "BACK"]

# Enable Motorst
EnableMotors            = True
MotorStopDelay          = 1

# Print on the terminal
PrintSessionDetails     = False     #Enable for RPi, to see the output on the shell
PrintDataStream         = False
PrintDataStream_Rate    = 100       #100 = update the screen every 0.1 sec
PrintMotorState         = True      #Enable to see motor state (Connected, Left, Right ...etc.)
PrintMotorSearch        = True      #Enable to see if the app is searching for the motor
PrintClassifierDebug    = False     #Enable to see the debug output of the detection octave script

# Debug
Debug = False
