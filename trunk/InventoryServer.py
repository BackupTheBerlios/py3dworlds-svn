# coding=utf-8
from twisted.web import xmlrpc
from databases.basics import basics
import databases.DB_Com
import uuid
#from xmlrpc.xmlrpc import myXmlRpc
from xmlrpc.gridxml import  gridxml

from misc.usefullThings import usefullThings
from twisted.web.resource import Resource
from twisted.internet.threads import deferToThread,  defer 
import time
from twisted.web.server import NOT_DONE_YET



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
        
        #print 'sRequest',  sRequest
        try:
            resp = None
            print 'licontent = ',  liContent
            sXml = liContent[0]
            #print 'sxml = ',  sXml
            dicPost = self.xmltodict(sXml)
            #print 'dicpost = ',  dicPost
            #defer.maybeDeferred(self.__add, data).addCallbacks(self.finishup,
             #                                 errback=self.error,
             #                                 callbackArgs=(request,))     
            if dicPost:
                if sRequest.find('GetInventory'):
                    #deferToThread(self.getInventory, dicPost,  request) 
                    #return deferToThread(self.getInventory, dicPost,  request)
                    return self.getInventory(dicPost,  request) 
            
            
        except Exception,  params :
            print Exception,  params
            
       
        return  NOT_DONE_YET
        #return
        # NO return 'NEVER REACHED'
        
    def getInventory(self, args,  request):
        sSql = "select * from inventoryfolders where agentid = '" + args['AvatarID'][0] + "' limit 3  "
        result = self.db_com.xmlrpc_executeNormalQuery(sSql.encode())
        #print len(result )
        sXml = self.dtd1 +"<Folders>"
        for row in result:
            sXml += "<InventoryFolderBase>"
            sXml += "<Name>"+ row['foldername'] + "</Name>"
            sXml += "<ID><Guid>" +  row['folderid'] + "</Guid></ID>"
            sXml += "<Owner><Guid>" + row['agentid'] +"</Guid></Owner>"
            sXml += "<ParentID><Guid>" +  row['parentfolderid'] + "</Guid></ParentID>"
            sXml += " <Type>" + `row['type']` + "</Type>"
            sXml += "<Version>" + `row['version']` + "</Version>"
            sXml += "</InventoryFolderBase>"
        
        sXml += "</Folders>"
        sSql = "select * from inventoryitems where avatarid = '" + args['AvatarID'][0] + "' limit 2"
        result = self.db_com.xmlrpc_executeNormalQuery(sSql.encode())

        sXml += "<Items>"
        for row in result:
            sXml += "<InventoryItemBase>"
            sXml += "<Name>" +row['inventoryname']  +"</Name>"
            sXml += "<ID><Guid>" +row['inventoryid'] +"</Guid></ID>"
            sXml += "<Owner><Guid>" +row['avatarid'] + "</Guid></Owner>"
            sXml += "<InvType>" + `row['invtype']` + "</InvType>"
            sXml += "<Folder><Guid>" +row['parentfolderid'] + "</Guid></Folder>"
            sXml += "<CreatorId>" + row['creatorid'] + "</CreatorId>"
            sXml += "<CreatorIdAsUuid><Guid>" + "</Guid></CreatorIdAsUuid>"
            sXml += "<Description>" +  row['inventorydescription']  + "</Description>"
            sXml += "<NextPermissions>" + `row['inventorynextpermissions']` + "</NextPermissions>"
            sXml += "<CurrentPermissions>" + `row['inventorycurrentpermissions']`+ "</CurrentPermissions>"
            sXml += "<BasePermissions>" + `row['inventorybasepermissions']` + "</BasePermissions>"
            sXml += "<EveryOnePermissions>" +  `row['inventoryeveryonepermissions']`+ "</EveryOnePermissions>"
            sXml += "<GroupPermissions>" + `row['inventorygrouppermissions']`+ "</GroupPermissions>"
            sXml += "<AssetType>" + `row['assettype']` + "</AssetType>"
            sXml += "<AssetID><Guid>" + row['assetid']+ "</Guid></AssetID>"
            sXml += "<GroupID><Guid>" +row['groupid'] + "</Guid></GroupID>"
            sXml += "<GroupOwned>" +('false' if row['groupowned'] == 0 else 'true') + "</GroupOwned>"
            sXml += "<SalePrice>" +  `row['saleprice']`+ "</SalePrice>"
            sXml += "<SaleType>" +  `row['saletype']`+ "</SaleType>"
            sXml += "<Flags>" +  `row['flags']`+ "</Flags>"
            sXml += "<CreationDate>" + `row['creationdate']`+ "</CreationDate>"
            sXml += "</InventoryItemBase>"
        sXml += "</Items>"    
        
        # last add user to it <UserID><Guid>fb65174f-2dde-4c1e-ba13-1a776d6864fd</Guid  >
        sXml += "<UserID><Guid>" +args['AvatarID'][0] + "</Guid></UserID>"
        # close the xml root tag
        sXml += "</InventoryCollection>"
        sXml = sXml.replace('&', '&amp;')

        #f= open('py3d.xml', 'wb')
        #f.write(sXml)
        #f.close()
        #print sXml
        print 'post finish'
        request.write(sXml)
        request.finish()
        print 'send all'
        return  NOT_DONE_YET
        #return






