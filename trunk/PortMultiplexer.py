#!/usr/bin/python
from socket import *

class PM:
    def __init__(self):
        self.bufsize = 1024 # Modify to suit your needs
        self.targetHost = "localhost"
        self.listenPort = 8002
        self.forwardport = 100
        self.toPort = 0
        print 'Port Start',  self.toPort
        self.sendToPort = 0
        
    def forward(self,  data, port):
        print "Forwarding: '%s' from port %s" % (data, port)
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(("localhost", port)) # Bind to the port data came in on
        sock.sendto(data, (self.targetHost, self.sendToPort))
    
    def listen(self,  host, port):
        listenSocket = socket(AF_INET, SOCK_DGRAM)
        listenSocket.bind(('localhost', port))
        
        print listenSocket
        
        while True:
            
            self.toPort += 1
            if self.toPort >2:
                self.toPort = 1
            self.sendToPort = self.listenPort + (self.forwardport*self.toPort)
            print 'send Data to: ',  self.sendToPort
            data, addr = listenSocket.recvfrom(self.bufsize)
            print "data = ",  data,  addr
            self.forward(data, self.sendToPort)  # data and port


npm = PM()
npm.listen("localhost", 8002)

