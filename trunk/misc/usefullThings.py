import xmlrpc.MyXML
import uuid

class usefullThings:
    def __init__(self):
        self.MyXml = xmlrpc.MyXML.MyXML()

    def stripIt(self,  dicValues):
        for key in dicValues:
            try:
                #very dirty
                #print dicValues[key]
                dicValues[key] = dicValues[key].strip()
            except:
                pass
        print 'after strip ',  dicValues
        return dicValues
    

    def getUUID(self):
        return  str(uuid.uuid4())

    
