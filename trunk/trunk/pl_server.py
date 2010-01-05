#! /usr/bin/python
#xmlrpc-server

from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
import mainxmlrpc    
import databases.basics
import sys

baseSettings = databases.basics.basics()

openssl = False
try:
    from OpenSSL import SSL
    openssl = True

except:
    pass
    
print 'Openssl = ', openssl
import locale, gettext
m = mainxmlrpc.ServerData()
u = m.getUserSite()
g = m.getGridSite()

try:    
    port = int(sys.argv[1])
except:
    port = 0
print port

reactor.listenTCP(baseSettings.USER_PORT + port, server.Site(u))

reactor.listenTCP(baseSettings.GRID_PORT + port, server.Site(g))

if openssl:
    """Create an SSL context."""
    
    try:
        reactor.listenSSL(baseSettings.USER_PORT + baseSettings.SSL_OFFSET + port,  server.Site(u), mainxmlrpc.ServerContextFactory())
        print 'HTTPS activated'
    except:
        print 'Error by activating HTTPS. Please check /etc/cuon/serverkey.pem and /etc/cuon/servercert.pem.'

reactor.run()
