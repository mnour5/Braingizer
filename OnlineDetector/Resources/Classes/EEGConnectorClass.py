import Queue
import time
import datetime
from PyQt4 import QtCore, QtGui
from epoc import *
import AppConfig

class EEGConnector(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        
        self.fps = 128
        
        #Connect Flag
        self.connected = False
        
        #Data Thread
        self.DataThread = DataStreamingThread()
        QtCore.QObject.connect(self.DataThread, QtCore.SIGNAL('update(PyQt_PyObject)'), self.DataThread_Update)
        QtCore.QObject.connect(self.DataThread, QtCore.SIGNAL('finished()'), self.DataThread_Finished)
        QtCore.QObject.connect(self.DataThread, QtCore.SIGNAL('error()'), self.DataThread_Error)
        
        #Data Store Thread
        self.StoreThread    = DataStoreThread()
        self.SaveThread     = DataSaveThread()
        
        #Print Readings
        if(AppConfig.PrintDataStream):
            self.PrintTimer = QtCore.QTimer()
            self.PrintTimer.timeout.connect(self.PrintTimer_Timeout)
        
        #Reset Data Lists
        self.reset()

    def connect(self):
        try:
            self.eeg_headset = EPOC()
            data = self.eeg_headset.get_sample()
            self.connected = True
            self.reset()
            self.startStreamData()
            if(AppConfig.PrintDataStream):
                self.PrintTimer.start(AppConfig.PrintDataStream_Rate)
            return "Connected"
        
        except EPOCNotPluggedError, ete:
            return "Dongle is not found"
        
        except EPOCTurnedOffError, ete:
            self.eeg_headset.disconnect()
            return "Headset is not found"
        
        except EPOCError, ete:
            return "ERROR"

    def reset(self):
        self.DataQueue      = Queue.Queue()
        
        self.eeg_data               = {}
        self.eeg_quality            = {}
        self.eeg_counter            = []
        self.eeg_gyroX              = []
        self.eeg_gyroY              = []
        self.eeg_triggers           = []
        self.eeg_detectedDirections = []
        self.eeg_trueDirections     = []
        
        for channel in EPOC.channels:
            self.eeg_data[channel] = []
            self.eeg_quality[channel] = []

    def startStreamData(self):
        if(self.connected):
            self.CanDisconnect = False
            self.DataThread.startStreaming(self)
            self.StoreThread.startStoring(self)

    def stopStreamData(self):
        self.DataThread.stopStreaming()
        self.StoreThread.stopStoring()
        self.CanDisconnect = True

    def DataThread_Update(self, eeg_data):
        self.DataQueue.put(eeg_data)

    def DataThread_Finished(self):
        self.CanDisconnect = True

    def DataThread_Error(self):
        self.emit( QtCore.SIGNAL('error()') )

    def setDetectedDirection(self, detectedDirection, trueDirection, ClassesNames):
        detectedDir = 0
        trueDir     = 0
        
        for i, c in enumerate(ClassesNames):
            if(detectedDirection == c):
                detectedDir = i+1
            
            if(trueDirection == c):
                trueDir     = i+1
        
        self.eeg_detectedDirections.append(detectedDir)
        self.eeg_trueDirections.append(trueDir)

    def setTrigger(self):
        self.eeg_triggers.append(len(self.eeg_counter))

    def getLastTrial(self, RecordingTime):
        firstIDX    = self.eeg_triggers[-1]
        lastIDX     = self.eeg_triggers[-1] + self.fps * RecordingTime
        
        TrialData   = [[] for i in enumerate(EPOC.channels)]

        for i, channel in enumerate(EPOC.channels):
            TrialData[i] = self.eeg_data[channel][firstIDX:lastIDX]
        
        return TrialData

    def getLastData(self, RecordingTime):
        l = len(self.eeg_counter)
        
        if(l < self.fps * RecordingTime):
            return False
        
        firstIDX    = l - self.fps * RecordingTime
        lastIDX     = l
        
        TrialData   = [[] for i in enumerate(EPOC.channels)]

        for i, channel in enumerate(EPOC.channels):
            TrialData[i] = self.eeg_data[channel][firstIDX:lastIDX]
        
        return TrialData

    def saveToFile(self, SessionDetails):
        self.SaveThread.startSaving(self, SessionDetails)

    def PrintTimer_Timeout(self):
        if(self.connected):
            # Clear screen
            print("\x1b[2J\x1b[H")
            
            # Print Header
            header = "Emotiv Data Packet [%3d/128] [Loss: N/A] [Battery: %2d(%%)]" % (self.eeg_counter[-1], self.eeg_battery)
            print "%s\n%s" % (header, '-'*len(header))
            
            print "%10s: %5d" % ("Gyro(x)", self.eeg_gyroX[-1])
            print "%10s: %5d" % ("Gyro(y)", self.eeg_gyroY[-1])
            
            for i,channel in enumerate(self.eeg_headset.channel_mask):
                print "%10s: %5d %20s: %.2f" % (channel, self.eeg_data[channel][-1], "Quality", self.eeg_quality[channel][-1])

    def disconnect(self):
        if(not self.CanDisconnect):
            self.stopStreamData()
            
            while(not self.CanDisconnect):
                pass
        
        self.connected = False
        self.eeg_headset.disconnect()
        self.reset()
        if(AppConfig.PrintDataStream):
            self.PrintTimer.start(AppConfig.PrintDataStream_Rate)

class DataStreamingThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.enabled = False

    def __del__(self):
        self.wait()

    def startStreaming(self, EEG):
        self.eeg_headset = EEG.eeg_headset
        self.enabled = True
        self.start()

    def stopStreaming(self):
        self.enabled = False
        self.terminate()
        self.emit( QtCore.SIGNAL('finished()') )

    def run(self):
        try:
            while self.enabled:
                data = self.eeg_headset.get_sample()
                # data is [] for each battery packet, self.eeg_headset.g. ctr > 127
                if data:
                    eeg_data = [self.eeg_headset.counter, self.eeg_headset.battery, self.eeg_headset.gyroX, self.eeg_headset.gyroY, data, self.eeg_headset.quality]
                    
                    self.emit( QtCore.SIGNAL('update(PyQt_PyObject)'), eeg_data)
                    
                '''
                else:
                    print "We are faster than the 128 sampling frequency"
                '''
                    
        except EPOCError, ete:
            self.emit( QtCore.SIGNAL('error()') )

class DataStoreThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def startStoring(self, EEG):
        self.EEG = EEG
        self.start()

    def stopStoring(self):
        self.terminate()

    def run(self):
        while(True):
            if(not self.EEG.DataQueue.empty()):
                eeg_counter_new, self.EEG.eeg_battery, eeg_gyroX_new, eeg_gyroY_new, eeg_data_new, eeg_quality_new = self.EEG.DataQueue.get()
                
                for i, channel in enumerate(EPOC.channels):
                    self.EEG.eeg_data[channel].append(eeg_data_new[i])
                    self.EEG.eeg_quality[channel].append(eeg_quality_new[channel])
                
                self.EEG.eeg_counter.append(eeg_counter_new)
                self.EEG.eeg_gyroX.append(eeg_gyroX_new)
                self.EEG.eeg_gyroY.append(eeg_gyroY_new)

class DataSaveThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def startSaving(self, EEG, SessionDetails):
        self.EEG            = EEG
        self.SessionDetails = SessionDetails
        self.start()

    def run(self):
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')
        self.fileName = "[D][" + date + "] " + self.SessionDetails["Name"] + ".csv"
        self.filePath = AppConfig.DetectionFolder + "/" + self.fileName
        
        out = open(self.filePath, "w")
        
        
        out.write("=====================\n")
        out.write("  Detection Session  \n")
        out.write("=====================\n")
        out.write("Name:\t\t"       + self.SessionDetails["Name"] + '\n')
        out.write("Source:\t\t"     + str(self.SessionDetails["TrainingSource"]) + '\n')
        out.write("Date:\t\t"       + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') + '\n')
        out.write("Trials:\t\t"     + str(self.SessionDetails["NumberOfTrials"]) + '\n')
        out.write("PreTime:\t"      + str(self.SessionDetails["PreRecordingTime"]) + '\n')
        out.write("RecTime:\t"      + str(self.SessionDetails["RecordingTime"]) + '\n')
        out.write("PostTime:\t"     + str(self.SessionDetails["PostRecordingTime"]) + '\n')
        out.write("Classifier:\t"+ str(self.SessionDetails["Classifier"]) + '\n')
        out.write("AvgDetectTime:\t"+ str(self.SessionDetails["AvgDetectTime"]) + '\n')
        
        out.write("Triggers:\t")
        for i, t in enumerate(self.EEG.eeg_triggers):
            if i != 0:
                out.write(", ")
            out.write(str(t))
        out.write('\n')
        
        out.write("Directions:\t")
        for i, t in enumerate(self.EEG.eeg_detectedDirections):
            if i != 0:
                out.write(", ")
            out.write(str(t))
        out.write('\n')
        
        out.write("ClassesTypes:\t")
        for i, t in enumerate(self.EEG.eeg_trueDirections):
            if i != 0:
                out.write(", ")
            out.write(str(t))
        out.write('\n')
        
        out.write("ClassesNames:\t")
        for i, c in enumerate(self.SessionDetails["Classes"]):
            if i != 0:
                out.write(", ")
            out.write(c)
        out.write('\n')
        
        #Data
        out.write("\nRawData:\n")
        
        #HEADER
        out.write("Count")
        
        for channel in EPOC.channels:
            out.write(",\t" + channel)
        
        for channel in EPOC.channels:
            out.write(",\tQ_" + channel)
        
        out.write(",\tGyroX,\tGyroY\n")
        
        #VALUES
        for j in  xrange(len(self.EEG.eeg_counter)):
            #COUNTER
            out.write(str(self.EEG.eeg_counter[j]))
            
            #CHANNELS
            for i,channel in enumerate(EPOC.channels):
                out.write(",\t" + str(self.EEG.eeg_data[channel][j]))
            
            #QUALITY
            for i,channel in enumerate(EPOC.channels):
                out.write(",\t" + str("%.2f" % self.EEG.eeg_quality[channel][j]))
            
            #GYROs
            out.write(",\t" + str(self.EEG.eeg_gyroX[j]))
            out.write(",\t" + str(self.EEG.eeg_gyroY[j]))
            
            out.write('\n')
        
        out.close()
        self.emit( QtCore.SIGNAL('dataSaved(PyQt_PyObject)'), self.fileName)
        
        self.terminate()
