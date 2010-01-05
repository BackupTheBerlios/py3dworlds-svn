# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

from xmlrpc.MyXML import MyXML
import cyr_table, cyr_column
import string
import re
import xmlrpc.xmlrpc

import cPickle
import sys
#sys.path.append('/usr/lib/zope/lib/python')

#from ZODB import FileStorage, DB
from dumps import dumps
from constants import constants



class cyr_load_table( constants,  MyXML, dumps):

    def __init__(self):
        constants.__init__(self)
        MyXML.__init__(self)
        dumps.__init__(self)
        
        self.rpc = xmlrpc.xmlrpc.myXmlRpc()
        
        self.configPath = "./"





    def getListOfTableNames(self, sFile):
        doc = self.getDatabaseDescription(sFile)
        
        #        cyRootNode = self.getRootNode(doc)
        allLists = self.getListOfTables(doc)
        return allLists

    def getListOfSequenceNames(self, sFile):
        doc = self.getDatabaseDescription(sFile)
        #        cyRootNode = self.getRootNode(doc)
        allLists = self.getListOfSequences(doc)
        return allLists
    
    def getListOfForeignKeyNames(self, sFile):
        doc = self.getDatabaseDescription(sFile)
        #        cyRootNode = self.getRootNode(doc)
        allLists = self.getListOfForeignKeys(doc)
        return allLists
    

    def getForeignKeyDefinition(self, sFile, nameOfForeignKey):
        dicForeign= {}
        doc = self.getDatabaseDescription(sFile)
        self.out( doc.toxml() )
        dicForeign['name'] = nameOfForeignKey.encode('ascii')

        cyRootNode = self.getRootNode(doc)
        #print cyRootNode[0].toxml()
        #print nameOfSequence
        
        cyForeignNode = self.getForeignKey(cyRootNode[0], "foreign_key", nameOfForeignKey)
        print 'cyForeignNode'
        print cyForeignNode.toxml()
        
                
        dicForeign['name'] = self.getData(self.getNodes(cyForeignNode, 'foreign_key_name')[0]).encode('ascii')
        dicForeign['sql'] = self.getData(self.getNodes(cyForeignNode, 'foreign_key_sql')[0]).encode('ascii')
        dicForeign['table'] = self.getData(self.getNodes(cyForeignNode, 'foreign_table')[0]).encode('ascii')
        print dicForeign
        
        return dicForeign
    
    def getDatabaseDescription(self, sFile):
        return  self.readDocument(sFile)


    def getSequenceDefinition(self, sFile, nameOfSequence):
        dicSeq = {}
        doc = self.getDatabaseDescription(sFile)
        self.out( doc.toxml() )
        dicSeq['name'] = nameOfSequence.encode('ascii')

        cyRootNode = self.getRootNode(doc)
        #print cyRootNode[0].toxml()
        #print nameOfSequence
        
        cySeqNode = self.getSequence(cyRootNode[0], "database_sequence", nameOfSequence)
        #print 'cySeqNode'
        #print cySeqNode.toxml()
        
                
        dicSeq['increment'] = self.getData(self.getNodes(cySeqNode, 'sequence_increment')[0]).encode('ascii')
        dicSeq['start'] = self.getData(self.getNodes(cySeqNode, 'sequence_start')[0]).encode('ascii')
        dicSeq['minvalue'] = self.getData(self.getNodes(cySeqNode, 'sequence_minvalue')[0]).encode('ascii')
        dicSeq['maxvalue'] = self.getData(self.getNodes(cySeqNode, 'sequence_maxvalue')[0]).encode('ascii')
        dicSeq['cycle'] = self.getData(self.getNodes(cySeqNode, 'sequence_cycle')[0]).encode('ascii')
        dicSeq['cache'] = self.getData(self.getNodes(cySeqNode, 'sequence_cache')[0]).encode('ascii')

        print dicSeq
        
        return dicSeq
    
    def getTableDefinition(self, sFile,  sNameOfTable):
        
        doc = self.getDatabaseDescription(self.nameOfXmlTableFiles[sFile])
        self.out( doc.toxml() )
        cyRootNode = self.getRootNode(doc)
   
        cyTableNode = self.getTable(cyRootNode[0], "table", sNameOfTable)
   
        table = cyr_table.cyr_table()

        table.setName(sNameOfTable)
        table.setSpecials(self.getTableSpecification(cyTableNode, "specials") )
        
        #self.out("searching Subtable")
