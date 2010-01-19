# coding=utf-8
import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import MySQLdb
import uuid
import md5
from xmlrpc.gridxml import  gridxml
from databases.basics import basics
import databases.DB_Com
#from xmlrpc.xmlrpc import myXmlRpc
from xmlrpc.gridxml import  gridxml

from misc.usefullThings import usefullThings
import time
import sys
from wsgiref.handlers import SimpleHandler



class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print self.path
        try:
            if self.path.endswith(".html"):
                pass
        except:
            pass
            
    def do_POST(self):
        print 'start Post'
        print ' Header = ',  self.headers
        clen = self.headers.getheader('content-length')
        if clen:
            clen = int(clen)
        else:
            print 'POST ERROR: missing content-length'
            return
        input_body = self.rfile.read(clen)
        print 'input = ',  input_body
        print self.command
        print self.path
        print 'input-ready'
        
        
        self.send_response(200,  self.request_version)
        #self.send_header('Expect' ,  '100-continue')
        self.send_header("Keep-Alive", "timeout=30, max=400")
        self.send_header("Connection", "Keep-Alive ")
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        
        if self.command == 'POST' and self.path == '/GetInventory':
            answer = doPostEvents().getInventory(input_body) 
            print 'post finish'
        
            self.wfile.write(answer)
            self.wfile.close()
     
        return
 

class doPostEvents(basics, gridxml,  usefullThings):
    def __init__(self):
        basics.__init__(self)
        self.db_com = databases.DB_Com.DB_Com()
        #dicxml.__init__(self)
        usefullThings.__init__(self)
        
    def getInventory(self, postData):
        args = self.xmltodict(postData)
        print args
        sSql = "select * from inventoryfolders where agentid = '" + args['AvatarID'][0] + "'  "
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
        sSql = "select * from inventoryitems where avatarid = '" + args['AvatarID'][0] + "' limit 200"
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
       
        return sXml
        #return


class InventoryServer2:
        
    def startServer(self):
        
        server = HTTPServer(('', 8004), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
        
    
    
