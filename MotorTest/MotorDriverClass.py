import os
import serial
from serial.tools import list_ports
import time  
import AppConfig

class MotorDriver():
    def __init__(self):
        self.connnected = False
        self.TimeOut = 10

    def connect(self):
        while(not self.connnected):
            for port in self.getSerialPorts():
                try:
                    if(AppConfig.PrintMotorSearch):
                       print "Trying...",port
                    arduino = serial.Serial(port, 115200, timeout=0) #WE NEEEED A TIMEOUT
                    
                    for i in xrange(1, self.TimeOut):
                        time.sleep(1)
                        arduino.write('c') #C = Connect
                        time.sleep(0.01)
                        msg = arduino.readline()
                        print msg
                        
                        if "C" in msg:
                        #if(ch == 'C'):
                            if(AppConfig.PrintMotorState):
                                print "Motor: Connected"
                            
                            self.connnected = True
                            self.arduino = arduino
                            break
                except:
                    if(AppConfig.PrintMotorSearch):
                        print "Failed to connect on", port

    def goRight(self):
        self.send('d', 'D')
    
    def stop(self):
        self.send('s', 'S')

    def goLeft(self):
        self.send('a', 'A')
    
    def goForward(self):
        self.send('w', 'W')

    def send(self, direction, acknowledgment):
        arduino = self.arduino
        try:
            for i in xrange(1, self.TimeOut):
                arduino.write(direction)
                time.sleep(0.01)
                msg = arduino.readline()
                if acknowledgment in msg:
                #if(msg[0] == acknowledgment):
                    if(AppConfig.PrintMotorState):
                        print "Motor: ", acknowledgment
                    
                    break
            
        except:
            print "Failed to send!"
    
    def getSerialPorts(self):
        if os.name == 'nt':
            # windows
            for i in range(256):
                try:
                    s = serial.Serial(i)
                    s.close()
                    yield 'COM' + str(i + 1)
                except serial.SerialException:
                    pass
        else:
            # unix
            for port in list_ports.comports():
                yield port[0]


if __name__ == '__main__':
    motor = MotorDriver()
    motor.connect()
    '''
    for i in xrange(1, 10):
        motor.goRight()
        time.sleep(1)
        motor.goLeft()
        time.sleep(1)
        motor.goForward()
        time.sleep(1)
        motor.stop()
        time.sleep(1)
    '''
    motor.goForward()