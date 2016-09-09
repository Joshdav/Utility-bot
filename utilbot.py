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

def exit(irc):
    irc.shutdown(socket.SHUT_RDWR)
    irc.close()
    quit()

if __name__ == '__main__':

	#Connecting to server and authenticating
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.settimeout(300)
    print ("Connecting to " + SERVER)
    irc.connect((SERVER, PORT))
    time.sleep(7)
    irc.send("NICK "+ NICK +"\n")
    irc.send("USER "+ UNAME +" 2 3 "+ REALNAME +"\n")

    #Entering main loop
    while True:
        data = irc.recv(4096)

        #Replies to the ping in order to not get a ping timeout
        if data[0:4] == "PING":
            irc.send ( "PONG " + data.split() [ 1 ] + "\r\n" )
            time.sleep(2)
            if not JOINED:
                irc.send("JOIN "+ CHANNEL +"\n")
                irc.send("PRIVMSG nickserv :identify %s\r\n" % PASSWORD)
                JOINED = True
        print (data)
        if data.find("!quit") != -1:
        	exit(irc)