#        subtable = re.search(r'inherits.*\((.*?)\)', str(table.getSpecials()), re.IGNORECASE)
#        if subtable:
#            sNameOfSubtable = subtable.group(1)
#            #self.out('----------------------------------Subtable found-----------------------------------------------')
#            #self.out('Subtable -> ' + str(subtable))
#            #self.out('Subtable -> ' + subtable.group(0))
#            #self.out('Subtable -> ' + subtable.group(1))
#            subTable = self.loadTable(sNameOfSubtable)
#            xColumns = subTable.getColumns()
#            for i in xColumns:
#                table.addColumn(i)
#                table.nameOfColumns.append(i.getName())
#                   

        iNr =  self.getNumberOfFields(cyTableNode)

        #self.out("Number of Columns %i "  + `iNr` )
        iCol = 0
        while (iCol < iNr):
            xmlCol = self.getColumnAt(cyTableNode,iCol)
            column = cyr_column.cyr_column()

            column.setName(self.getColumnSpecification(xmlCol, "name") )
            #self.out("column-name = " + column.getName() )
            table.nameOfColumns.append(column.getName())

            column.setType(self.getColumnSpecification(xmlCol, "type") )
            sSize = string.strip(self.getColumnSpecification(xmlCol, "size"))
            if sSize: 
                column.setSizeOfDatafield(string.strip(self.getColumnSpecification(xmlCol, "size")) )
            else:
                column.setSizeOfDatafield('18')

                
            
            column.setAllowNull(string.atoi(self.getColumnSpecification(xmlCol, "notnull")) )
            column.setPrimaryKey(string.atoi(self.getColumnSpecification(xmlCol, "pkey")) )
            column.setDefaultValue(self.getColumnSpecification(xmlCol, "default") )

            
            table.addColumn(column)
            iCol += 1

        return table

    def saveTable(self, sNameOfTable, table ): 
        
        self.out( sNameOfTable)
        self.out( table.getName())
#        self.out( cPickle.dumps(table))
        print "::::::::::::::::::::::::::", ` cPickle.dumps(table)`
        #self.rpc.callRP('Database.saveInfo', sNameOfTable, self.doEncode(repr(cPickle.dumps(table) )))
        liColumns = table.getColumns()
        for i in liColumns:
            print 'save table-columns TTTZZ'
            print i.getName()
            co_name = sNameOfTable + '_' + i.getName()
            #self.rpc.callRP('Database.saveInfo', co_name, self.doEncode(repr(cPickle.dumps(i))) )
            print co_name
            print ' TTTTUU'

    def loadTable(self,sNameOfTable):
        self.openDB()
        dictTable = eval(self.doDecode(self.rpc.callRP('Database.getInfo', sNameOfTable)))
        self.out('*****************************************************************************ZZ')
        self.out(dictTable)
        self.out('****************************************************************************UU')
        table = cPickle.loads(dictTable)
        #print '******************************************************************PPPP'
        self.saveObject('table_' + sNameOfTable.encode('ascii'), table)
        print 'table of Columns --> ' + str (table.nameOfColumns) 
        for i in table.nameOfColumns:
            #print i
            sColumn = eval(self.doDecode(self.rpc.callRP('Database.getInfo', sNameOfTable + '_' + i)))
            coColumn = cPickle.loads(sColumn)
            table.addColumn(coColumn)
            self.saveObject('column_' + sNameOfTable.encode('ascii') + '_' + i.encode('ascii'), coColumn) 
        #print table.nameOfColumns
        #print table.getCountOfColumns()
        self.closeDB()
        #ok = self.rpc.callRP('src.Databases.py_packCuonFS')
        return table


    def loadLocalTable(self, sNameOfTable):
        #print '--------------------------'
        #print 'table = ' + `sNameOfTable`
        #print '--------------------------'
        self.openDB()
        table = self.loadObject('table_' + sNameOfTable.encode('ascii'))
        if table:
            #print 'table of Columns --> ' + str (table.nameOfColumns) 
            for i in table.nameOfColumns:
                #print i
                coColumn = self.loadObject('column_' + sNameOfTable.encode('ascii') + '_' + i.encode('ascii')) 
                table.addColumn(coColumn)
                #print table.nameOfColumns
                #print table.getCountOfColumns()
        self.closeDB()
        return table
        
    def loadTableOld(self, sNameOfTable):
        storage = FileStorage.FileStorage('cuon3.fs')
        db = DB(storage)
        connection = db.open()
        root = connection.root()
        self.out( root.items())
        self.out( "-------------------------------------------------------------------------------------------------------")
        t2 = root[sNameOfTable]
        connection.close()
        db.close()
        return t2
    

        
        


