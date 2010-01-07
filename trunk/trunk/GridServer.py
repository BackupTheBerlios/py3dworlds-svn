# coding=utf-8
from twisted.web import xmlrpc
from databases.basics import basics
import databases.DB_Com
import uuid
from xmlrpc.xmlrpc import myXmlRpc
from misc.usefullThings import usefullThings

class GridServer( xmlrpc.XMLRPC, basics, myXmlRpc,  usefullThings):
    def __init__(self):
        xmlrpc.XMLRPC.__init__(self)
        basics.__init__(self)
        self.db_com = databases.DB_Com.DB_Com()
        myXmlRpc.__init__(self)
        usefullThings.__init__(self)


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
        
        sSql = "select to_char(locx,'999999999') as x, to_char(locy,'999999999') as y , serverip as sim_ip, to_char(access,'99999999') as access ,1 as agents,  to_char( 9300,'999999') as http_port , "
        sSql += " to_char(regionhandle,'9999999999999999999') as regionhandle , uuid , serveruri as sim_uri, regionname as name, to_char(serverremotingport,'999999') as remoting_port, regionmaptexture as map_image_id "
        #sSql += " 512 as regions-flags "
        sSql += " from regions where locx between " + `args['xmin']` + " and " + `args['xmax']` + " and locy between " + `args['ymin']` + " and " + `args['ymax']`
        sim_profiles = []
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        for i in range(len(result)):
        #answer sim_profile...
            dicSim = result[i]
            dicSim['water_height'] = 0
            dicSim['regions-flags'] = 512
            dicSim['map-image-id'] = dicSim['map_image_id']
            dicSim = self.stripIt(dicSim)
            print "dicSim = ",  dicSim
            sim_profiles.append(dicSim)
            
        return sim_profiles
