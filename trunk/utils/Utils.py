# coding=utf-8


class Utils:

    def __init__(self):
        pass
        
    def make64BitInt(self, x, y):
        
        
        return   (long(x) << 32) + long(y)

        
    def  normalizeXML(self,  sValue):
        sValue = sValue.replace('&', '&amp;')
    #        sXml = sXml.replace('Ä', '&#196;')
    #        sXml = sXml.replace('Ö', '&#214;')#        sXml = sXml.replace('Ä', '&#196;')
    #        sXml = sXml.replace('Ö', '&#214;')
    #        sXml = sXml.replace('Ü', '&#220;')
    #        sXml = sXml.replace('ä', '&#228;')
    #        sXml = sXml.replace('ö', '&#246;')
    #        sXml = sXml.replace('ü', '&#252;')
    #        sXml = sXml.replace('ß', '&#223;')
    
    #        sXml = sXml.replace('Ü', '&#220;')
    #        sXml = sXml.replace('ä', '&#228;')
    #        sXml = sXml.replace('ö', '&#246;')
    #        sXml = sXml.replace('ü', '&#252;')
    #        sXml = sXml.replace('ß', '&#223;')
        sValue = sValue.replace('\'', '&apos;')
        sValue = sValue.replace('\"', '&quot; ')
        sValue = sValue.replace('<', '&lt;')
        sValue = sValue.replace('>', '&gt;')
           
        return sValue
        
    def getXmlSchema(self,  sName):
         # InventoryCollection
        return '<?xml version="1.0" encoding="utf-8"?><' + sName + ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n'
        
    
