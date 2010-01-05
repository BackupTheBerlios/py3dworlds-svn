# -*- coding: utf-8 -*-

##Copyright (C) [2002]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

from twisted.web import xmlrpc
import os
import sys
import time
import random   
import xmlrpclib
import pg 
import string

from basics import basics

class SQL(xmlrpc.XMLRPC, basics):
    def __init__(self):
        basics.__init__(self)
 
    def xmlrpc_executeNormalQuery(self, cSql, dicUser={'Name':'griddata', 'SessionID':'0'}):
        #print "Start ExecuteQuere"
       
        conn = None
        dicResult = None
        rows = None
        #print dicUser
        #print cSql
        sUser =dicUser['Name']
        print 'sUser = ',  sUser
        try:
            self.out('execute SQL = ' + `cSql`)
            
            
            #self.writeLog('User = ' + sUser)
            #DSN = 'dbname=cuon host=localhost user=' + sUser
            conn = pg.connect(dbname = 'griddata',host = self.POSTGRES_HOST, port = self.POSTGRES_PORT, user = sUser)
            #conn = pg.connect(dbname = 'cuon',host = self.POSTGRES_HOST, user = sUser)
            #curs.execute(cSql.decode('utf-8'))
            #conn = libpq.PQconnectdb(dbname='cuon',host = 'localhost', user = sUser)
            print "conn = ",  conn
            try:
                                       
                rows = conn.query(cSql.encode('utf-8'))
                #self.writeLog('return from database = ' + `rows`)
            except:
                rows = 'ERROR'
        except:
            pass
            
            
        if rows and rows not in ['NONE','ERROR']:
            try:
                dicResult = rows.dictresult()
            except Exception, params:
                self.writeLog('try dic-Result')
                self.writeLog(`Exception`)
                self.writeLog(`params`)
                self.writeLog('----------------------------- dicResult should be None --------------')
                
                dicResult = None
        else :
            dicResult = 'NONE'
            
          
