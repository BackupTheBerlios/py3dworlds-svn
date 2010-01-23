
from xml.dom import minidom
from xml.dom.minidom import parse, parseString

class gridxml:
    
    def __init__(self):
        pass
    def createDoc(self,  sDTD='super_special.dtd',sDTD2='super_special2.dtd',   encoding = 'utf-8',  sRoot='test'  ):
        impl = minidom.getDOMImplementation()
        #dt = impl.createDocumentType(sRoot , None, None)
        doc = impl.createDocument(None, sRoot, None)
        print doc.toxml()
        return doc
    def readXmlString(self,  sXml):    
        return parseString(sXml)
        
    def dic2xml(self,  doc, liParams, sTag=None):
        #print 'liParams = ',  liParams
        if sTag:
            rootNode = self.getRootNode(doc)
            tag = self.getSingleNode(rootNode, sTag)[0]
        else:
            tag = None
        for dicParams in liParams:
            doc = self.append2doc(doc,  dicParams,  tag)
        return doc
    
    def getDoc2String(self, doc):
        return doc.toxml("UTF-8")
        
    def append2doc(self, doc, dicParams,  tag = None):

        if tag is None:
            root = doc.documentElement
        else:
            root = tag
        
        #print 'dicParams = ',   dicParams
        for key, value in dicParams.iteritems():
            tag = doc.createElement(key)
            root.appendChild(tag)
            if isinstance(value, dict):
                self.append2doc(doc, value, tag)
            else:
                root.appendChild(tag)
                tag_txt = doc.createTextNode(value)
                tag.appendChild(tag_txt)
     
        return doc
    def xmltodict(self,  xmlstring):
        doc = minidom.parseString(xmlstring)
        self.remove_whilespace_nodes(doc.documentElement)
        return self.elementtodict(doc.documentElement)
    
    def elementtodict(self,  parent):
        child = parent.firstChild
        if (not child):
            return None
        elif (child.nodeType == minidom.Node.TEXT_NODE):
            return child.nodeValue
        
        d={}
        while child is not None:
            if (child.nodeType == minidom.Node.ELEMENT_NODE):
                try:
                    d[child.tagName]
                except KeyError:
                    d[child.tagName]=[]
                d[child.tagName].append(self.elementtodict(child))
            child = child.nextSibling
        return d
    
    def remove_whilespace_nodes(self,  node, unlink=True):
        remove_list = []
        for child in node.childNodes:
            if child.nodeType == minidom.Node.TEXT_NODE and not child.data.strip():
                remove_list.append(child)
            elif child.hasChildNodes():
                self.remove_whilespace_nodes(child, unlink)
        for node in remove_list:
            node.parentNode.removeChild(node)
            if unlink:
                node.unlink()
        

    def addElement(self, doc,  sName ):
        x = doc.createElement(sName)
        print x
        self.getRootNode(doc).appendChild(x)
        return doc
        
    def getRootNode(self, doc):
        return doc.documentElement
        
    def getSingleNode(self,  cyNode,  cyValue):
        return cyNode.getElementsByTagName(cyValue)  
