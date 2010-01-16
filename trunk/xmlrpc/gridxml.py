

from xml.dom import minidom
from xml.dom.minidom import parse, parseString

class gridxml:
    
    def __init__(self):
        pass
    def createDoc(self,  sDTD='super_special.dtd',sDTD2='super_special2.dtd',   encoding = 'utf-8',  sRoot='test'  ):
        impl = minidom.getDOMImplementation()
        dt = impl.createDocumentType(sDTD +sDTD2, None, sRoot)
        doc = impl.createDocument(None, sRoot, dt)
        print doc.toxml()
        return doc
    
    def dic2xml(self,  doc, liParams, tag=None):
        #print 'liParams = ',  liParams

        for dicParams in liParams:
            doc = self.append2doc(doc,  dicParams)
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
        