#        Folders =[]
#        for row in result:
#            #print 'row = ',   row
#            dicXml= {}
#            InventoryFolderBase = {}
#            dicXml['Name'] = row['foldername']
#            dicXml['ID'] = {'Guid': row['folderid']}
#            dicXml['Owner'] = {'Guid': row['agentid']}
#            dicXml['ParentID'] = {'Guid': row['parentfolderid']}
#            dicXml['Type'] = `row['type']`
#            dicXml['Version'] = `row['version']`
#            
#            InventoryFolderBase = {'InventoryFolderBase': dicXml}
#            Folders.append(InventoryFolderBase)
#            
#        sSql = "select * from inventoryitems where avatarid = '" + args['AvatarID'][0] + "' limit 20"
#        result = self.db_com.xmlrpc_executeNormalQuery(sSql.encode())
#        Items = []
#        for row in result:
#            #print 'row by items = ',  row
#            dicXml= {}
#            InventoryItemBase = {}
#            dicXml['Name'] = row['inventoryname'] +'-' + time.strftime('%d.%m.%Y %H:%M', time.gmtime(row['creationdate']))
#            dicXml['ID'] = {'Guid': row['inventoryid']}
#            dicXml['Owner'] = {'Guid': row['avatarid']}
#            dicXml['InvType'] = `row['invtype']`
#            dicXml['Folder'] = {'Guid': row['parentfolderid']}
#            dicXml['CreatorId'] =  row['creatorid']
#            dicXml['CreatorIdAsUuid'] = {'Guid': row['creatorid']}
#            dicXml['Description'] =  row['inventorydescription']            
#            dicXml['NextPermissions'] =  `row['inventorynextpermissions']`
#            dicXml['CurrentPermissions'] =  `row['inventorycurrentpermissions']`
#            dicXml['EveryOnePermissions'] =  `row['inventoryeveryonepermissions']`
#            dicXml['BasePermissions'] =  `row['inventorybasepermissions']`
#            dicXml['GroupPermissions'] =  `row['inventorygrouppermissions']`
#            dicXml['AssetType'] =  `row['assettype']`
#            dicXml['AssetID'] = {'Guid': row['assetid']}
#            dicXml['GroupID'] = {'Guid': row['groupid']}
#            if row['groupowned']  == 0:
#                dicXml['GroupOwned'] = 'false'
#            else:
#                dicXml['GroupOwned'] = 'true'
#                
#                
#            dicXml['SalePrice'] =  `row['saleprice']`
#            dicXml['SaleType'] =  `row['saletype']`
#            dicXml['Flags'] =  `row['flags']`
#            dicXml['CreationDate'] =  `row['creationdate']`
#
#            InventoryItemBase = {'InventoryItemBase': dicXml}
#            Items.append(InventoryItemBase)
#            
#        doc1 = self.createDoc(sDTD= self.dtd1, sDTD2 = self.dtd1_2,   sRoot = 'InventoryCollection' )
#        #print '1',   self.getDoc2String(doc1)
#        
#        doc1 = self.addElement(doc1, 'Folders')
#        #print'2',   self.getDoc2String(doc1)
#        
#        doc1 = self.dic2xml(doc1, Folders,  'Folders')
#        
#        #doc2 = self.createDoc(sDTD= self.dtd1, sDTD2 = self.dtd1_2,   sRoot = 'items' )
#        #doc2 =  self.dic2xml(doc2, Items)
#        doc1 = self.addElement(doc1, 'Items')
#        doc1 = self.dic2xml(doc1, Items,  'Items')
#        # last add user to it <UserID><Guid>fb65174f-2dde-4c1e-ba13-1a776d6864fd</Guid  >
#        
#        doc1 = self.addElement(doc1, 'UserID')
#        doc1 = self.dic2xml(doc1, [{'Guid':args['AvatarID'][0] }],  'UserID')
#        sXml = self.getDoc2String(doc1) #+ self.getDoc2String(doc2) 
#        #print sXml
#        
#        request.write(sXml)
#        request.finish()
#        return  NOT_DONE_YET
