from bottle import route, run,  request,  response
from xmlrpc.gridxml import  gridxml
from databases.DB_Com import DB_Com
from databases.basics import basics

db_com = DB_Com()
basics = basics()

@route('/hello')
def hello():
    return "Hello World!"
    
@route('/GetFolderContent/', method='POST')
def getFolderContent():
      print "getFolderContent request = ",  `request`
      return 'NONE'
      
@route('/SystemFolders/', method='POST')
def getSystemfolders():
    print "getSystemFoldert request = ",  `request`
    return 'NONE'
      
@route('/GetInventory/', method='POST')
def getInventory():
    print "getInventory request = ",  `request`
    try:
         print '1',  request.method()
    except Exception,  param:
        print Exception,  param
        
            
    try:
         print '2',  request.input_length()
    except Exception,  param:
        print Exception,  param
        
    try:
         print '3',  request.GET()
    except Exception,  param:
        print Exception,  param
        
    try:
         print '4',  request.params()
    except Exception,  param:
        print Exception,  param
        
    print 'resonse = ',  response
    print 'response Header = ',  response.header_list
    print 'resp. headers = ',  response.wsgiheaders()
    if request:
        query = request.POST.get('<?xml version', '').strip()
       
    #query = request.POST
    if not query:
        return "You didn't supply a search query."
    else:
        print query
        query = '<?xml version' +"="+ query
        print "2 = ",  query
        
        args = gridxml().xmltodict(query)
        print args
        sSql = "select * from inventoryfolders where agentid = '" + args['AvatarID'][0] + "'  "
        result = db_com.xmlrpc_executeNormalQuery(sSql.encode())
        #print len(result )
        sXml = basics.dtd1 +"<Folders>"
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
        sSql = "select * from inventoryitems where avatarid = '" + args['AvatarID'][0] + "' limit 200"
        result = db_com.xmlrpc_executeNormalQuery(sSql.encode())

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
       
        return sXml
        #return


run(port=8004, host='py3d-worlds.org') # This starts the HTTP server
