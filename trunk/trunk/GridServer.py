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
        uuid = args['originUUID']
        sSql = "delete from regions where uuid = '"  + uuid  + "' "
        
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        
        sSql = " insert into regions (uuid, serveruri,locx,locy, serverip, serverremotingport,regionrecvkey, regionsendkey )values("  
        sSql += "'" + uuid + "', " 
        sSql += "'" + args['server_uri'] + "', " 
        sSql += args['region_locx'] + ", " 
        sSql += args['region_locy'] + ", " 
        sSql += "'" + args['sim_ip'] + "', " 
        sSql += args['remoting_port'] + ", " 
        sSql += args['recvkey']  + ", "
        # to do, set the correct key for sendkey
        sSql += args['recvkey']  

        


                                                     
        sSql += ") "
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        print result
        # now send the answer
        dicAnswer = {}
        dicAnswer['authkey'] = ''
        dicAnswer['neighbours'] =''
        dicAnswer['OpenSim.Data.RegionProfileData'] = ''
        
        
        return dicAnswer
        
        
    def xmlrpc_map_block(self,  args):
        print 'map block ',  args
        # seems tobe cleared , more regions ?
        
        sSql = "select * from regions where locx between " + `args['xmin']` + " and " + `args['xmax']` + " and locy between " + `args['ymin']` + " and " + `args['ymax']`
        
        dicSim = self.db_com.xmlrpc_executeNormalQuery(sSql)[0]
        #answer sim_profile...
        dicSim['sim-profiles'] = []
        
        return dicSim
