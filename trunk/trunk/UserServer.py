# coding=utf-8
from twisted.web import xmlrpc
from twisted.internet import reactor, defer

from databases.basics import basics
import databases.DB_Com
import uuid
from xmlrpc.xmlrpc import myXmlRpc
from misc.usefullThings import usefullThings


class UserServer( xmlrpc.XMLRPC, basics, myXmlRpc,  usefullThings):
    def __init__(self):
        
        xmlrpc.XMLRPC.__init__(self)
        basics.__init__(self)
        self.db_com = databases.DB_Com.DB_Com()
        
        myXmlRpc.__init__(self)
        usefullThings.__init__(self)
        self.dicExpectUser = {}
        
        
        
        self.defaultUser  = { 'last_name': 'Tairov', 'sim_ip':'85.214.139.187', 'start_location':"last" ,  'seconds_since_epoch': 20000, 'message':'Monday', 'first_name':'Juergen', 'circuit_code':3,  'sim_port':9300,'secure_session_id':'uuid333', 'look_at ':[1.0, 1.0, 1.0],  'agent_id':'aaabb-33dsd-seee', 'inventory_host':'localhost', 'region_y':0.0, 'region_x':0.0, 'seed_capability':'<llsd><map><key>request1</key><string>Capability1</string><key>request2</key><string>Capability2</string</map></llsd> ', 'agent_access': '0', 'session_id': 'aaddss-wewew-33222', 'login': 'true'} 
        
        
