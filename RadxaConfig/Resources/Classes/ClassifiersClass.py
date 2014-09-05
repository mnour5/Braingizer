import os
import AppConfig

class Classifiers(object):
    def getFunctionsPath(self):
        return AppConfig.ClassifiersFolder

    def getTrainFunction(self, ClassifierScript):
        return ClassifierScript + AppConfig.TrainSuffix

    def getDetectFunction(self, ClassifierScript):
        return ClassifierScript + AppConfig.DetectSuffix

    def getClassifiers(self):
        TSufx = AppConfig.TrainSuffix + ".m"
        DSufx = AppConfig.DetectSuffix + ".m"
        
        TrainList = []
        DetectList = []
        
        Classifiers = os.listdir(AppConfig.ClassifiersFolder)
        
        for c in Classifiers:
            if(c.endswith(TSufx)):
                TrainList.append(c[:-len(TSufx)])
            elif(c.endswith(DSufx)):
                DetectList.append(c[:-len(DSufx)])
        
        if(TrainList == DetectList):
            ClassifiersList = TrainList
            
        else:
            ClassifiersList = []
            
            for c in TrainList:
                if c in DetectList:
                    ClassifiersList.append(c)
        
        return ClassifiersList