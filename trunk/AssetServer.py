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
import base64


class AssetServer(Resource,  basics, gridxml,  usefullThings):
    isLeaf = True
    allowedMethods = ('GET','POST')
    
    def __init__(self):
        Resource.__init__(self)
        basics.__init__(self)
        self.db_com = databases.DB_Com.DB_Com()
        #dicxml.__init__(self)
        usefullThings.__init__(self)
        
        self.handler = {}
                
    def render_GET(self, request):
        print request
        print request.postpath
        #try:
        #    if request.postpath == (".html"):
        #        f = open(curdir + sep + self.path) #self.path has /test.html
        #                                             
        #except IOError:
        #    (404,'File Not Found: %s' % request.postpath)
        
        pp = request.postpath
        if pp[0] == 'assets':
            if pp[1]:
                self.getAsset(request,  pp[1])
        else:
            return "<html>Hello, world!</html>"
        
    def render_POST(self, request):
        return 'true'
        
    def getAsset(self,  request,  id):
        sSql = "SELECT data, name, assetType as type, local, temporary FROM assets WHERE id = '" + id + "'"
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        
        dic = {}
        if result and result not in self.liSQL_ERRORS :
            sXml = self.dtd2
            for row in result:
                sXml += "<Data>" +  base64.decodestring(row['data']) + "</Data>"
                sXml += "<FullID><Guid>" + id + "</Guid></FullID>"
                sXml += "<ID>" + id + "</ID>"
                sXml += "<Name>" +row['name'] + "</Name>"
                sXml += "<Description/>"
                sXml += "<Type>" + `row['type']` + "</Type>"
                sXml += "<Local>" + ('false' if row['local'] == 0 else 'true') + "</Local>"
                sXml += "<Temporary>" + ('false' if row['temporary'] == 0 else 'true')  + "</Temporary>"
                
            sXml += "</AssetBase>"
        else:
            sXml = self.dtd2 + "</AssetBase>"
                
#                dic['Data'] = row['data']
#                dic['FullID'] = {'Guid' : id}
#                dic['ID'] = id
#                dic['name'] = row['name']
#                #dic['Description'] = None tag must be <Description/>
#                dic['Type'] = row['type']
#                dic['Local'] = row['local']
#                dic['Temporary'] = row['temporary']
#            
#        doc = self.createDoc(sDTD= self.dtd1,None,  sRoot = 'AssetBase' )
#        sXml = self.dic2xml(doc, [dic])
#        print sXml
        
        return sXml
        
