import os
from PyQt4 import QtCore, QtGui

class TrainingFileCreator(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
    
    def AddComments(self, Filename, Comments):
        CommnetAdded = False
        
        FindAttr    = "Date:"
        tmpfile     = Filename + "_tmp"
        
        with open(tmpfile, 'w') as outfile:
            with open(Filename, 'r') as infile:
                for line in infile:
                    if(line.startswith(FindAttr)):
                        CommnetAdded = True
                        outfile.write(line)
                        newline = "Comments:\t" + Comments.replace("\n","\t") + "\n"
                        outfile.write(newline)
                    else:
                        outfile.write(line)
        
        if(CommnetAdded):
            self.removeFile(Filename)
            self.renameFile(tmpfile, Filename)
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
    