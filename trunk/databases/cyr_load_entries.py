# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

##***************************************************************************
##                          cyr_load_entries.py  -  description
##                             -------------------
##    begin                : Thu Jun 19 2003
##    copyright            : (C) 2003 by jhamel
##    email                : jhamel@cyrus.de
##***************************************************************************
from xmlrpc.MyXML import MyXML
import dataEntry
import string
import xmlrpc.xmlrpc

import cPickle
import sys
import setOfEntries 
from dumps import dumps

class cyr_load_entries(MyXML, dumps):

    def __init__(self):
        MyXML.__init__(self)
  
        self.rpc = xmlrpc.xmlrpc.myXmlRpc()
        
        #self.setLogLevel(self.ERROR)
        self.configPath = "./"


##        self.db = ZODB.DB(ZODB.FileStorage("cuon"))
##        self.connection = self.db.open()
##        self.root = self.connection.root()



    def getListOfEntriesNames(self, sFile):
        allLists = []
        doc = self.getEntriesDescription(sFile)
        #        cyRootNode = self.getRootNode(doc)
        if doc:
            allLists = doc.getElementsByTagName("table")
        return allLists
    

    def getEntriesDescription(self, sFile):
        return  self.readDocument(self.td.nameOfXmlEntriesFiles[sFile])

        
    def getEntriesDefinition(self, sFile,  sNameOfTable, sNameOfEntries):

        doc = self.getEntriesDescription(sFile)
        self.out( doc.toxml() )
        cyRootNode = self.getRootNode(doc)

        self.out( cyRootNode[0].toxml())

        self.out( 'sNameOfTable : '  + str(sNameOfTable))
        self.out( 'sNameOfentries : '  + str(sNameOfEntries))
        
        cyEntriesNode = self.getEntry(cyRootNode, sNameOfTable, sNameOfEntries)

   
        entrySet = setOfEntries.setOfEntries()

        entrySet.setName(sNameOfEntries)


        
        iNr =  self.getNumberOfEntries(cyEntriesNode)

        self.out("Number of Columns %i "  + `iNr` )
        iCol = 0
        while (iCol < iNr):
            xmlCol = self.getEntryAt(cyEntriesNode,iCol)
            
            entry =  cuon.Windows.dataEntry.dataEntry()

            entry.setName(self.getEntrySpecification(xmlCol, "name") )
            entry.setType(self.getEntrySpecification(xmlCol, "type") )
            entry.setSizeOfEntry(self.getEntrySpecification(xmlCol, "size") )
            entry.setVerifyType(self.getEntrySpecification(xmlCol, "verify_type") )
            entry.setCreateSql(self.getEntrySpecification(xmlCol, "create_sql") )
            entry.setSqlField(self.getEntrySpecification(xmlCol, "sql_field") )
            entry.setBgColor(self.getEntrySpecification(xmlCol, "bg_color") )
            entry.setFgColor(self.getEntrySpecification(xmlCol, "fg_color") )
            entry.setDuty(self.getEntrySpecification(xmlCol, "duty") )
            entry.setRound(self.getEntrySpecification(xmlCol, "round") )
            entry.setNextWidget(self.getEntrySpecification(xmlCol, "next_widget") )
            
##            s1 = `self.getEntrySpecification(xmlCol, "name") ` + ", "
##            s1 = s1 + `self.getEntrySpecification(xmlCol, "type") ` + ", "
##            s1 = s1 + `self.getEntrySpecification(xmlCol, "size") ` + ", "
##            s1 = s1 + `self.getEntrySpecification(xmlCol, "verify_type") ` + ", "
##            s1 = s1 + `self.getEntrySpecification(xmlCol, "create_sql") ` + ", "
##            s1 = s1 + `self.getEntrySpecification(xmlCol, "sql_field") ` + ", "
##            s1 = s1 + `self.getEntrySpecification(xmlCol, "bg_color") ` + ", "
##            s1 = s1 + `self.getEntrySpecification(xmlCol, "fg_color") ` + ", "
##            s1 = s1 + `self.getEntrySpecification(xmlCol, "duty") ` + ", "
##            s1 = s1 + `self.getEntrySpecification(xmlCol, "round")`
##            
##            print s1
            
            self.out( 'entry-gets = ' + str(entry.getName())  + ', ' + str(entry.getType()))
            entrySet.addEntry(entry)
            iCol += 1

        return entrySet

    def saveEntries(self, sNameOfEntries, entries ): 

        
        self.rpc.callRP('Database.saveInfo', sNameOfEntries, self.doEncode(repr(cPickle.dumps(entries) )))
        


    def loadEntries(self,sNameOfEntries):
        dictEntries = None
        self.openDB()
        #dictEntries = eval(self.doDecode(self.rpc.callRP('Database.getInfo', sNameOfEntries)))
        try:
            if self.td.SystemName:
                if self.td.SystemName == 'LINUX-Standard':
                    dictEntries = eval(self.doDecode(self.loadObject(sNameOfEntries)))
                else:
                    dictEntries = eval(self.doDecode(self.loadObject(+ self.td.SystemName + '_' + sNameOfEntries)))
            else:
                dictEntries = eval(self.doDecode(self.loadObject(sNameOfEntries)))
        except:
            print 'Error reading Entry Definition'
            dictEntries = eval(self.doDecode(self.loadObject(sNameOfEntries)))

        if not dictEntries:
            dictEntries = eval(self.doDecode(self.loadObject(sNameOfEntries)))
            
        self.closeDB()
        if dictEntries:
            entries = cPickle.loads(dictEntries)   

        
        return entries

   
