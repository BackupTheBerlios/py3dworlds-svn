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
