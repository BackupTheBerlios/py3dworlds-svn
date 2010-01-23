import httplib, urllib


class webclient:
    def __init__(self):
        pass
        
    def executeConnect(self, port, params,  sCall):
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/xml",  "Content-Length": len(params)}

        conn = httplib.HTTPConnection("py3d-worlds.org:" + `port`)
        conn.request("POST", sCall, params, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        print data
        conn.close()
        return data
        
    def test_getInventory01(self):
        Port = 8004 
        params = '<?xml version="1.0" encoding="utf-8"?><RestSessionObjectOfGuid xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><SessionID>c52a992a-96f8-90f3-b7e4-0c6d9abc9dee</SessionID><AvatarID>fb65174f-2dde-4c1e-ba13-1a776d6864fd</AvatarID><Body>fb65174f-2dde-4c1e-ba13-1a776d6864fd</Body></RestSessionObjectOfGuid>'

        sCall = "/GetInventory/"
        #sCall = None
        return self.executeConnect(Port,  params, sCall)

    def test_getInventory02(self):
        ''' AddItem'''
        Port = 8004 
        params = '<?xml version="1.0" encoding="utf-8"?><RestSessionObjectOfInventoryItemBase xmlns:xsi="http://www .w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchem a"><SessionID>178bc3f1-4a7a-15d5-b15a-6efa6dbe4f2b</SessionID><AvatarID>fb6 5174f-2dde-4c1e-ba13-1a776d6864fd</AvatarID><Body><Name>New Underpants</Nam e><ID><Guid>5162426b-f857-4462-9946-de022e585b05</Guid></ID><Owner><Guid>fb 65174f-2dde-4c1e-ba13-1a776d6864fd</Guid></Owner><InvType>18</InvType><Fold er><Guid>26bdf276-ef62-40c0-b727-fd26c561d193</Guid></Folder><CreatorId>fb6 5174f-2dde-4c1e-ba13-1a776d6864fd</CreatorId><CreatorIdAsUuid><Guid>fb65174 f-2dde-4c1e-ba13-1a776d6864fd</Guid></CreatorIdAsUuid><Description /><NextP ermissions>532480</NextPermissions><CurrentPermissions>2147483647</CurrentP ermissions><BasePermissions>2147483647</BasePermissions><EveryOnePermission s>0</EveryOnePermissions><GroupPermissions>0</GroupPermissions><AssetType>5 </AssetType><AssetID><Guid>071030a9-beb6-7351-eb31-edd8f9f49cb1</Guid></Ass etID><GroupID><Guid>00000000-0000-0000-0000-000000000000</Guid></GroupID><G roupOwned>false</GroupOwned><SalePrice>0</SalePrice><SaleType>0</SaleType>< Flags>11</Flags><CreationDate>1264086774</CreationDate></Body></RestSession ObjectOfInventoryItemBase>'
        
     
        sCall = "/AddItem/"
        #sCall = None
        return self.executeConnect(Port,  params, sCall)   
