# coding=utf-8
from twisted.web import xmlrpc
from databases.basics import basics
import databases.DB_Com
import uuid
from xmlrpc.xmlrpc import myXmlRpc

class GridServer( xmlrpc.XMLRPC, basics, myXmlRpc):
    def __init__(self):
        xmlrpc.XMLRPC.__init__(self)
        basics.__init__(self)
        self.db_com = databases.DB_Com.DB_Com()
        myXmlRpc.__init__(self)
        
    def xmlrpc_simulator_login(self,  args):
        print 'simulator_login ',  args
        # first: delete, then save the data in regions
        uuid = arg['uuid']
        sSql = "delete from regions where uuid = '"  + uuid  + "' "
        
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        
        sSql = " insert into regions ('uuid, serveruri,region_locx,region_locy, serverremotingport,recvkey, sendkey ')values("  
        sSql += uuid + ", " 
        sSql += args['server_uri'] + ", " 
        sSql += args['region_locx'] + ", " 
        sSql += args['region_locy'] + ", " 
        sSql += args['sim_ip'] + ", " 
        sSql += args['remoting_port'] + ", " 
        sSql += args['recvkey'] + ", " 
        sSql += args['sendkey'] + ", " 
        sSql += args['server_uri'] + ", " 


                                                     
        sSql += ") "
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        
        # now send the answer
        dicAnswer = {}
        dicAnswer['authkey'] = ''
        dicAnswer['neighbours'] =''
        dicAnswer['OpenSim.Data.RegionProfileData'] = ''
        
        
        return dicAnswer
        
        
    def xmlrpc_map_block(self,  args):
        print 'map block ',  args
        
        #answer sim_profile...
        
