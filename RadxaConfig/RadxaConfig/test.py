import pxssh
import getpass
try:                                                            
    s = pxssh.pxssh()
    '''
    hostname = raw_input('hostname: ')
    username = raw_input('username: ')
    password = getpass.getpass('password: ')
    '''
    '''
    hostname = "192.168.2.4"
    username = "rock"
    password = "rock"
    '''
    
    hostname = "127.0.0.1"
    username = "medo"
    password = "aa"
    
    s.login (hostname, username, password)
    
    
    
    s.sendline ('uptime')   # run a command
    s.prompt()             # match the prompt
    print s.before          # print everything before the prompt.
    s.sendline ('ls -l')
    s.prompt()
    print s.before
    s.sendline ('df')
    s.prompt()
    print s.before
    s.logout()
except pxssh.ExceptionPxssh, e:
    print "pxssh failed on login."
    print str(e)