#        try:
#            #self.writeLog( '----------> SQL ')
#            #self.writeLog(cSql)
#            conn.close()
#            self.writeLog( '<-------SQL need : ' + ` time.mktime(time.localtime()) -t1` )
#        except Exception, params:
#            self.writeLog( 'executeQuery 3 ERROR = ' + `Exception` + ' ' + `params`)
#
#        #self.writeLog('sql return = ' + `dicResult`)
            
        return dicResult
     
        
    def xmlrpc_getListEntries(self, dicEntries, sTable, sSort, sWhere="", dicUser={}, bDistinct=False):
        #print 'start xmlrpc_getListEntries'
        
        import string
        import time
        
        if sWhere == None:
            sWhere = ''
        print 'table = ', sTable
        ok = False
        
        for cModul in self.liModules:
            if not ok:
                for li in self.dicLimitTables[cModul]['list']:
                    if li == sTable:
                        ok = True
                        self.LIMITSQL = self.dicLimitTables[cModul]['limit']
                        
        
        #dicEntries['status'] = 'string'
        if bDistinct:
            sSql = 'select distinct '
        else:
            sSql = 'select '
        liTable = []
        try:    
            #print 'replace id with table.id'
            del dicEntries['id']
            dicEntries[sTable + '.id'] = 'int'
        except Exception, params:
            #print Exception, params
            pass
        for i in dicEntries.keys():
            if dicEntries[i] == 'date':
                sSql = sSql + "to_char(" + i + ",  \'" + self.DIC_USER['SQLDateFormat'] + "\') as " + i  + ', '
            elif dicEntries[i] == 'time':
                sSql = sSql + "to_char(" + i + ",  \'" + self.DIC_USER['SQLTimeFormat'] + "\') as " + i  + ', '
            elif dicEntries[i] == 'datetime':
                sSql = sSql  + "to_char(" + i +", \'" + self.DIC_USER['SQLDateTimeFormat'] + "\') as " + i  + ', '
            
            else:
              sSql = sSql + i + ', '
            if i.find('.') > 0:
                liTable.append(i[:i.find('.')])
            
                
        #print liTable
        sSql = sSql[0: string.rfind(sSql,',') ]
        #self.writeLog('sWhere =' + `sWhere`)
        
        sWhere = self.getWhere(sWhere, dicUser, Prefix=sTable + '.')
        
        
           
        sSql += ' from ' + sTable 
        #zComa = 0
        liTableNames = [sTable]
        for i in liTable:
            appendTablename = True
            for name in liTableNames:
                if i == name:
                   appendTablename = False 
            if appendTablename:
                sSql += ',' + i 
                liTableNames.append(i)
            #zComa += 1
        #if zComa > 0:
        #    sSql = sSql[0: string.rfind(sSql,',') ]
                
        sSql +=  ' ' + sWhere + ' order by ' + sSort
        
        
       
        #self.writeLog(`sSql`)
        sSql = sSql + ' LIMIT ' + `self.LIMITSQL`
        #print 'self.LIMITSQL', self.LIMITSQL
        sSql = sSql.replace('specialsql1','where')
        #print sSql
        
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        #result2 = []
        #for li in result:
        #
        #    if string.strip(unicode(li['status'])) != unicode('delete'):
        #        result2.append(li)
        #        self.writeLog(string.strip(`li['status']`))
         
            
                
        
        #self.writeLog(repr(result))
        
        return result
        
    def xmlrpc_loadRecord(self, nameOfTable, record, dicUser , dicColumns):
        import string 
        sSql = 'select '
        
        for i in dicColumns.keys():
           if dicColumns[i] == 'date':
              sSql = sSql  + "to_char(" + i +", \'" + self.DIC_USER['SQLDateFormat'] + "\') as " +i  + ', '
           elif dicColumns[i] == 'time':
              sSql = sSql  + "to_char(" + i +", \'" + self.DIC_USER['SQLTimeFormat'] + "\') as " + i  + ', '
           elif dicColumns[i] == 'timestamp':
              sSql = sSql  + "to_char(" + i +", \'" + self.DIC_USER['SQLDateTimeFormat'] + "\') as " + i  + ', '
         
           else:
              sSql = sSql + i + ', ' 
        
        sSql = sSql[0: string.rfind(sSql,',') ]
        sSql = sSql + " from " + nameOfTable + " where id = " + `record`
        
        result = self.xmlrpc_executeNormalQuery(sSql,dicUser)
        
       
           
        return result
           
    def xmlrpc_saveRecord(self, sNameOfTable='EMPTY', id=0, dicValues ={}, dicUser={}, liBigEntries='NO'):       
        import string
        import types
        dicValues['client'] = [dicUser['client'], 'int']