# 
#+-------------------+---------------------+------+-----+--------------------------------------+-------+
#| Field             | Type                | Null | Key | Default                              | Extra |
#+-------------------+---------------------+------+-----+--------------------------------------+-------+
#| UUID              | varchar(36)         | NO   | PRI |                                      |       | 
#| username          | varchar(32)         | NO   | MUL | NULL                                 |       | 
#| lastname          | varchar(32)         | NO   |     | NULL                                 |       | 
#| passwordHash      | varchar(32)         | NO   |     | NULL                                 |       | 
#| passwordSalt      | varchar(32)         | NO   |     | NULL                                 |       | 
#| homeRegion        | bigint(20) unsigned | YES  |     | NULL                                 |       | 
#| homeLocationX     | float               | YES  |     | NULL                                 |       | 
#| homeLocationY     | float               | YES  |     | NULL                                 |       | 
#| homeLocationZ     | float               | YES  |     | NULL                                 |       | 
#| homeLookAtX       | float               | YES  |     | NULL                                 |       | 
#| homeLookAtY       | float               | YES  |     | NULL                                 |       | 
#| homeLookAtZ       | float               | YES  |     | NULL                                 |       | 
#| created           | int(11)             | NO   |     | NULL                                 |       | 
#| lastLogin         | int(11)             | NO   |     | NULL                                 |       | 
#| userInventoryURI  | varchar(255)        | YES  |     | NULL                                 |       | 
#| userAssetURI      | varchar(255)        | YES  |     | NULL                                 |       | 
#| profileCanDoMask  | int(10) unsigned    | YES  |     | NULL                                 |       | 
#| profileWantDoMask | int(10) unsigned    | YES  |     | NULL                                 |       | 
#| profileAboutText  | text                | YES  |     | NULL                                 |       | 
#| profileFirstText  | text                | YES  |     | NULL                                 |       | 
#| profileImage      | varchar(36)         | YES  |     | NULL                                 |       | 
#| profileFirstImage | varchar(36)         | YES  |     | NULL                                 |       | 
#| webLoginKey       | varchar(36)         | YES  |     | NULL                                 |       | 
#| homeRegionID      | char(36)            | NO   |     | 00000000-0000-0000-0000-000000000000 |       | 
#| userFlags         | int(11)             | NO   |     | 0                                    |       | 
#| godLevel          | int(11)             | NO   |     | 0                                    |       | 
#| customType        | varchar(32)         | NO   |     |                                      |       | 
#| partner           | char(36)            | NO   |     | 00000000-0000-0000-0000-000000000000 |       | 
#| email             | varchar(250)        | YES  |     | NULL                                 |       | 
#| scopeID           | char(36)            | NO   |     | 00000000-0000-0000-0000-000000000000 |       | 
#+-------------------+---------------------+------+-----+--------------------------------------+-------+ '''


    def xmlrpc_getTest(self):
        return 42
        
  
    def getLoginData(self, sUsername, sLastname, sPassword, sStartPosition):
        sSql = "select users.uuid as uuid, users.lastname as last_name,  users.username as first_name,  "
        sSql += "  '{ region_handle: [' || '2562560,2561536' || '] , position: [' || to_char(users.homelocationx,'000.999999') "
        sSql += " || ', ' || to_char(users.homelocationy,'000.999999') || ', ' || to_char(users.homelocationz,'000.999999') || '] ,  look_at: ['"
        sSql += " || to_char(users.homelookatx,'000.999999') "
        sSql += " || ', ' ||  to_char(users.homelookaty,'000.999999') || ', ' || to_char(users.homelookatz,'000.999999') || '] }'  as home, "
        sSql += " '[1, 0, 0]' as look_at , 'A' as agent_access_max,  regions.serveruri as serveruri, "
        sSql += " '2562560' as region_x,  '2561536' as region_y, 1546967460 as circuit_code,  "
        sSql += " users.lastlogin as seconds_since_epoch,  'True' as login , "
        sSql += " users.uuid as agent_id , regions.serverip as sim_ip, 'last' as start_location, 'Hallo PyLife' as message,"
        sSql += " regions.serverport as sim_port,  'sim-linuxmain.org' as inventory_host,  'M' as agent_access,  "
        
        sSql += " agents.securesessionid as secure_session_id,  agents.sessionid as session_id "
        sSql += " from users , regions, agents where users.username = '" + sUsername + "' and users.lastname = '" + sLastname + "' "
        sSql +=  " and agents.uuid = users.uuid and agents.currentregion = regions.uuid "
        
        #sSql = "select * from agents where uuid = '" + result[0]['uuid'] + "' "
        
            
        #sSql = "select * from regions where uuid = '" + result[0]['currentregion'] + "' "
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        #print result3
        print '###################  regions #####'
    
        #dicUser = result[0]
        
            
        #self.server = 'http://' + dicUser['serverip'] + ':' + dicUser['serverhttpport']
        #self.callRP('expect_user',  )
        #inform the sim with expect_user
        print result[0]
        return result[0]
    def xmlrpc_login_to_simulator(self, args):
        print "Incoming --> ",   args
        dicResult = self.getLoginData(args['first'],  args['last'], args['passwd'],  args['start'])
        if dicResult not in ['NONE', 'ERROR']:
            dicResult = self.informSim(dicResult)
            #self.informSim(dicResult)
            

        return dicResult
        
    def informSim(self,  dicResult):
        #self.server = dicResult['serveruri']
        dicSimUser = {}
        self.server = 'http://cuonsim1.de:9300'
        # defaults for testing
        sSql = "select * from avatarappearance where owner = '" + dicResult['uuid'] + "' "
        dicSimUser = self.db_com.xmlrpc_executeNormalQuery(sSql)[0]
                
        dicSimUser['circuit_code'] = 105842181
        dicSimUser['regionhandle'] = "11006111396599296"
        dicSimUser['lastname'] = dicResult['last_name']
        dicSimUser['firstname'] = dicResult['first_name']
        dicSimUser['secure_session_id'] = dicResult['secure_session_id']
        dicSimUser['session_id'] = dicResult['session_id']
        dicSimUser['startpos_x'] = '20'
        dicSimUser['startpos_y'] = '20'
        dicSimUser['startpos_z'] = '40'
        dicSimUser['caps_path']= self.getUUID()
        dicSimUser['region_x'] = `dicResult['region_x']`
        dicSimUser['region_y'] = `dicResult['region_y']`
        dicSimUser['folder_id'] = '3e1a8134-f9d7-40a1-9a01-7fff99ac8536'
        dicSimUser['owner'] = 'fb65174f-2dde-4c1e-ba13-1a776d6864fd'
        
        
        # test it
        #self.server = 'http://cuonsim2.de:7080'
        #answer = self.callRP('Database.is_running' )
        #print 'Answer 1 = ',  answer
        #sys.exit(0)
        
        answer = self.callRP('expect_user',  dicSimUser)
        print 'answer from sim:',  answer
        doc = self.MyXml.readXmlString(answer)
        print doc
        element = self.MyXml.getRootNode(doc)
        print element
#        for i in ['params','param', 'value', 'struct']:
#            element = self.MyXml.getNode(element, i)
#            print element
        elements = self.MyXml.getNodes(element[0], 'member')
        print 'elements = ',  elements
        reason = ''
        for oneMember in elements:
            print 'onemember = ',  oneMember
            print 'node = ',  self.MyXml.getSingleNode(oneMember, 'name')
            
            if  self.MyXml.getData(self.MyXml.getSingleNode(oneMember, 'name')[0]) == 'success':
                print 'success gefunden'
