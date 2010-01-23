# coding=utf-8
import bottle
from bottle import route, run,  request,  response
from xmlrpc.gridxml import  gridxml
from databases.DB_Com import DB_Com
from databases.basics import basics
import wsgiref 
from utils.Utils import Utils
db_com = DB_Com()
basics = basics()

#bottle.autojson = False

@route('/hello')
def hello():
    return "Hello World!"
    
       
@route('/NewItem/', method = 'POST') 
def newItem():
    return Utils().getXmlSchema('NewItem') +"<value>true</value> </NewItem>"
     
@route('/AddItem/', method = 'POST') 
def addItem():
    return Utils().getXmlSchema('AddItem') +"<value>true</value> </AddItem>"
 
       
    
@route('/GetFolderContent/', method='POST')
def getFolderContent():
      print "getFolderContent request = ",  `request`
      return Utils().getXmlSchema('GetFolderContent') +"<value>false</value> </GetFolderContent>"
      
@route('/SystemFolders/', method='POST')
def getSystemfolders():
    print "getSystemFoldert request = ",  `request`
    return Utils().getXmlSchema('SystemFolders') +"<value>false</value> </SystemFolders>"

@route('/QueryFolder/', method = 'POST') 
def queryFolder():
    return Utils().getXmlSchema('QueryFolder') +"<value>true</value> </QueryFolder>"
     
@route('/GetInventory/', method='POST')
def getInventory():
    print "getInventory request = ",  `request`
    
    env2  = request.environ['wsgi.input'].read(int(request.environ['CONTENT_LENGTH']))
    print 'env22 = ',  env2
  
    
    #response.content_type = 'application/xml; charset=utf-8'
    response.content_type = 'application/xml'
    #response.header['Connection'] = "Keep-Alive "
    #response.header['Keep-Alive'] = "timeout=30, max=400"
    
     
    #response.header_list.append( ("Keep-Alive", "timeout=30, max=400"))
    #response.header_list.append(("Connection", "Keep-Alive "))
    print 'resonse = ',  response
    print 'response Header = ',  response.header_list
    print 'resp. headers = ',  response.wsgiheaders()
           
    if not env2:
        return "You didn't supply a search query."
    else:
        args = gridxml().xmltodict(env2)
        print args
        sSql = "select * from inventoryfolders where agentid = '" + args['AvatarID'][0] + "'  and type = 8"
        resultRoot = db_com.xmlrpc_executeNormalQuery(sSql.encode())
        #sSql = "select * from inventoryfolders where parentfolderid = '" + resultRoot[0]['folderid'] +"' "
        sSql = "select * from inventoryfolders where agentid = '" + args['AvatarID'][0] + "'  and type != 8 order by type desc"
        result = db_com.xmlrpc_executeNormalQuery(sSql.encode())
        #print len(result )
        sXml = Utils().getXmlSchema('InventoryCollection') +"<Folders>\n"
        for row in resultRoot:
            sXml += "<InventoryFolderBase>\n"
            sXml += "<Name>"+Utils().normalizeXML(row['foldername'])+ "</Name>\n"
            sXml += "<ID><Guid>" +  row['folderid'] + "</Guid></ID>\n"
            sXml += "<Owner><Guid>" + row['agentid'] +"</Guid></Owner>\n"
            sXml += "<ParentID><Guid>" +  row['parentfolderid'] + "</Guid></ParentID>\n"
            sXml += " <Type>" + `row['type']` + "</Type>\n"
            sXml += "<Version>" + `row['version']` + "</Version>\n"
            sXml += "</InventoryFolderBase>\n"
        
        for row in result:
            sXml += "<InventoryFolderBase>\n"
            sXml += "<Name>"+Utils().normalizeXML(row['foldername']) + "</Name>\n"
            sXml += "<ID><Guid>" +  row['folderid'] + "</Guid></ID>\n"
            sXml += "<Owner><Guid>" + row['agentid'] +"</Guid></Owner>\n"
            sXml += "<ParentID><Guid>" +  row['parentfolderid'] + "</Guid></ParentID>\n"
            sXml += " <Type>" + `row['type']` + "</Type>\n"
            sXml += "<Version>" + `row['version']` + "</Version>\n"
            sXml += "</InventoryFolderBase>\n"
        
        sXml += "</Folders>\n"
        #sSql = "select * from inventoryitems where avatarid = '" + args['AvatarID'][0] + "' and parentfolderid = 'f92ddd25-a266-4034-863f-938f63183d17' "
        sSql = "select * from inventoryitems where avatarid = '" + args['AvatarID'][0] + "' "
        result = db_com.xmlrpc_executeNormalQuery(sSql.encode())

        sXml += "<Items>\n"
        for row in result:
            sXml += "<InventoryItemBase>\n"
            sXml += "<Name>" +Utils().normalizeXML(row['inventoryname'])  +"</Name>\n"
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
    
        
 
        #f= open('py3d.xml', 'wb')
        #f.write(sXml)
        #f.close()
        #print sXml
       
        return sXml
        
        #return

run(  port=8004, host='py3d-worlds.org') # This starts the HTTP server
