import socket
import sys
import time
import ssl
import re

#initial setup
SERVER = "irc.synirc.net"
PORT = 6667
CHANNEL = "#aeleven"
UNAME = "botname"
REALNAME = "realname"
NICK = "utilbot"
PASSWORD = "testing"
JOINED = False

highf = []

def exit(irc):
    irc.shutdown(socket.SHUT_RDWR)
    irc.close()
    quit()

def highfive(direction, irc):
    if direction == "o/":
        if len(highf) != 0:
            if highf[len(highf)-1] == "\o":
                irc.send("PRIVMSG " + CHANNEL + " :o/\o\n")
                highf.pop()
            else:
                highf.append("o/")
        else:
            highf.append("o/")
    if direction == "\o":
        if len(highf) != 0:
            if highf[len(highf)-1] == "o/":
                irc.send("PRIVMSG " + CHANNEL + " :o/\o\n")
                highf.pop()
            else:
                highf.append("\o")
        else:
            highf.append("\o")

def connection():
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.settimeout(300)
    print ("Connecting to " + SERVER)
    irc.connect((SERVER, PORT))
    time.sleep(7)
    irc.send("NICK "+ NICK +"\n")
    irc.send("USER "+ UNAME +" 2 3 "+ REALNAME +"\n")
    return irc

def pong(irc, JOINED):
    irc.send ( "PONG " + data.split() [ 1 ] + "\r\n" )
    time.sleep(2)
    if not JOINED:
        irc.send("JOIN "+ CHANNEL +"\n")
        irc.send("PRIVMSG nickserv :identify %s\r\n" % PASSWORD)
        JOINED = True

if __name__ == '__main__':

	#Connecting to server and authenticating
    irc = connection()

    #Entering main loop
    while True:
        data = irc.recv(4096)
        print (data)

        #Replies to the ping in order to not get a ping timeout
        if data[0:4] == "PING":
            pong(irc, JOINED)
        
        #Quit function -- only to be used in testing
        if data.find("&quit") != -1:
        	exit(irc)

        #High five function
        if data.find("o/") != -1:
            highfive("o/", irc)
        if data.find("\o") != -1:
            highfive("\o", irc)