#                node1 = self.MyXml.getSingleNode(oneMember, 'value')
#                node2 = self.MyXml.getNode(node1,'string')
#                data = self.MyXml.getData(node2[0])
#                print data 
                dicResult['login'] = self.MyXml.getData(self.MyXml.getNode(self.MyXml.getSingleNode(oneMember, 'value'), 'string')[0]).lower() 
                print dicResult['login'] 
                
            if  self.MyXml.getData(self.MyXml.getSingleNode(oneMember, 'name')[0]) == 'reason':
                print 'reason gefunden'
                reason = self.MyXml.getData(self.MyXml.getNode(self.MyXml.getSingleNode(oneMember, 'value'), 'string')[0]).lower() 
        if dicResult['login'] == 'false':
            dicResult['message'] = reason
            
#        print 'success = ',      self.MyXml.getData(self.MyXml.getNode(element, 'name')[0])
#        if  self.MyXml.getData(self.MyXml.getNode(element, 'name')[0]) == 'success':
#             dicResult['login'] = self.MyXml.getData(self.MyXml.getNode(self.MyXml.getNode(element, 'value'), 'string')[0]).lower()
#             if dicResult['login'] == 'false':
#                 if if  self.MyXml.getData(self.MyXml.getNode(element, 'name')[0]) == 'reason':
#                 dicResult['message'] = 
#               
        dicResult['seed_capability'] = dicResult['serveruri'] + '/CAPS/' + dicResult['caps_path'] +'0000/'

        return dicResult
        
        
        
    def xmlrpc_get_user_by_uuid(self, args):
        print 'get_user_by_uuid ',  args
        
        
        # response >custom_type profile_want_do  home_region_id >profile_created >profile_image >home_coordinates_x  profile_firstlife_image home_coordinates_y home_coordinates_z >server_asset home_look_x 
        sSql = "select to_char(profileWantDoMask,'99999999999' )as profile_want_do, homeregionid as home_region_id , to_char(users.created,'999999999999') as profile_created, "
        sSql += " profileImage as profile_image ,  to_char(homelocationx,'FM990.99999') as  home_coordinates_x,  to_char(homelocationy,'FM990.99999') as  home_coordinates_y,  to_char(homelocationz,'FM990.99999') as  home_coordinates_z, "
        sSql += " users.partner,  '' as server_asset,  to_char(profileCanDoMask,'FM99999999990') as profile_can_do,  users.uuid as uuid ,  users.username as firstname,  "
        sSql += " to_char(godlevel,'FM999990') as god_level, '' as   server_inventory,  to_char(userflags,'FM9999999999990') as user_flags,  profileabouttext as profile_about ,  "
        sSql += "to_char(homeregion,'FM9999999999999999990') as home_region,  profilefirsttext as profile_firstlife_about , "
        sSql += " to_char(homelookatx,'FM990.99999') as home_look_x, to_char(homelookaty,'FM990.99999') as home_look_y, to_char(homelookatz,'FM990.99999') as home_look_z "
        sSql += " from users  where users.uuid = '" + args['avatar_uuid'] + "' "
        dicUser = self.db_com.xmlrpc_executeNormalQuery(sSql)[0]
        print dicUser
        dicUser['custom_type'] = ' '
        dicUser = self.stripIt(dicUser)    
        return dicUser
        
    def xmlrpc_update_avatar_appearance(self, args):
        print 'update_avatar_appearance ',  args 
         
    def xmlrpc_check_auth_session(self, args):
        print 'check_auth_session ',  args
        
        #session_id, avatar_uuid
        
        dicSession = {'auth_session':'TRUE'}
        return dicSession
        

    def xmlrpc_get_agent_by_uuid(self, args):
        print 'get_agent_by_uuid ',  args
        sSql = "select agents.sessionID as session,  to_char(currentHandle, '999999999999999999999') as handle,  'FALSE' as agent_online "
        sSql += " from users, agents where users.uuid = '" + args['avatar_uuid']+ "' and agents.uuid = '" + args['avatar_uuid']+ "' "
        
        result = self.db_com.xmlrpc_executeNormalQuery(sSql)
        print "result = ",  result
        if result not in self.liSQL_ERRORS:
            return result[0]
        else:
            return {'agents.sessionID': self.NullKey}
                            
    def getNewUUID(self):  
       
        return str(uuid.uuid4())
