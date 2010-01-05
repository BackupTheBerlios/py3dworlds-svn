#!/usr/bin/env python
# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

class cyr_column:

    def __init__(self):
        self.Name = "EMPTY"
        self.nameOfVariable = "EMPTY"
        self.sizeOfDatafield = '0'
        self.Type = None
        self.defaultValue = None
        
    
    # set the name of the column */
    def setName(self, s):
        self.Name = s 
        self.nameOfVariable = "e_" + s 
	


    # gets the name of the column */
    def getName(self):
        return self.Name 


    ### set the fieldspezification for the column */
    def setType(self, s):
        self.Type = s


    ### gets the field-spec. */
    def getType(self):
        return self.Type



    ## # gets the Size of the field */
    def getSizeOfDatafield(self):
        return self.sizeOfDatafield


    ##  # set the fieldsisze for the column */
    def setSizeOfDatafield(self, sSize):
        self.sizeOfDatafield = sSize



### if true, the "NULL" value can be inserted */
    def setAllowNull(self, b):
        self.allowNull = ~ b


### gets true, if "NULL" can be inserted */
    def isAllowNull(self):
        return self.allowNull


### the name of the column with the primary key */
    def setPrimaryKey(self, s):
        self.primaryKey = s

### gets the name of the column with the primary key */
    def getPrimaryKey(self):
        return self.primaryKey


### set the default value */
    def setDefaultValue(self, s=None):
        self.defaultValue = s

### get the default value */
    def getDefaultValue(self):
        return self.defaultValue


        
        
### set the extras */
##void def setExtras(std::string s)
##	Extras.assign(s);

### gets the extra definition */
##std::string def getExtras()
##	return Extras;



##int  def getColumnID()
##    return columnID;


##void def setColumnID(int i)
##    columnID = i;


##  std::string  def getNameOfVariable()
##      return nameOfVariable;


##void def setNameOfVariable(std::string s)
##  if(s.length() != 0)
##    nameOfVariable.assign(s);
  
	


##  std::string  def getTypeOfVariable()
##      return typeOfVariable;


##  void def setTypeOfVariable(std::string s)
##      typeOfVariable.assign(s);
	


##  int def getMaxLengthOfVariable()
##      return maxLengthOfVariable;


##  void def setMaxLengthOfVariable(int i)
##      maxLengthOfVariable = i;
  

  
