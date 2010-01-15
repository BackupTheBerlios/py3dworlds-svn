# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

from xml.dom import minidom
from xml.dom.minidom import parse, parseString

#from xml.dom.ext.reader import Sax2
#from xml.dom import ext
from xml.dom import Node
#from xml.dom.ext.reader import PyExpat
import string
# from amara import *


class MyXML:
    """
    @author: Juergen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Loehne
    @copyright: by Juergen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """
    def __init__(self):
            pass

    def NotTextNodeError(self):
        pass

    def getTextFromNode(self, node):
        """
        scans through all children of node and gathers the
        text. if node has non-text child-nodes, then
        NotTextNodeError is raised.
        """
        t = ""
        for n in node.childNodes:
            if n.nodeType == n.TEXT_NODE:
                t += n.nodeValue
            else:
                raise NotTextNodeError
        return t
    
    
    def nodeToDic(self, node):
        """
        nodeToDic() scans through the children of node and makes a
        dictionary from the content.
            1. three cases are differentiated.
                  - if the node contains no other nodes, it is a text-node
                    and {nodeName:text} is merged into the dictionary.
                  - if the node has the attribute "method" set to "true",
                    then it's children will be appended to a list and this
                    list is merged to the dictionary in the form: {nodeName:list}.
                  - else, nodeToDic() will call itself recursively on
                    the nodes children (merging {nodeName:nodeToDic()} to
                    the dictionary).
        """
        print "nodeToDic"
        dic = {} 
        for n in node.childNodes:
            if n.nodeType != n.ELEMENT_NODE:
                continue
            if n.getAttribute("multiple") == "true":
                # node with multiple children:
                # put them in a list
                l = []
                for c in n.childNodes:
                    if c.nodeType != n.ELEMENT_NODE:
                        continue
                    l.append(nodeToDic(c))
                    dic.update({n.nodeName:l })
                    continue
        
                try:
                    text = getTextFromNode(n)
                except NotTextNodeError:
                    # 'normal' node
                    dic.update({n.nodeName:nodeToDic(n)})
                    continue
                
                # text node
                dic.update({n.nodeName:text})
                continue
            return dic
        
        
    def readDocument(self, filename):
        #    reader = PyExpat.Reader()
        #    doc = reader.fromUri(filename)
        #build a DOM tree from the file
        #self.out("filename = " + `filename`)
        doc = None
        try:
            doc = minidom.parse(filename)
        except Exception, param:
                print 'unknown exception by read XML-document'
                print `Exception`
                print `param`
        
        #self.out("Document =  " + doc.toxml() )


        return  doc
              
    def readXmlString(self,  sXml):    
        return parseString(sXml)
        
    def getRootNode(self, doc):
        return doc.childNodes

    def getListOfTables(self, cyNode):
        allTable = cyNode.getElementsByTagName("table")
        allNames = []
        for iNode in allTable:
            allName = iNode.getElementsByTagName("nameOfTable")
            for oneName in allName:
                rc = oneName.firstChild
                if rc.nodeType == Node.TEXT_NODE:
                  
                    allNames.append( rc.data) 
            
        return allNames

    def getListOfSequences(self, cyNode):
        allNames = []
        try:
            allTable = cyNode.getElementsByTagName("database_sequence")
           
            for iNode in allTable:
                allName = iNode.getElementsByTagName("nameOfSequence")
                for oneName in allName:
                    rc = oneName.firstChild
                    if rc.nodeType == Node.TEXT_NODE:
                        allNames.append( rc.data) 
            print "sequences allNames", allNames 
        except:
             pass
        return allNames
        
    def getListOfForeignKeys(self, cyNode):
        allTable = cyNode.getElementsByTagName("foreign_key")
        allNames = []
        for iNode in allTable:
            allName = iNode.getElementsByTagName("foreign_key_name")
            for oneName in allName:
                rc = oneName.firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    allNames.append( rc.data) 
        print "foreign_key allNames", allNames 
        return allNames

    def getTable(self, cyNode, cyName, cyValue):

        allTable = cyNode.getElementsByTagName("table")
        for iNode in allTable:
            allName = iNode.getElementsByTagName("nameOfTable")
            for oneName in allName:
                rc = oneName.firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    if(cyValue == rc.data):
                        #self.out( iNode.toxml())
                        #self.out("rc.data found = " +  rc.data)
                        return iNode

                    
    def getSequence(self, cyNode, cyName, cyValue):

        allTable = cyNode.getElementsByTagName("database_sequence")
        for iNode in allTable:
            allName = iNode.getElementsByTagName("nameOfSequence")
            for oneName in allName:
                rc = oneName.firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    if(cyValue == rc.data):
                        return iNode
                                     
    def getForeignKey(self, cyNode, cyName, cyValue):

        allTable = cyNode.getElementsByTagName("foreign_key")
        for iNode in allTable:
            allName = iNode.getElementsByTagName("foreign_key_name")
            for oneName in allName:
                rc = oneName.firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    if(cyValue == rc.data):
                        return iNode
                        
    def getNumberOfFields(self, cyTable):

        allColumns = cyTable.getElementsByTagName("field")
        return len(allColumns)
    

    def getColumnAt(self, cyTable, iIndex):
        allColumns = cyTable.getElementsByTagName("field")
        return allColumns[iIndex]


    def getTableSpecification(self, cyTable, sValue):
        nameTag = cyTable.getElementsByTagName(sValue)
        for oneName in nameTag:
            rc = oneName.firstChild
            if rc.nodeType == Node.TEXT_NODE:
                return rc.data
            else:
                return "EMPTY"
          

    def getColumnSpecification(self, cyColumn, sValue):
        nameTag = cyColumn.getElementsByTagName(sValue)
        for oneName in nameTag:
            rc = oneName.firstChild
            if rc:
                if rc.nodeType == Node.TEXT_NODE:
                    return rc.data
            else:
                return None
            
                        
        
    def test(self):
        import pprint
        doc = self.readDocument("/etc/cuon/tables.dbd")
        for n in doc.childNodes :
            print  n.nodeName
            for n2 in n.childNodes :
                print n2.nodeName
                

        cyRootNode = self.getRootNode(doc)
        print "----------------------------------------------------------------------------------"
        for n in cyRootNode :
            print  n.nodeName
        print cyRootNode[0].nodeName

        
        cyTestNode = self.getTable(cyRootNode[0], "table", "articles")
        table.createTable(cyTestNode)
        

    def getListOfEntries(self, cyNode):
        allEntries = cyNode.getElementsByTagName("table")
        allNames = []
        print cyNode.toxml()
        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        
        for iNode in allEntries:
            print iNode.toxml()
            ent =  iNode.getElementsByTagName("entry")
           
            for eNode in ent:
                eName = eNode.getElementsByTagName("name")
                rc = eName[0].firstChild
                if rc.nodeType == Node.TEXT_NODE:
                    allNames.append( rc.data) 
        print '###########################################################################'
        print allNames
        print '###########################################################################'
        
        return allNames
    
    def getEntries(self, sFileName):
        doc = self.readDocument(sFileName)
        

    def getEntry(self, cyNode, cyName, cyValue):
        
        for tNode in cyNode:
            oneTable = tNode.getElementsByTagName("table")
            print 'oneTable = ' + oneTable[0].toxml()
            for oneTableEntry  in oneTable:
                te = oneTableEntry.getElementsByTagName("entry")
              ##  print '**************************************************'