##}

##/** load the xml-file ( from sql-server or disk ) */

##bool cyr_load_table::writeDatabaseDescription(int nFile, xmlpp::DomParser* databaseDefinition){
##  // write  
    
##  std::cout << "read XML-file " << std::endl ;
##  std::string FileName = *configPath +*(nameOfFiles.begin() +nFile);
##  std::cout << "FileName = " << FileName << std::endl ;

##  //    FileName.assign(* nameOfFiles.begin() +nFile)
##  databaseDefinition->write_to_file(FileName);

##  return true ;

##}


##/** gets the definition of the table */
##cyr_table* cyr_load_table::getTableDefinition(std::string *nameOfTable, int nFile){
    
##  // std::cout << "read XML-File " << std::endl ;

##  MyXML myxml;

##  xmlpp::DomParser *databaseDefinition = getDatabaseDescription(nFile);
##  cyr_table *table = new cyr_table() ;

    
##  xmlpp::Node* xtroot = databaseDefinition->get_root_node();
##  // std::cout << "cuon.ini root =  " << xtroot.name() << std::endl ;
##  // std::cout << "nameOfTables = " << *nameOfTable << std::endl ;

##  xmlpp::Node::NodeList xmlTable = xtroot->get_children("table");

##  for(xmlpp::Node::NodeList::iterator iX0 = xmlTable.begin(); iX0 != xmlTable.end();iX0++){
##    xmlpp::Node &Table = **iX0;
  
    
##    xmlpp::Node::NodeList xmlFields = Table.get_children();
  

##    if(myxml.find(xmlFields,"name") == *nameOfTable){
##       std::cout << "table " << *nameOfTable << " gefunden !!" << std::endl ;
##      table->setName(*nameOfTable);

##      table->setSpecials(myxml.find(xmlFields,"specials") ) ;
##      std::cout << "Specials = " << table->getSpecials() << std::endl ;

    
##      for(xmlpp::Node::NodeList ::iterator iX = xmlFields.begin();iX != xmlFields.end();iX++){
##  xmlpp::Node::Node &Field = **iX;
##  if(Field.get_name() == "field"){
##      std::cout << "fields erreicht " << std::endl ;
##    xmlpp::Node::NodeList  FieldsNL = Field.get_children();
      
##    cyr_column colX2 ; // = new cyr myXml.getNumberOfFields(xmlTable_column() ;
      
##    std::string PrimaryKeyField = myxml.find(FieldsNL,"name");
##     std::cout << "Name in XML = " <<  PrimaryKeyField << std::endl ;
      
##    colX2.setName( myxml.find(FieldsNL,"name"));
      
##    colX2.setType(myxml.find(FieldsNL,"type"));
##    colX2.setAllowNull(new bool((myxml.find(FieldsNL,"notnull"))=="0" ? false : true) );
##    if(myxml.find(FieldsNL,"pkey") == "1"){
##      colX2.setPrimaryKey(PrimaryKeyField );
##    }
      
##    int sot;
##    sot = atoi((myxml.find(FieldsNL,"size").c_str())) ; 
##    colX2.setSizeOfDatafield(sot);
      
