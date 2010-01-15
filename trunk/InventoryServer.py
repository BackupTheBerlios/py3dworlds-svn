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

class InventoryServer(  Resource,  basics, gridxml,  usefullThings):
    isLeaf = True
    allowedMethods = ('GET','POST')
    
    
    def __init__(self):
        Resource.__init__(self)
        basics.__init__(self)
        self.db_com = databases.DB_Com.DB_Com()
        #dicxml.__init__(self)
        usefullThings.__init__(self)
        
        
    def render_GET(self, request):
        print request
        print request.postpath
        try:
            if request.postpath == (".html"):
                f = open(curdir + sep + self.path) #self.path has /test.html
                
                                     
        except IOError:
            (404,'File Not Found: %s' % request.postpath)
            
        return "<html>Hello, world!</html>"

    def render_POST(self,  request):
        sRequest = `request`
        headers =   request.received_headers
        liContent = request.content.readlines()
        args =  request.args
        
        try:
            print 'licontent = ',  liContent
            sXml = liContent[0]
            print 'sxml = ',  sXml
            dicPost = self.xmltodict(sXml)
            print 'dicpost = ',  dicPost
            
            if dicPost:
                if sRequest.find('GetInventory'):
                    return self.getInventory(dicPost) 
            
            print "try"
        except Exception,  params :
            print Exception,  params
        return 'NONE'
        
    def getInventory(self, args):
        sSql = "select * from inventoryfolders where agentid = '" + args['AvatarID'][0] + "'"
        result = self.db_com.xmlrpc_executeNormalQuery(sSql.encode())
        print len(result )
        #for row in result:
        #    dicXml = {}
            #dicXml[]
        
        return '<Hallo>'
