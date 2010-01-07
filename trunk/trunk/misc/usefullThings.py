
class usefullThings:
    def __init__(self):
        pass

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
    