##        if liBigEntries != 'NO':
##            for lb in liBigEntries:
##                sKey = dicUser['Name'] + '_' + lb
##                self.writeLog('sKey in Entries' + `sKey`)
##                dicValues[lb][0] = self.getValue(sKey)
##        
        self.writeLog('begin RECORD2 id = ' + `id`)
        if id > 0:
            # update
            self.writeLog('start Update')
            sSql = 'update ' + sNameOfTable + ' set  '
            
            for i in dicValues.keys():
                sSql = sSql + i
                liValue = dicValues[i]
                if liValue[1] == 'string' or liValue[1] == 'varchar':
                    sSql = sSql  + " = \'" + liValue[0]+ "\', "
        
                elif liValue[1] == 'int':
                    sSql = sSql  + " =  " + `int(liValue[0])` + ", "
        
                elif liValue[1] == 'float':
                    sSql = sSql  + " = " + `float(liValue[0])` + ", "
        
                elif liValue[1] == 'date':
                    if len(liValue[0]) < 6:
                        sSql = sSql  + " = NULL, "
                    else:
                        sSql = sSql  + " = \'" + liValue[0]+ "\', "
        
                elif liValue[1] ==  'bool':
                    self.writeLog('REC2-bool ')
                    if liValue[0] == 1:
                        liValue[0] = 'True'
                    if liValue[0] == 0:
                        liValue[0] = 'False'
                    sSql = sSql + " = " + liValue[0] + ", "
                else:
                    sSql = sSql  + " = \'" + liValue[0]+ "\', "
            
            sSql = sSql[0:string.rfind(sSql,',')]
        
            sSql = sSql + ' where id = ' + self.convertTo(id, 'String')
            self.writeLog('Update SQL = ' + sSql)
            
        else:
            self.writeLog('new RECORD2')
            sSql = 'insert into  ' + sNameOfTable + ' (  '
            sSql2 = 'values ('
            self.writeLog('REC2-1 ' + `sSql` + `sSql2`)
            for i in dicValues.keys():
                sSql = sSql + i + ', '
                self.writeLog('REC2-1.1 ' + `sSql`)
                liValue = dicValues[i]
                #self.writeLog('REC2-1.2 ' + `liValue`)
                #print "recValue = " ,  liValue
                if liValue == None :
                    sSql2 = sSql2 + "\'\', " 
                else:
                    if liValue[1] ==  'string' or liValue[1] == 'varchar':
                        if len(liValue[0]) == 0:
                            sSql2 = sSql2 + "\'\', " 
                        else:
                            sSql2 = sSql2  + "\'" + liValue[0] + "\', "
                        self.writeLog('REC2-2 ' + `sSql` + `sSql2`)
                    elif liValue[1] == 'int':
                        sSql2 = sSql2  + `int(liValue[0])` + ", "
                        self.writeLog('REC2-3 ' + `sSql` + `sSql2`)
                    elif liValue[1] == 'float':
                        sSql2 = sSql2  + `float(liValue[0])` + ", "
                        self.writeLog('REC2-4 ' + `sSql` + `sSql2`)
                    elif liValue[1] == 'date':
                        if len(liValue[0]) < 6:
                            sSql2 = sSql2  +  " NULL, "
                        else:
                            sSql2 = sSql2  + " \'" + liValue[0] + "\', "
                            self.writeLog('REC2-5 ' + `sSql` + `sSql2`)
                    elif liValue[1] ==  'bool':
                        #self.writeLog('REC2-bool ')
                        if liValue[0] == 1:
                           liValue[0] = 'True'
                        if liValue[0] == 0:
                           liValue[0] = 'False'
        
                        sSql2 = sSql2  +"\'" + liValue[0] + "\', "
                        #self.writeLog('REC2-6 ' + `sSql` + `sSql2`)
                    else:
                        sSql2 = sSql2  +  " \'" + liValue[0] + "\', "
                        #self.writeLog('REC2-6 ' + `sSql` + `sSql2`) 
             
                        
            self.writeLog('REC2-10 ' + `sSql` + '__' + `sSql2`) 
            sSql = sSql + 'id, user_id, status'
            sSql2 = sSql2 + 'nextval(\'' + sNameOfTable + '_id\'), current_user, \'create\''  
            
            # set brackets and add
            sSql = sSql + ') ' + sSql2 + ')'
        
        # execute insert
        self.writeLog('First SQL by RECORD2 = ' + `sSql`)
        #print sSql
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        self.writeLog(result)
        
            
        
        
        # find last id 
        if id < 0:
        # insert
            try:
                sSql = 'select last_value from ' + sNameOfTable + '_id'
                result = self.xmlrpc_executeNormalQuery(sSql,dicUser)
                id = result[0]['last_value']
            except:
                id = 0
        
        # sSql = sSql[0:string.rfind(sSql,',')]
             
        print "id by save record = ",  id 
        return  id 
        
        
    def xmlrpc_createBigRow(self, sFile, data, j, dicUser=None):
        debug = 1
        ok = 1
        #self.writeLog('createBigRow reached', debug)
        #self.writeLog('first j = ' + `j`,debug)
        
        sKey = dicUser['Name'] +'_' +sFile
        
        #self.writeLog(sKey, debug)
        if j == 0:
            #self.writeLog('j = ' + `j`, debug)
            self.saveValue(sKey,data)
        else:
            #self.writeLog('j = ' + `j`, debug)
            sData =  self.getValue(sKey)
            if sData not in ['NONE','ERROR']:
                #self.writeLog('len sData = ' + `len(sData)`, debug)
                sData = sData + data
            else:
                sData = data
                
            
            self.saveValue(sKey,sData)
        
        return ok
        
    def xmlrpc_deleteRecord(self,nameOfTable = 'EMPTY', record = -1, dicUser=None):
        sSql = "delete from " + nameOfTable + " where id = " + `record`
        return self.xmlrpc_executeNormalQuery(sSql, dicUser)
    def xmlrpc_loadCompeteTable(self, nameOfTable, dicUser):
        sSql = "select * from " + nameOfTable
        return xmlrpc_executeNormalQuery(sSql, dicUser)


    
