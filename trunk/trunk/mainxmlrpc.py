#! /usr/bin/python
#xmlrpc-server

from twisted.web import xmlrpc, resource, static
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
from databases.basics import basics
import UserServer
import GridServer
import AssetServer
import InventoryServer
import databases.DB_Com
import databases.Funcs

openssl = False
try:
    from OpenSSL import SSL
    openssl = True

except:
    pass
    

import locale, gettext

class ServerContextFactory:

    def getContext(self):
        """Create an SSL context.

        Similar to twisted's echoserv_ssl example, except the private key
        and certificate are in separate files."""
        ctx = None
        try:
            ctx = SSL.Context(SSL.SSLv23_METHOD)
            ctx.use_privatekey_file('etc/pylife/serverkey.pem')
            ctx.use_certificate_file('etc/pylife/servercert.pem')
        except:
            ctx = None
        return ctx

    def render_GET(self, request):
        print request

class ServerData(xmlrpc.XMLRPC):
    def __init__(self):
        pass
        
    def getUserSite(self):
        r = UserServer.UserServer()
         
        #r.putSubHandler('Tweet', oTweet)
        return r 
    def getGridSite(self):   
        r = GridServer.GridServer()
        return r
        
    def getAssetSite(self):   
        r = AssetServer.AssetServer()
        return r   
        
    def getInventorySite(self):   
        r = InventoryServer.InventoryServer()
        return r
        
    def getDB_ComSite(self):
        r = databases.Funcs.Funcs()
        r.putSubHandler('Database', databases.DB_Com.DB_Com() )
        return r
    
        
    def MyFunc(self):
        print 'test'
    
