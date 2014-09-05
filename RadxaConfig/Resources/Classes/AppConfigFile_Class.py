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
