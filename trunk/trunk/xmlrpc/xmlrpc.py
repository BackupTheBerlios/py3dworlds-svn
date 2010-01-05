# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


#import xmlrpclib
#from xmlrpclib import Server
from databases.dumps import dumps
#from M2Crypto.m2xmlrpclib import  Server, SSL_Transport

import time
from xmlrpclib import ServerProxy
#import bzip2

class myXmlRpc(dumps):
    """
    @author: Jürgen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Löhne
    @copyright: by Jürgen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """
    def __init__(self):
        dumps.__init__(self)
        
        #self.zope_server = self.getZopeServer()
        #self.MyServer = self.getMyServer()
        self.server = 'http://localhost:9000'
        
    def getMyServer(self):
        """
        if the CUON_SERVER environment-variable begins with https,
        then the server use SSL for security.
        @return: Server-Object for xmlrpc
        """
        
        sv = None
        try:
#            if self.td.server[0:5] == 'https':
#                #print "------ HTTPS ------", self.td.server
#                #sv =  Server( self.td.server  , SSL_Transport(), encoding='utf-8')
#                sv =  ServerProxy( self.td.server, allow_none = 1) 
#            else:
#                #print 'Server2 = ', self.td.server
#                #sv =  ServerProxy( self.td.server, allow_none = 1 )
            sv = ServerProxy(self.server,allow_none = 1)
                
        except Exception, params:
            print 'Server error by xmlrpc : ', self.td.server
            print Exception
            print params
            
        
        return sv
    
  

    def getServer(self):
        #return self.MyServer
        return ServerProxy(self.server,allow_none = 1)
        
    def getServer2(self):
        return self.MyServer
        
    def getHelpServer(self):
        return self.MyHelpServer
        


    def getInfoOfTable(self, sNameOfTable):
        return self.getServer().src.Databases.py_getTable(sNameOfTable)
    

    def callRP(self, rp, *c):
        #t1 = time.mktime(time.localtime()) 
        #print  '<-------xmlrpc start : ' + ` t1` 
        r = None
        #print 'rp',rp
        #print rp[0:3]
        print 'server = ',  self.getServer() 
        s = 'r = self.getServer().' + rp + '('
        for i in c:
            s = s + `i` + ', '
            #print '-------------------------------------------------'
            #print 'i = ', `i`
            #print '-------------------------------------------------'
            
        if len(c) > 0:
            s = s[0:len(s) -2]
        s = s + ')'
        print s
        #self.out(s)
        startRP = True
        rp_tries = 0
        #print 'Server by connection: ', self.getServer()
        #print 'Servercall by Connection: ', s
        #s = bz2.compress(s)
        #s = base64.encodestring(s)
        while startRP:
            try:
                exec s
                
                startRP = False

            except IOError, param:
                print 'IO-Error'
                print param
                
            except KeyError, param:
                print 'KEY-Error'
                print param

            except Exception, param:
                print 'unknown exception'
                print `Exception`
                print param[0:200]
                
            if startRP:
                print 'error, next try'
                
                rp_tries = rp_tries + 1
                
                if rp_tries > 5:
                    startRP = False
                else:
                    print ' wait for 2 sec. '
                    print ' Try :' + `rp_tries`
                    time.sleep(1)
        if r and r == 'NONE':
            r = None
        #print  '<-------xmlrpc need: ' + ` time.mktime(time.localtime()) -t1` 
        return    r

    
        
        
        


