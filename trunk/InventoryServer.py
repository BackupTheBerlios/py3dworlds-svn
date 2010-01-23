# coding=utf-8
from twisted.internet.task import deferLater
from twisted.web.resource import Resource
from databases.basics import basics
import databases.DB_Com
import uuid
#from xmlrpc.xmlrpc import myXmlRpc
from xmlrpc.gridxml import  gridxml
from twisted.internet import reactor
from misc.usefullThings import usefullThings

from twisted.internet.threads import deferToThread,  defer 
import time
from twisted.web.server import NOT_DONE_YET



class InventoryServer(Resource,  basics, gridxml,  usefullThings):
    _allowedMethods = ('GET','POST')
    allowedMethods = ('GET','POST')
    addSlash = True
    def __init__(self):
        #resource.__init__(self)
        Resource.__init__(self)

        self.isLeaf = True
        self.allowedMethods = ('GET','POST')
        self.addSlash = False

        basics.__init__(self)
        self.db_com = databases.DB_Com.DB_Com()
        #dicxml.__init__(self)
        usefullThings.__init__(self)

    
        
    def render_GET(self, request):
    
            
        return "<html>Hello, world!</html>"

    def render_POST (self,  request):
        print 'reached Post'
        
        sRequest = `request`
        headers =   request.received_headers
        liContent = request.content.readlines()
        args =  request.args
        
        print 'sRequest',  sRequest
        try:
            resp = None
            print 'licontent = ',  liContent
            sXml = liContent[0]
            print 'sxml = ',  sXml
            dicPost = self.xmltodict(sXml)
            print 'dicpost = ',  dicPost
            #defer.maybeDeferred(self.__add, data).addCallbacks(self.finishup,
             #                                 errback=self.error,
             #                                 callbackArgs=(request,))     
            if dicPost:
                if sRequest.find('GetInventory'):
                    
                    #return deferToThread(self.getInventory, dicPost) 
                    #d = deferLater(reactor, 5, lambda: request)
                    #d.addCallback(self.getInventory(dicPost,  request))
                    #return NOT_DONE_YET

                    request = self.getInventory(dicPost,  request) 
                    
            
        except Exception,  params :
            print Exception,  params
        return request
        
    def getInventory(self,   args,  request):
    
        request.responseHeaders.removeHeader ('content-type')
        request.responseHeaders.addRawHeader("Content-Type", "application/xml ")
        
        request.responseHeaders.addRawHeader("Keep-Alive", "timeout=30, max=400")
        request.responseHeaders.addRawHeader("Connection", "Keep-Alive ")
        
        #request.setResponseCode(200)
        print 'res.Headers = ',   request.responseHeaders

        #s1 = "<InventoryFolderBase>test </InventoryFolderBase>\n"
        #time.sleep(5)
        #return s1
        
        
        #print args
        sSql = "select * from inventoryfolders where agentid = '" + args['AvatarID'][0] + "'  and type = 8"
        resultRoot = self.db_com.xmlrpc_executeNormalQuery(sSql.encode())
        sSql = "select * from inventoryfolders where parentfolderid = '" + resultRoot[0]['folderid'] +"' "
        #sSql = "select * from inventoryfolders where agentid = '" + args['AvatarID'][0] + "' limit 5 "
        result = self.db_com.xmlrpc_executeNormalQuery(sSql.encode())
        #print len(result )
        sXml = self.dtd1 +"<Folders>\n"
        for row in resultRoot:
            sXml += "<InventoryFolderBase>\n"
            sXml += "<Name>"+ row['foldername'] + "</Name>\n"
            sXml += "<ID><Guid>" +  row['folderid'] + "</Guid></ID>\n"
            sXml += "<Owner><Guid>" + row['agentid'] +"</Guid></Owner>\n"
            sXml += "<ParentID><Guid>" +  row['parentfolderid'] + "</Guid></ParentID>\n"
            sXml += " <Type>" + `row['type']` + "</Type>\n"
            sXml += "<Version>" + `row['version']` + "</Version>\n"
            sXml += "</InventoryFolderBase>\n"
        
        for row in result:
            sXml += "<InventoryFolderBase>\n"
            sXml += "<Name>"+ row['foldername'] + "</Name>\n"
            sXml += "<ID><Guid>" +  row['folderid'] + "</Guid></ID>\n"
            sXml += "<Owner><Guid>" + row['agentid'] +"</Guid></Owner>\n"
            sXml += "<ParentID><Guid>" +  row['parentfolderid'] + "</Guid></ParentID>\n"
            sXml += " <Type>" + `row['type']` + "</Type>\n"
            sXml += "<Version>" + `row['version']` + "</Version>\n"
            sXml += "</InventoryFolderBase>\n"
        
        sXml += "</Folders>\n"
        sSql = "select * from inventoryitems where avatarid = '" + args['AvatarID'][0] + "' and parentfolderid = 'f92ddd25-a266-4034-863f-938f63183d17' "
        result = self.db_com.xmlrpc_executeNormalQuery(sSql.encode())

        sXml += "<Items>\n"
        for row in result:
            sXml += "<InventoryItemBase>\n"
            sXml += "<Name>" +row['inventoryname']  +"</Name>\n"
            sXml += "<ID><Guid>" +row['inventoryid'] +"</Guid></ID>\n"
            sXml += "<Owner><Guid>" +row['avatarid'] + "</Guid></Owner>\n"
            sXml += "<InvType>" + `row['invtype']` + "</InvType>\n"
            sXml += "<Folder><Guid>" +row['parentfolderid'] + "</Guid></Folder>\n"
            sXml += "<CreatorId>" + row['creatorid'] + "</CreatorId>\n"
            sXml += "<CreatorIdAsUuid><Guid>" + row['creatorid'] + "</Guid></CreatorIdAsUuid>\n"
            sXml += "<Description>" +  row['inventorydescription']  + "</Description>\n"
            sXml += "<NextPermissions>" + `row['inventorynextpermissions']` + "</NextPermissions>\n"
            sXml += "<CurrentPermissions>" + `row['inventorycurrentpermissions']`+ "</CurrentPermissions>\n"
            sXml += "<BasePermissions>" + `row['inventorybasepermissions']` + "</BasePermissions>\n"
            sXml += "<EveryOnePermissions>" +  `row['inventoryeveryonepermissions']`+ "</EveryOnePermissions>\n"
            sXml += "<GroupPermissions>" + `row['inventorygrouppermissions']`+ "</GroupPermissions>\n"
            sXml += "<AssetType>" + `row['assettype']` + "</AssetType>\n"
            sXml += "<AssetID><Guid>" + row['assetid']+ "</Guid></AssetID>\n"
            sXml += "<GroupID><Guid>" +row['groupid'] + "</Guid></GroupID>\n"
            sXml += "<GroupOwned>" +('false' if row['groupowned'] == 0 else 'true') + "</GroupOwned>\n"
            sXml += "<SalePrice>" +  `row['saleprice']`+ "</SalePrice>\n"
            sXml += "<SaleType>" +  `row['saletype']`+ "</SaleType>\n"
            sXml += "<Flags>" +  `row['flags']`+ "</Flags>\n"
            sXml += "<CreationDate>" + `row['creationdate']`+ "</CreationDate>\n"
            sXml += "</InventoryItemBase>\n"
        sXml += "</Items>\n"    
        
        # last add user to it <UserID><Guid>fb65174f-2dde-4c1e-ba13-1a776d6864fd</Guid  >
        sXml += "<UserID><Guid>" +args['AvatarID'][0] + "</Guid></UserID>\n"
        # close the xml root tag
        sXml += "</InventoryCollection>\n"
        sXml = sXml.replace('&', '&amp;')
#        sXml = sXml.replace('Ä', '&#196;')
#        sXml = sXml.replace('Ö', '&#214;')#        sXml = sXml.replace('Ä', '&#196;')
#        sXml = sXml.replace('Ö', '&#214;')
#        sXml = sXml.replace('Ü', '&#220;')
#        sXml = sXml.replace('ä', '&#228;')
#        sXml = sXml.replace('ö', '&#246;')
#        sXml = sXml.replace('ü', '&#252;')
#        sXml = sXml.replace('ß', '&#223;')

#        sXml = sXml.replace('Ü', '&#220;')
#        sXml = sXml.replace('ä', '&#228;')
#        sXml = sXml.replace('ö', '&#246;')
#        sXml = sXml.replace('ü', '&#252;')
#        sXml = sXml.replace('ß', '&#223;')
        sXml = sXml.replace('\'', '&apos;')
        
 
        #f= open('py3d.xml', 'wb')
        #f.write(sXml)
        #f.close()
        #print sXml
        #request.write(sXml)
        #request.finish()
        
        
        return  sXml
         
        


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
       #request.finish()
        #return  NOT_DONE_YET
#        return request