##    sot = atoi((myxml.find(FieldsNL,"column_id").c_str())) ; 
##    colX2.setColumnID(sot);

      
##    colX2.setNameOfVariable(myxml.find(FieldsNL,"var_name"));
##    colX2.setTypeOfVariable(myxml.find(FieldsNL,"var_type"));
    
##    sot = atoi((myxml.find(FieldsNL,"var_length").c_str())) ; 
##    colX2.setMaxLengthOfVariable(sot);
    
##    table->addColumn(colX2);

##  }
##      }
##    }
##  }
##  // std::cout << "xml finished" << std::endl;

##  //  table->getColumnAtIndex(0) ;
##  //  table->getColumnAtIndex(1) ;

##  std::cout << "cyr_load_table 1" << std::endl ;    

##  for(int zaehler=0;zaehler<table->getCountOfColumns();zaehler++){
##    table->getColumnAtIndex(zaehler) ;
##    std::cout <<    "zaehler = " << zaehler << std::endl ;
##  }

##  std::cout << "cyr_load_table 2" << std::endl ;    
##  return table ;
##}

##std::vector<std::string> cyr_load_table::getNameOfTables(int nFile){
  
##  MyXML myxml;
##  // std::cout << "cyr_load_table getNameOfTables started " << std::endl ;
 

##  xmlpp::DomParser *databaseDefinition = getDatabaseDescription(nFile);
## std::vector<std::string> NameOfTables ;

##  xmlpp::Node*  xtroot = databaseDefinition->get_root_node();
##  xmlpp::Node::NodeList  xmlTable = xtroot->get_children("table");


## for(xmlpp::Node::NodeList::iterator iX0 = xmlTable.begin(); iX0 != xmlTable.end();iX0++){
##    xmlpp::Node &Table = **iX0;
  
    
##    xmlpp::Node::NodeList  xmlFields = Table.get_children();
  
##    std::string s = "";
##    s = myxml.find(xmlFields,"name");
##    if(s.size() > 0){
##      // std::cout << "tables in nameOfTables = " << s << std::endl ;
##  NameOfTables.push_back(s);
##    }
    
## }

##// for(XMLNodeIterator iX0 = xmlTable.begin();iX0 != xmlTable.end();iX0++){
##//     std::cout << "for working iX0" << std::endl ;
   
##//     XMLNode &Table = **iX0;
##//     XMLNodeList xmlFields = Table.children();
    

##//     for(XMLNodeIterator iX = xmlFields.begin();iX != xmlFields.end();iX++){

##//       XMLNode &Field = **iX;
##//       XMLNodeList FieldsNL = Field.children();
   
##//     }
##//   }

## // std::cout << "Size Of NameOfTables = " << NameOfTables.size() << std::endl ;

##  //    TiXmlNode* node = 0;
##  //     TiXmlElement* tableElement = 0;
##  //     TiXmlElement* nameElement = 0;

##  //     TiXmlElement* fieldElement = 0;

##  //     node = databaseDefinition->FirstChild( "database" );
##  //     assert( node );
##  //     std::cout << "node-Value = " << node->Value() << std::endl;

##  //     TiXmlNode *child = 0;
##  //     while( child = node->IterateChildren( child ) ){
##  //         if(child != 0){
##  //      std::cout << "child = " << child->Value() << std::endl ;
##  //      if(child->Value() == "table"){
##  //      std::cout << "table gefunden"  << std::endl ;
        
##  //      TiXmlNode *child1 = child->FirstChild() ;
        
##  //      tableElement = child1->ToElement();
##  //      assert( tableElement  );
##  //      std::cout << "Element-Value = " << tableElement->Value() << std::endl;
    


##  //      if(tableElement->Value() == "name"){ 
##  //          TiXmlNode * child2 = child1->FirstChild();
##  //          TiXmlText *text = child2->ToText();
##  //          std::cout << "Test = " << text->Value() <<  std::endl ;
##  //          std::string *s = new std::string();
##  //          s->assign(text->Value());
##  //          NameOfTables.push_back(*s);
##  //      }


##  //      }
##  //  }
##  //     }


##  return NameOfTables;
##}

##void cyr_load_table::addExistingTable(){
##}
