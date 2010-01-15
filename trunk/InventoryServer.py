# coding=utf-8
from twisted.web import xmlrpc
from databases.basics import basics
import databases.DB_Com
import uuid
#from xmlrpc.xmlrpc import myXmlRpc
from xmlrpc import dicxml

from misc.usefullThings import usefullThings
from twisted.web.resource import Resource

class InventoryServer(  Resource,  basics, dicxml,  usefullThings):
    isLeaf = True
    allowedMethods = ('GET','POST')
    
    
    def __init__(self):
        Resource.__init__(self)
        basics.__init__(self)
        self.db_com = databases.DB_Com.DB_Com()
        dicxml.__init__(self)
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
        print ' HTTP Post reached',  request
        print request.received_headers
        print request.content.readlines()
        print request
        print request.args
        try:
            
            dicPost = self.parse_to_dic(request.args)
            print 'dicpost = ',  dicPost
            if dicPost:
                if request.find('GetInventory'):
                     return deferToThread(self.getInventory, dicPost)
            
            print "try"
        except :
            pass
            
    def getInventory(self, args):
        sSql = "select * from inventoryitems where agentid = '" + args['AvatarID'] + "'"
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        for row in result:
            pass
            
