# coding=utf-8
from twisted.web import xmlrpc
from databases.basics import basics
import UserServer


class login(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
        xmlrpc.XMLRPC.__init__(self)
        self.userServer = UserServer.UserServer()
        self.liSLUser = ['last_name',  'first_name', 'agent_id', 'inventory_host', 'region_y', 'region_x', 'secure_session_id',  'seed_capability', 'agent_access' , 'session_id' , 'login','sim_ip',  'seconds_since_epoch', 'message', 'circuit_code',   'sim_port', 'look_at ' ]
        
        self.liDataUser = ['lastname', 'username', 'uuid', 'userinventoryuri', 'homelocationx', 'homelocationy', 'securesessionid' ]

        
    def xmlrpc_login_to_simulator(self, args):
        ''' Required Response

    last_name

        last name of avatar--identical to name given in input parameters 

    { 'last_name': <last_name>} 

    sim_ip

        ip address used to establish UDP connection with startup simulator 

    { 'sim_ip':<ip_num> } 

    start_location

        Result of 'start' parameter as specified in input parameters 

    {'start_location':"first" | "last" | <specific location> } 

    seconds_since_epoch

        seconds... clarification needed 

    'seconds_since_epoch':<int> 

    message

        message of the day from login 

    { 'message': <string> } 

    first_name

        first name of avatar--identical to name given in input parameters 

    [ 'first_name': <first_name> } 

    circuit_code

        used to validate UDP connection with login simulator 

    { 'circuit_code': <int> } 

    sim_port 
    port used to establish UDP connection with login simulator

        { 'sim_port':<int> } 

    secure_session_id 
    secure token for this login session--never used in UDP packets (unknown if this is unique per login or unique per simulator) clarification needed

        'secure_session_id': <uuid> 

    look_at 
    initial camera direction (3D vector) of avatar

        { 'look_at ': r + <real>, r + <real>, r + <real> } 

    agent_id

        permanent UUID of avatar 

    { 'agent_id': <uuid> } 

    inventory_host

        name of database used for inventory 

    { 'inventory_host': <name> } 

    region_y

        The 'y' grid coordinate of the region 

    { 'region_y': <int> } 

    region_x

        The 'x' grid coordinate of the region 

    { 'region_x': <int> } 

    seed_capability

        [Capabilities|Capability]] that provides access to various capabilities as described in Current_Sim_Capabilities, the most import of these is the EventQueueGet 

    { 'seed_capability': <capability> } 

    agent_access: M

        authorization information about access to main/mature grid as opposed to teen grid clarification needed 

    { 'agent_access': <'M'|'T'> } 

    session_id

        "UUID for current session with simulator. used in UDP message passing clarification needed 

    {'session_id': <uuid> } 

    login

        ... clarification needed 

    { 'login': 'true' } 

Optional Response

    inventory-root

        UUID of the agent’s root inventory folder. 

    { 'inventory-root': [{'folder_id': <uuid>}] } 

    inventory-skeleton

        Initial list of folders in agent’s inventory. Returned as an array of five-entry dictionaries. Each dictionary element describes a folder with its name, version, type, its UUID, and the UUID of the containing folder. 

    {'inventory-skeleton': [{'parent_id': <uuid>, 'version': <int>, 'name': <name>, 'type_default': <int>, 'folder_id': <uuid>}, .... ]} 

    inventory-lib-root

        folder_id of library root inventory folder. 

    { 'inventory-lib-root': [{'folder_id': <uuid>}] } 

    inventory-lib-owner

        agent_id of owner for inventory lib. Used to establish common inventory library for all avatars in Second Life 

Note: Not the same as the agent_id in the required response section

    { 'inventory-lib-owner': [{'agent_id': <uuid>}] } 

    inventory-skel-lib

        Initial list of folders in agent’s inventory. Returned as an array of five element dictionaires. Each dictionary describes a folder with its name, its UUID, the UUID of the containing folder, its type, its version. 

    {'inventory-skeleton': [{'parent_id': <uuid>, 'version': <int>, 'name': <name>, 'type_default': <int>, 'folder_id': <uuid>},... ]} 

    gestures

        List of active gestures. An array of two element dictionaries with the inventory item uuid and the asset uuid. 

    { 'gestures': [{'item_id': <uuid>, 'asset_id': <uuid>},...] } 

    event_categories

        List of different event categories, mapping category id (an integer) to a category name. Returned as an array of two element dictionaries. Each dictionary describes a category’s id and it’s name. 

    { 'event_categories': [{'category_id': <int>, 'category_name': <name>},...] } 

    event_notifications

        List of events for which the agent has pending notifications. An array of eight-element dictionaries containing: event_id, event_name, event_desc, event_date, grid_x, grid_y, x_region, y_region. 

    {'events': [{"event_id":<uuid>, "event_name"<name>,"event_desc":<string>, "event_date":<date>, "grid_x":<float>, "grid_y":<float>, "x_region":<float>, "y_region":<float>}, ...]} 

    classified_categories"

        List of classifieds categories, mapping category id (an integer) to a category. Returned as an array of two element dictionaries with a category’s id and it’s name. 

    { 'event_categories': [{'category_id': <int>, 'category_name': <name>},...] } 

    buddy-list

        List of friends with granted and given rights masks. Returned as an array of three-element dictionaries with riend’s agent id, granted rights mask, given rights mask. 

    { 'buddy-list':[{'buddy_id': <uuid>', 'buddy_rights_given': <int>, 'buddy_rights_has': <int>}, ....] } 

    ui-config

        list of UI enabled/disabled states, currently: allow_first_life ('Y' or 'N') for teens. 

    { 'ui-config': {'allow_first_life': if allow first life} } 

    login-flags

        Several flags about the state of the agent. 

    { 'login-flags': {'stipend_since_login': <'Y'|'N'>, 'ever_logged_in': <'Y'|'N'>, 'gendered': <'Y'|'N'>, 'daylight_savings': <'Y'|'N'>} } 

    global-textures

        The asset ids of several global textures. 

    { 'global-textures': {'sun_texture_id': <uuid>, 'moon_texture_id': <uuid>, 'cloud_texture_id': <uuid>} } 

    adult_compliant

        No special data returned, but this parameter indicates the viewer understands the 'Adult' region access level 
'''

        print "Incoming --> ",   args
        dicResult = self.userServer.getLoginData(args['first'],  args['last'], args['passwd'],  args['start'])
        if dicResult not in ['NONE', 'ERROR']:
            dicResult = self.userServer.informSim(dicResult)
            
        return dicResult
        
    def get_user_by_uuid(self, args):
        
    def update_avatar_appearance(self, args):
           
    def check_auth_session(self, args):
        print args
