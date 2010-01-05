#!/usr/bin/env python
# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jügen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import string
#import logging
#sys.path.append('/usr/lib/zope/lib/python')
#import ZODB
#import Persistence



import cyr_column 
import cyr_load_table
from xmlrpc.MyXML import MyXML


class cyr_table:

    def __init__(self):
    ##    logging.basicConfig()
##        self.log = logging.getLogger("cyr_table")
##        self.log.setLevel(logging.DEBUG)
##        self.log.info("cyr_table startet")
   
        self.Adabas = 1
        self.mSql = 2 
        self.Mysql = 3
        self.Sybase = 4 
        self.Interbase = 5 
        self.Oracle = 6 
        self.Informix = 7 
        self.Microsoft = 8 
        self.nameOfColumns = []
        self.Columns = []
        self.oneColumn = cyr_column.cyr_column();

    
        



    # set the name of the table */
    def setName( self, name):
        self.Name = name
        
    

    # gets the name of the table */
    def getName(self):
        return  self.Name
        

   
        
            


    ##/** set the specials of the table */
    def setSpecials(self,s):
        self.Specials =s
    

##/** gets the specials of the table */
    def getSpecials(self):
        return  self.Specials




##/**
## * Get the value of AktivesLoeschen.
## * @return *value of AktivesLoeschen.
## */
##bool def isAktivesLoeschen() {
##  return AktivesLoeschen;
##    }

##/**
## * Set the value of AktivesLoeschen.
## * @param v  Value to assign to AktivesLoeschen.
## */
##void def setAktivesLoeschen(bool  v) {
##  AktivesLoeschen = v ;
##    }



##/**
## * Get the value of StandardQuery.
## * @return *value of StandardQuery.
## */
##std::string def getStandardQuery() {
##  return StandardQuery;
##    }

##/**
## * Set the value of StandardQuery.
## * @param v  Value to assign to StandardQuery.
## */
##     void def setStandardQuery(std::string  v) {
##  StandardQuery .assign(v);
##    }


##/**
## * Get the value of NumberOfOverviewColumn.
## * @return value of NumberOfOverviewColumn.
## */
##int def getNumberOfOverviewColumn() {getElementsByTagName("name")
      
##  return numberOfOverviewColumn;
##    }

##/**
## * Set the value of NumberOfOverviewColumn.
## * @param v  Value to assign to NumberOfOverviewColumn.
## */
##     void def setNumberOfOverviewColumn(int  v) {
##  numberOfOverviewColumn = v ;
##    }



##/**
## * Get the value of nameOfIDField.
## * @return value of nameOfIDField.
## */
##     std::string def getNameOfIDField() {
##  return nameOfIDField;
##    }

##/**
## * Set the value of nameOfIDField.
## * @param v  Value to assign to nameOfIDField.
## */
##     void def setNameOfIDField(std::string  v) {
##  nameOfIDField .assign(v);
##    }



##    // Normal = Mysql = 3

##/**
## * Get the value of SqlDialekt.
## * @return value of SqlDialekt.
## */
##     int def getSqlDialekt() {
##  return SqlDialekt;
##    }

##/**
## * Set the value of SqlDialekt.
## * @param v  Value to assign to SqlDialekt.
## */
##     void def setSqlDialekt(int  v) {
##  SqlDialekt = v ;
##    }





##/**
## * Get the value of MandantenIdVorhanden.
## * @return value of MandantenIdVorhanden.
## */
##     bool def isMandantenIdVorhanden() {
##  return MandantenIdVorhanden;
##    }

##/**
## * Set the value of MandantenIdVorhanden.
## * @param v  Value to assign to MandantenIdVorhanden.
## */
##     void def setMandantenIdVorhanden(bool v) {
##  MandantenIdVorhanden = v;
##    }



##/**
## * Get the value of NameOfForeignKey.
## * @return value of NameOfForeignKey.
## */
    def getForeignKey(sName):
        return self.ForeignKey[sName];


##/**
## * Set the value of NameOfForeignKey.
## * @param v  Value to assign to NameOfForeignKey.
## */
    def setNameOfForeignKey(sName, sValue):
        self.ForeignKey[sName] = sValue
        
        


##/**
## * Get the value of Columns.
## * @return value of Columns.
## */
##     std::vector<cyr_column> def getColumns() {
##  return Columns;
##    }


##/**
## * Set the value of Columns.
## * @param v  Value to assign to Columns.
## */
##     void def setColumns(std::vector<cyr_column>  v) {
##   // Columns = v;
##    }

##/**
## * Add a cyr_column to Columns.
## * @param v  Value to add cyr_column to Columns.
## */

    def addColumn(self,  di_column) :
        self.Columns.append(di_column)
        
     


## * get a cyr_column from Columns at index.
## * @param i  Value to get a cyr_column from Columns at index i.
## */
    def getColumnAtIndex( i1):
        return self.Columns[i1]
        


    def getCountOfColumns(self):
        return len(self.Columns)


    def getColumns(self):
        #print 'Anzahl = '
        #print self.getCountOfColumns()
        return self.Columns

    
    
##    cyr_column SingleColumn = *(Columns.begin()+i1) ; 
  
 
##    return SingleColumn;
##}

##/**
## * delete a cyr_column from Columns at index.
## * @param i  Value to get a cyr_column from Columns at index i.
## */
##void def deleteColumnAtIndex(int i) {


##    Columns.erase(Columns.begin() + i);
##}


##/**
## * Get the value of CountOfColumns
## * @return value of CountOfColumns.
## */
##int def getCountOfColumns() {

##    return Columns.size();
##}
