# coding=utf-8
from twisted.web import xmlrpc
from databases.basics import basics
import databases.DB_Com
import uuid
#from xmlrpc.xmlrpc import myXmlRpc
from xmlrpc.gridxml import  gridxml

from misc.usefullThings import usefullThings
from twisted.web.resource import Resource
from twisted.internet.threads import deferToThread

class AssetServer(Resource,  basics, gridxml,  usefullThings):
    isLeaf = True
    allowedMethods = ('GET','POST')
    
    def __init__(self):
        Resource.__init__(self)
        basics.__init__(self)
        self.db_com = databases.DB_Com.DB_Com()
        #dicxml.__init__(self)
        usefullThings.__init__(self)
                
    def render_GET(self, request):
        sRequest = request
        print sRequest
        print request.postpath
        try:
            if request.postpath == (".html"):
                pass
                
        except IOError:
            (404,'File Not Found: %s' % request.postpath)
            
        sRet =  "<html>Hello, world!  request = " + `sRequest`
        sRet += " and postpath = " + `request.postpath`+ " </html>"

        return sRet
