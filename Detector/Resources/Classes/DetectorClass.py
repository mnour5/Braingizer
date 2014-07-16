import os
import oct2py
from PyQt4 import QtCore, QtGui
import AppConfig

from ClassifiersClass import Classifiers

class Detector:
    def __init__(self, TrainingFile, ClassifierScript):
        self.DetectionStarted = False
        self.TrainingFile = TrainingFile
        self.ClassifierScript = ClassifierScript
        
        C = Classifiers()
        self.OctaveFunctionsPath    = C.getFunctionsPath()
        self.OctaveTrainFunction    = C.getTrainFunction(ClassifierScript)
        self.OctaveDetectFunction   = C.getDetectFunction(ClassifierScript)
        
        #Octave
        self.octave = oct2py.Oct2Py()
        self.octave.call('addpath', self.OctaveFunctionsPath)
        
        self.DetectThread = DetectDirectionThread(self.octave, self.OctaveDetectFunction)

    def startDetection(self):
        self.DetectionStarted = True
        self.TrainOut = self.octave.call(self.OctaveTrainFunction, AppConfig.TrainingFolder + "/" + self.TrainingFile)

    def detect(self, TrialData):
        DetectIn = oct2py.Struct()
        DetectIn['TrialData'] = TrialData
        DetectIn['TrainOut'] = self.TrainOut
        
        self.DetectThread.startDetect(DetectIn)
        
        #return self.octave.call(self.OctaveDetectFunction, DetectIn)

    def stopDetection(self):
        self.DetectionStarted = False
        self.octave.close()

class DetectDirectionThread(QtCore.QThread):
    def __init__(self, octave, OctaveDetectFunction):
        QtCore.QThread.__init__(self)
        self.octave = octave
        self.OctaveDetectFunction = OctaveDetectFunction

    def __del__(self):
        self.wait()

    def startDetect(self, DetectIn):
        self.DetectIn = DetectIn
        self.start()
    
    def stopDetect(self):
        self.terminate()

    def run(self):
        [DetectOut, Debug] = self.octave.call(self.OctaveDetectFunction, self.DetectIn)
        
        if(AppConfig.PrintClassifierDebug):
            print Debug
        
        self.emit( QtCore.SIGNAL('detected(PyQt_PyObject)'), DetectOut)