##                for te1 in te:
##                    print self.getEntrySpecification( te1, cyValue)
            
                

        return oneTableEntry
        

    
    
    def getNumberOfEntries(self, cyEntries):
            all = cyEntries.getElementsByTagName("entry")
            return len(all)
    

    def getEntryAt(self, cyEntries, iIndex):
        all = cyEntries.getElementsByTagName("entry")
        return all[iIndex]



    def getEntrySpecification(self, cyEntry, sValue):
        nameTag = cyEntry.getElementsByTagName(sValue)
        for oneName in nameTag:
            rc = oneName.firstChild
            if rc:
                if rc.nodeType == Node.TEXT_NODE:
                    return rc.data
                else:
                    return "EMPTY"
            else:
                return "EMPTY"
            
    def getSingleNode(self,  cyNode,  cyValue):
        return cyNode.getElementsByTagName(cyValue)
        
        
    def getNode(self, cyNode, cyValue):
        #print cyNode[0].toxml()
        OneNode = cyNode[0]
        element1 = OneNode.getElementsByTagName(cyValue)
        return element1
                             

    def getNodeData(self, cyNode, sValue):
        nameTag = cyNode[0]
        oneName = nameTag.getElementsByTagName(sValue)
        for oneElement in oneName:
            rc = oneElement.firstChild
            if rc.nodeType == Node.TEXT_NODE:
                return rc.data
            else:
                return "EMPTY"   

    def getNodes(self, cyNode, cyValue):
        #print cyNode[0].toxml()
        elements = cyNode.getElementsByTagName(cyValue)
        return elements

    def getData(self, cyNode):
        rc = cyNode.firstChild
        if rc and rc.nodeType == Node.TEXT_NODE:
            return rc.data
        else:
            return "EMPTY"   

            
    def getAttributValue(self, node, sName):
        s = None
        #print 'getAttributValue'
        #print node.toxml()
        #print '------------------------------------------------------'
        if node.hasAttributes():
            #print `node.attributes`
            #print '+++++++++++++++++++++++++++++++++++++++++++++++++++'
            s = node.getAttribute(sName)
            #print s
        return s
        
   
        
##        pprint.pprint(dic)
##        print dic["database"]["name"]
##        print
##        for item in dic["database"]["table"]:
##            print "table Name:", item["name"]
##            print "Item's Value:", item["x"]
            
                


##import pprint
##import xml.dom.minidom
##from xml.dom.minidom import Node
##doc = xml.dom.minidom.parse("books.xml")
##mapping = {}
##for node in doc.getElementsByTagName("book"):
##  isbn = node.getAttribute("isbn")
##  L = node.getElementsByTagName("title")
##  for node2 in L:
##    title = ""
##    for node3 in node2.childNodes:
##      if node3.nodeType == Node.TEXT_NODE:
##        title += node3.data
##    mapping[isbn] = title

### New Classes with AMARA-Object-Bindings
##
##    def getXmlDocument(self, filename)
##        assert filename
##        try:
##            doc = binderytools.bind_file('tables.xml')
##        exception:
##            doc = None
##            
##        return doc
##        
##        

