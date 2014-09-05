import pxssh
import getpass
import AppConfig
from PyQt4 import QtCore, QtGui

#class RadxaSession(QtCore.QObject):
class RadxaSession():
    def __init__(self):
        self.Connected = False
    
    def connect(self):
        try:
            self.s = pxssh.pxssh()
            self.s.login (AppConfig.IP_Radxa, AppConfig.Username_Radxa, AppConfig.Password_Radxa)
            self.Connected = True
        except pxssh.ExceptionPxssh, e:
            print "Radxa Error: Failed to connect."
            print str(e)
    
    def sendCommand(self, Command):
        if(self.Connected):
            try:
                # Run the command
                self.s.sendline (Command)
                
                # Match the prompt
                self.s.prompt()
                
                # Print everything before the prompt.
                if(AppConfig.PrintSSH):
                    print "Radxa:\n", self.s.before
                
            except pxssh.ExceptionPxssh, e:
                print "Radxa Error: Failed to send command:'", Command, "'."
                print str(e)
        else:
            print "Radxa Error: Radxa is not connected, failed to send command:'", Command, "'."
    
    def disconnect(self):
        if(self.Connected):
            try:
                self.s.logout()
                self.Connected = False
            except pxssh.ExceptionPxssh, e:
                print "Radxa Error: Failed to disconnect."
                print str(e)
        else:
            print "Radxa Error: Radxa is not connected, failed to disconnect."

def SendFile(SourceFile, Destination):
    CommnetAdded = False

def AddComments(Filename, Comments):
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

if __name__ == '__main__':
    radxa = RadxaSession()
    radxa.connect()
    if(radxa.Connected):
        #radxa.sendCommand('ls')
        radxa.sendFile()