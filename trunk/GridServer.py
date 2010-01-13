# coding=utf-8
from twisted.web import xmlrpc
from databases.basics import basics
import databases.DB_Com
import uuid
from xmlrpc.xmlrpc import myXmlRpc
from misc.usefullThings import usefullThings
from regions.Region import Region



class GridServer( xmlrpc.XMLRPC, basics, myXmlRpc,  usefullThings,  Region):
    def __init__(self):
        xmlrpc.XMLRPC.__init__(self)
        basics.__init__(self)
        Region.__init__(self)
        
        self.db_com = databases.DB_Com.DB_Com()
        myXmlRpc.__init__(self)
        usefullThings.__init__(self)
        
        

    def xmlrpc_simulator_login(self,  args):
        print 'simulator_login ',  args
        # first: delete, then save the data in regions
        uuid = args['UUID']
        sSql = "delete from regions where uuid = '"  + uuid  + "' "
        
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        
        sSql = "insert into regions (uuid, serveruri,locx,locy, serverip, serverremotingport,regionrecvkey, regionsendkey , owner_uuid, " 
        sSql += "serverHttpPort, regionSecret, regionName, regionHandle)values("  
        sSql += "'" + uuid + "', " 
        sSql += "'" + args['server_uri'] + "', " 
        sSql += args['region_locx'] + ", " 
        sSql += args['region_locy'] + ", " 
        sSql += "'" + args['sim_ip'] + "', " 
        sSql += args['remoting_port'] + ", " 
        sSql += args['recvkey']  + ", "
        # to do, set the correct key for sendkey
        sSql += args['recvkey']  + ",  "
        sSql += "'" + args['master_avatar_uuid']  + "', "
        sSql += args['http_port']  + ", "
        sSql += "'" + args['region_secret']  + "', "
        sSql += "'" + args['sim_name']  + "',  "
        regionHandle =  self.convertTo(self.getRegionHandle(int(args['region_locx']), int( args['region_locy']) ), 'String') 
        sSql +=  regionHandle + " "
        #sSql += args['recvkey']  + ", "
        #sSql += args['recvkey']  + ", "
        #sSql += args['recvkey']  + ", "

        


                                                     
        sSql += ") "
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        print result
        # search neighbours
        x = int(args['region_locx'])
        y = int(args['region_locy'])
        
        sSql = "select locx,  locy , serverip as sim_ip, serverport as sim_port from regions where locx between  " + `x-1` + " and " + `x+1` 
        sSql += " and  locy between " + `y-1` + " and " + `y+1` 
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        
        # now send the answer
        dicAnswer = args
        dicAnswer['authkey'] = args['authkey']
        liRegion = []
        print result
        if result and result not in self.liSQL_ERRORS:
           
            for i in result:
                dicRecgion = {}
                dicRecgion[']regionHandle'] = self.convertTo(self.getRegionHandle(int(i['locx']), int( i['locy']) ), 'String') 
                dicRecgion['region_locx'] = `i['locx']`
                dicRecgion['region_locy'] = `i['locy']`
                dicRecgion['sim_ip'] = `i['sim_ip']`
                dicRecgion['sim_port'] = `i['sim_port']`
                dicRecgion['UUID'] = 'OpenSim.Data.RegionProfileData'
                
                liRegion.append(dicRecgion)
                
            
        dicAnswer['neighbours'] =liRegion
        
        
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

    def xmlrpc_simulator_data_request(self,  args):
        print 'simulator_data_request',  args
        
        resultDict = {}

        sSQL = "SELECT serverIP AS sim_ip, serverPort AS sim_port, serverURI AS server_uri, serverHttpPort "
        sSQL += "AS http_port, serverRemotingPort AS remoting_port, locX AS region_locx, locY AS region_locy, "
        sSQL += "uuid AS region_UUID, regionName AS region_name, regionHandle AS regionHandle "

        if 'regionUUID' in args:
            sSQL += "FROM regions WHERE uuid = '" + args['regionUUID'] + "'"
        elif 'region_handle' in args:
            sSQL += "FROM regions WHERE regionHandle = '" + args['region_handle'] + "'"
        elif 'region_name_search' in args:
            sSQL += "FROM regions WHERE regionName = '" + args['region_name_search'] + "'"
        else:
            print '[DATA] regionlookup without regionID, regionHandle or regionHame'

        resultDict = self.db_com.xmlrpc_executeNormalQuery(sSql)[0]

        if resultDict:
            returnDict = resultDict
        else:
            returnDict = {'error' : 'Sim does not exist'}
        
        print 'xmlrpc_simulator_data_request, return',  returnDict
        
        return returnDict
