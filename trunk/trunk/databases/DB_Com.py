from twisted.web import xmlrpc
import os
import sys
import time
import types
import random   
import xmlrpclib
import string
from basics import basics
from SQL import SQL
from ConfigParser import ConfigParser



class DB_Com(xmlrpc.XMLRPC, SQL):
    def __init__(self):
        basics.__init__(self)
        SQL.__init__(self)
        
    def xmlrpc_is_running(self):
        return 12
        
    def getValue(self, sKey):
        v = 'NONE'
        sSql = "select svalue from cuon where skey = '" + sKey + "'"
        result = self.xmlrpc_executeNormalQuery(sSql)
        #print 'get-Value = ', result
        if result not in ['NONE','ERROR']:
           try:
              v = result[0]['svalue']
           except:
              v = 'NONE'
        if not v:
            v = 'NONE'
            
        return v
    def saveValue(self, sKey, cKey):
        #self.out('py_saveValue cKey = ' + cKey)
        sSql = "select skey from cuon where skey = '" + sKey + "'"
        #self.out('py_saveValue sSql = ' + `sKey`)
        result = self.xmlrpc_executeNormalQuery(sSql)
        #self.out('py_saveValue result = ' + `result`)
        if result not in ['NONE','ERROR']:
           sSql = "update cuon set svalue = '" + cKey +"' where skey = '" + sKey + "'"
        else:
           sSql = "insert into cuon (skey, svalue) values ('" + sKey + "','" + cKey +"')"
        #self.out('py_saveValue sSql = ' + `sSql`)
        result = self.xmlrpc_executeNormalQuery(sSql)
        return result

    def xmlrpc_createPsql(self, sDatabase, sHost, sPort, sUser,  sSql):

        # os.system('pysql ' + '-h ' + sHost + '-p ' + sPort + ' -U ' + sUser + ' ' + sDatabase + ' < ' + sSql) 
        oFile = open('/etc/cuon/run.sql', 'w')
        oFile.write(sSql)
        oFile.close()
        
        sysCommand =  'psql  ' + '-h ' + sHost + ' -p ' + sPort + ' -U ' + sUser +   ' '  + sDatabase + ' < /etc/cuon/run.sql'
        
        os.system(sysCommand)
        
        
        return sysCommand

#context.exSaveInfoOfTable(sKey, oKey )
    
    def checkUser(self, sUser, sID, userType = None):
        ok = None
        dSession = {}
        #print sUser, userType
        if userType:
           if userType == 'cuon':
                try:
                    #dSession['SessionID'] = self.dicVerifyUser[sUser]['SessionID']
                    #dSession['endTime'] = self.dicVerifyUser[sUser]['endTime']
                    #--dSession['SessionID'] = self.getValue('user_' + sUser + '_Session_ID')
                    #--dSession['endTime'] = float(self.getValue('user_' + sUser + '_Session_endTime'))
                    self.openDB()
                    dSession['SessionID'] = self.loadObject('user_' + sUser + '_Session_ID')
                    dSession['endTime'] = float(self.loadObject('user_' + sUser + '_Session_endTime'))
                    self.closeDB()
                    #print 'dSession', dSession
                    
                    if sID == dSession['SessionID'] and self.checkEndTime(dSession['endTime']):
                        ok = sUser
                except:
                    #dSession['SessionID'] = self.getValue('user_' + sUser + '_Session_ID')
                    #dSession['endTime'] = float(self.getValue('user_' + sUser + '_Session_endTime'))
                    #self.out('py_checkUser dSession is found')
                    ok = 'zope'
                    
        #self.out('Session = ' + `dSession`)
##        if dSession:
##            if sID == dSession['SessionID'] and self.checkEndTime(dSession['endTime']):
##                ok = sUser
##        
##        self.out('end checkUser ok = ' + `ok`)
        return ok
        
    def authenticate(self, name, password, request):
        ok = False
        cParser = ConfigParser()
        cParser.read(self.CUON_FS + '/user.cfg')
        sP = cParser.get('password',name)
        #self.writeLog('Password = ' + sP )
        if sP.strip() == password.strip():
            ok = True
            
        return ok
        
    def xmlrpc_createSessionID(self, sUser, sPassword):
        #self.out('1 -- createSessionID start')
        s = ''
        
        
        if self.authenticate(name=sUser,password=sPassword,request=None):
            #self.out('2 -- createSessionID User found ')
            s = self.createNewSessionID()
            #self.out('3 -- createSessionID id created for ' + sUser + ' = '  + `s`)
            self.openDB()
            self.saveObject('user_'+ sUser + '_Session_ID' , s['SessionID'])
            self.saveObject('user_'+ sUser + '_Session_endTime' , `s['endTime']`)
            dicUserACL = self.getUserAcl(sUser) 
            self.saveObject('user_'+ sUser + '_dicUserACL' , dicUserACL)
            try:
                f = open('/var/log/cuonlogin.log','a')
                f.writeline ( `time.strftime('%Y-%m-%d %H:%M:%s')` +' LOGIN: ' + sUser +'\n')
                f.close()
            except:
                pass
                
            #--self.saveValue('user_'+ sUser + '_Session_ID' , s['SessionID'])
            #--self.saveValue('user_'+ sUser + '_Session_endTime' , `s['endTime']`)
            #context.exSaveInfoOfTable('user_' + sUser , s)
            #self.out('4 -- createSessionID User is write ')
            
            #self.dicVerifyUser[sUser] = {}
            #self.dicVerifyUser[sUser]['SessionID'] = s['SessionID']
            #self.dicVerifyUser[sUser]['endTime'] = `s['endTime']`
            self.closeDB()
        else:
            self.out('createSessionID User not found')
        if not s.has_key('SessionID'):
            s['SessionID'] = 'TEST'
        self.out('createSessionID ID = ' + `s`)
        
        return s['SessionID']
    def getUserAcl(self, sUser):
        dicUserACL = {}
        
        return dicUserACL
        
    def xmlrpc_checkVersion(self, VersionClient, version):
        ok = 'O.K.'
        print version
        print VersionClient
        if version['Major'] != VersionClient['Major'] or version['Minor'] != VersionClient['Minor'] or version['Rev'] != VersionClient['Rev']:
            ok = 'Wrong'

        return ok
    def testMulti(self, value):
        return   value[0] * value[1]

    def xmlrpc_getLastVersion(self):
        self.writeLog('Start check version')
        id = 0
        version = '0.0.0'
        dicUser={'Name':'zope'}
        sSql = 'select last_value from cuon_clients_id'
        #self.writeLog('Start check version sql= ' + `sSql`)
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        self.writeLog('LastVersion = ' + `result`)
            
        if result not in ['NONE','ERROR']:
            try:
                id = int(result[0]['last_value'])
            except:
                id = -1
        else:
           id = -1
        if id == -1:
           version = '0.0.0'
        else:
           sSql = 'select version from cuon_clients where id = ' + `id`
           result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
           
           if result not in ['NONE','ERROR']:
               version = result[0]['version']
        liVersion = version.split('.')
        print liVersion
        dicVersion = {'Major':int(liVersion[0]),'Minor':int(liVersion[1]), 'Rev':int(liVersion[2])}
        self.writeLog('check version id, version = ' + `id` + ', ' + `dicVersion` )  
        return id, dicVersion
    def xmlrpc_getInfo(self, sSearch):
        return self.getValue(sSearch)
    def xmlrpc_saveInfo(self, sKey, cKey):
        return self.saveValue(sKey, cKey)
    
    def xmlrpc_getListOfClients(self, dicUser):
        #self.writeLog('Start List Of Clients')
        sSql = "select id from clients"
        dicClients = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        liClients = []
        #self.writeLog('Clients = ' + `dicClients`)

        if dicClients not in ['NONE','ERROR']:
           for i in dicClients:
              self.writeLog('i = ' + `i`)
              cli = i['id']
              self.writeLog('cli = ' + `cli`)
              
              liClients.append(cli)
        
        #self.writeLog('liClients = ' + `liClients`)
        return liClients
    
    def xmlrpc_checkExistSequence(self, sName, dicUser):

        sSql = "select relname from pg_class where relname = '" + sName + "'"
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        ok = 0

        if dicName not in ['NONE','ERROR']:
            ok = len(dicName)

        return  ok
        
    
    def xmlrpc_checkExistTable(self, sName, dicUser):
        sSql = "select tablename from pg_tables where tablename = '" + sName + "'"
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        ok = 0

        if dicName not in ['NONE','ERROR']:
            try:
                ok = len(dicName)
            except:
                ok = 0

        return  ok
        
    def xmlrpc_checkExistColumn(self, sTableName, sColumnName, dicUser):
        sSql =  "select attname from pg_attribute where attrelid = ( select relfilenode from pg_class where relname = '" + sTableName +"')" 
        
        # and atttypmod != -1 )"
        
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        ok = 0
        print `dicName`
        
        for i in range(len(dicName)):
            print dicName[i]['attname']
            if sColumnName == dicName[i]['attname']:
               ok = 1
    

        return ok
        
    def xmlrpc_checkTypeOfColumn(self, sTable, sColumn, sType, iSize, dicUser ):
        sColumn = sColumn.lower()
        bCheck = 0
        sSql = "select typname from pg_type where pg_type.oid = (select atttypid from pg_attribute where attrelid = (select relfilenode from pg_class where relname = \'"
        
        sSql = sSql + sTable + "\') and attname = \'" + sColumn+ "\' ) "
        
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser )
        #print result
        try: 
            print('types by ColumnCheck: ' + `result[0]['typname']` + ' ### ' + `sType`)
        except:
            pass 
        try:    
            if string.find(result[0]['typname'],sType) > -1 :
               self.writeLog( 'type is equal')
               if string.find(sType,'char') > -1:
                  result2 = self.xmlrpc_getSizeOfColumn(sTable, sColumn, dicUser)
                  self.writeLog( 'Size =' + `result2[0]['atttypmod'] -4` + ', ' +  `int(iSize)`)
                  if (result2[0]['atttypmod'] -4) == int(iSize):
                     bCheck = 1
               else:
                  bCheck = 1
        except:
                bCheck = 0
        return bCheck
    
    def xmlrpc_getSizeOfColumn(self, sTable, sColumn, dicUser):
        sSql = "select pg_attribute.atttypmod from pg_attribute where  attrelid = (select relfilenode from pg_class where relname = \'" + sTable + "\') and attname = \'" + sColumn + "\'"
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        return result


    def xmlrpc_logout(self, sUser):
        ok = True
        self.openDB()
        self.saveObject('user_'+ sUser + '_Session_ID' , 'TEST')
        self.saveObject('user_'+ sUser + '_Session_endTime' , '0')
        self.closeDB()    
        #self.saveValue('user_' + sUser,{'SessionID':'0', 'endTime': 0})
        try:
            f = open('/var/log/cuonlogin.log','a')
            f.writeline ( `time.strftime('%Y-%m-%d %H:%M:%s')` +' LOGOUT: ' + sUser +'\n')
            f.close()
        except:
            pass
        return ok 
    def xmlrpc_createGroup(self, sGroup, dicUser):
        # check the group
        
        sSql = "select groname from pg_group where groname = '" + sGroup + "'"
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        
        if dicName not in ['NONE','ERROR']:
           ok = 'Group exists'
        else:
           sSql = 'CREATE GROUP ' + sGroup
           ok = self.xmlrpc_executeNormalQuery(sSql,dicUser )
        
        return ok
        
    def xmlrpc_createUser(self, sUser, sPassword,  dicUser, createDBUser=1):
        ok = 'No action'
        if createDBUser:
            # check the user
            
            sSql = "select usename from pg_user where usename = '" + sUser + "'"
            dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
            
            if dicName not in ['NONE','ERROR']:
               ok = 'User exists'
            else:
               sSql = 'CREATE USER ' + sUser
               ok = self.xmlrpc_executeNormalQuery(sSql, dicUser)
            
        # context.Cuon.src.Databases.py_saveValue('user_'+ sUser, sPassword)
        
        return ok

    def xmlrpc_addGrantToGroup(self, sGrants, sGroup, sTable, dicUser):
        # check the group
        ok = 'ERROR'
        
        sSql = "select groname from pg_group where groname = '" + sGroup + "'"
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        if dicName not in ['NONE','ERROR']:
           ok = 'GROUP'
           sSql = 'Grant ' +sGrants + ' ON '  + sTable + ' TO GROUP ' + sGroup
           ok = self.xmlrpc_executeNormalQuery(sSql, dicUser)
         
        
        else:
           ok = 'Group does not exist'
        
        return ok
    def xmlrpc_addUserToGroup(self, sUser, sGroup, dicUser):
        
        # check the user
        self.writeLog(dicUser['Name'])
        self.writeLog(dicUser['SessionID'])
        
        sSql = "select usename from pg_user where usename = '" + sUser + "'"
        dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        ok = 'ERROR'
        if dicName not in ['NONE','ERROR']:
           # check the group
           sSql = "select groname from pg_group where groname = '" + sGroup + "'"
           dicName = self.xmlrpc_executeNormalQuery(sSql, dicUser)
           ok = 'USER'
           if dicName not in ['NONE','ERROR']:
              ok = 'GROUP'
              sSql = 'ALTER GROUP ' +sGroup + ' ADD USER ' + sUser
              ok = self.xmlrpc_executeNormalQuery(sSql, dicUser)
         
        
        else:
           ok = 'Group or User does not exist'
        
        return ok
        
    def xmlrpc_createCuon(self, dicUser):
        
        self.writeLog('start py_createCuon')
        retValue = True
        ok = self.xmlrpc_checkExistTable('cuon', dicUser)
        self.writeLog('py_createCuon1 ' + `ok`)
        if ok == 0:
           retValue = False
           sSql = 'create table cuon ( skey varchar(255) NOT NULL UNIQUE , svalue text NOT NULL, PRIMARY KEY (skey) )'
           ok = self.xmlrpc_executeNormalQuery(sSql, dicUser)
           sSql = 'GRANT ALL ON  cuon TO PUBLIC'
           ok = self.xmlrpc_executeNormalQuery(sSql, dicUser)
           
        return retValue
        
        
    def saveWebshopRecord(self, sNameOfTable='EMPTY', id=0, id_field='id', dicValues ={}, dicUser={}):
        import string
        import types
        
        context.logging.writeLog('begin RECORD2')
        dicUser['Database'] = 'osCommerce'
        
        if id > -1:
            # update
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
                    if len(liValue[0]) < 10:
                        sSql = sSql  + " = NULL, "
                    else:
                        sSql = sSql  + " = \'" + liValue[0]+ "\', "
        
                elif liValue[1] ==  'bool':
                    context.logging.writeLog('REC2-bool ')
                    if liValue[0] == 1:
                        liValue[0] = 'True'
                    if liValue[0] == 0:
                        liValue[0] = 'False'
                    sSql = sSql + " = " + liValue[0] + ", "
                else:
                    sSql = sSql  + " = \'" + liValue[0]+ "\', "
            
            sSql = sSql[0:string.rfind(sSql,',')]
        
            sSql = sSql + ' where ' + id_field + ' = ' + `id`
            #print sSql
        else:
            context.logging.writeLog('new RECORD2')
            sSql = 'insert into  ' + sNameOfTable + ' (  '
            sSql2 = 'values ('
            context.logging.writeLog('REC2-1 ' + `sSql` + `sSql2`)
            for i in dicValues.keys():
                sSql = sSql + i + ', '
                context.logging.writeLog('REC2-1.1 ' + `sSql`)
                liValue = dicValues[i]
                context.logging.writeLog('REC2-1.2 ' + `liValue`)
                if liValue == None :
                    sSql2 = sSql2 + "\'\', " 
                else:
                    if liValue[1] ==  'string' or liValue[1] == 'varchar':
                        if len(liValue[0]) == 0:
                            sSql2 = sSql2 + "\'\', " 
                        else:
                            sSql2 = sSql2  + "\'" + liValue[0] + "\', "
                        context.logging.writeLog('REC2-2 ' + `sSql` + `sSql2`)
                    elif liValue[1] == 'int':
                        sSql2 = sSql2  + `int(liValue[0])` + ", "
                        context.logging.writeLog('REC2-3 ' + `sSql` + `sSql2`)
                    elif liValue[1] == 'float':
                        sSql2 = sSql2  + `float(liValue[0])` + ", "
                        context.logging.writeLog('REC2-4 ' + `sSql` + `sSql2`)
                    elif liValue[1] == 'date':
                        if len(liValue[0]) < 10:
                            sSql2 = sSql2  +  " NULL, "
                        else:
                            sSql2 = sSql2  + " \'" + liValue[0] + "\', "
                            context.logging.writeLog('REC2-5 ' + `sSql` + `sSql2`)
                    elif liValue[1] ==  'bool':
                        context.logging.writeLog('REC2-bool ')
                        if liValue[0] == 1:
                           liValue[0] = 'True'
                        if liValue[0] == 0:
                           liValue[0] = 'False'
        
                        sSql2 = sSql2  +"\'" + liValue[0] + "\', "
                        context.logging.writeLog('REC2-6 ' + `sSql` + `sSql2`)
                    else:
                        sSql2 = sSql2  +  " \'" + liValue[0] + "\', "
                        context.logging.writeLog('REC2-6 ' + `sSql` + `sSql2`) 
             
                        
            context.logging.writeLog('REC2-10 ' + `sSql` + '__' + `sSql2`) 
            sSql = sSql[0:sSql.rfind(',')]
            sSql2 = sSql2[0:sSql2.rfind(',')]
            #sSql2 = sSql2 + 'nextval(\'' + sNameOfTable + '_id\'), current_user, \'create\''  
            
            # set brackets and add
            sSql = sSql + ') ' + sSql2 + ')'
        
            # execute insert
            context.logging.writeLog('SQL by RECORD2 = ' + `sSql`)
            #print sSql
            context.py_executeNormalQuery(sSql, dicUser)
        
            # find last id 
        
            sSql = 'select max(' + id_field + ') as last_value from ' + sNameOfTable 
            # sSql = sSql[0:string.rfind(sSql,',')]
        
            
        
        #print sSql
        #return printed
                   
        return context.py_executeNormalQuery(sSql,dicUser)
    def xmlrpc_saveZipPlanet(self, dicPlanet, dicUser):   
        print 'dicPlanet', dicPlanet
        sSql = "select id from planet where name = '" + dicPlanet['name'][0] + "'"
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        print 'zipPlanet 1', result
        if result == 'NONE':
            print 'zipPlanet 2', result
            result = self.xmlrpc_saveRecord('planet', -1, dicPlanet, dicUser, liBigEntries='NO') 
            print 'zipPlanet 3', result
        else:
            result = self.xmlrpc_saveRecord('planet', result[0]['id'], dicPlanet, dicUser, liBigEntries='NO')
            print 'zipPlanet 4', result
        return result
    def xmlrpc_saveZipCountry(self, dicCountry, dicUser):   
        print 'dicCountry', dicCountry
        sSql = "select id from country where name = '" + dicCountry['name'][0] + "'"
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        print 'zipCountry 1', result
        if result == 'NONE':
            print 'zipCountry 2', result
            result = self.xmlrpc_saveRecord('country', -1, dicCountry, dicUser, liBigEntries='NO') 
            print 'zipCountry 3', result
        else:
            result = self.xmlrpc_saveRecord('country', result[0]['id'], dicCountry, dicUser, liBigEntries='NO')
            print 'zipCountry 4', result
        return result
        
        
    def xmlrpc_saveZipState(self, dicState, dicUser):   
        print 'dicState', dicState
        sSql = "select id from country where short_name = '"+ dicState['country_id'][0] +"'"
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        dicState['country_id'][0] = result[0]['id']
        if int(dicState['country_id'][0]) > 0:
            sSql = "select id from states where name = '" + dicState['name'][0] +"'"
            result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
            print 'zipState 1', result
            if result == 'NONE':
                print 'zipState 2', result
                result = self.xmlrpc_saveRecord('states', -1, dicState, dicUser, liBigEntries='NO') 
                print 'zipState 3', result
            else:
                result = self.xmlrpc_saveRecord('states', result[0]['id'], dicState, dicUser, liBigEntries='NO')
                print 'zipState 4', result
            return result
        else:
            print 'No Country found'
        return result 
                
                
                
    def xmlrpc_saveZipCity(self, dicCity,dicZip, dicUser):  
         
        country_id = 0
        print 'dicCity', dicCity
        sSql = "select id from country where short_name = '"+ dicCity['country_id'][0] +"'"
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        if result not in ['NONE','ERROR'] and int(result[0]['id']) > 0:
            country_id = int(result[0]['id'])
        dicCity['country_id'][0] = country_id
        
        state_id = 0    
        sSql = "select id from states where state_short = '"+ dicCity['state_id'][0] +"' and country_id = " + `country_id` 
        result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        if result not in ['NONE','ERROR'] and int(result[0]['id']) > 0:
            state_id = int(result[0]['id'])
        dicCity['state_id'][0] = state_id
        ad_id = 0
        district_id = 0
        if country_id and state_id:
            if dicCity['ad_id'] != '-':
            
                sSql = "select id from administrative_district where state_id = " + `state_id` + " and name = '" + dicCity['ad_id'][0] + "'"
                result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
                if result not in ['NONE','ERROR'] and int(result[0]['id']) > 0:
                    ad_id = int(result[0]['id'])
                else:
                    dicAD = {}
                    dicAD['name'] = [dicCity['ad_id'][0],'string']
                    dicAD['state_id'] = [state_id,'int']
                    if result == 'NONE':
                        result = self.xmlrpc_saveRecord('administrative_district', -1, dicAD, dicUser, liBigEntries='NO') 
                    else:
                        result = self.xmlrpc_saveRecord('administrative_district', result[0]['id'], dicAD, dicUser, liBigEntries='NO')
                    
##                    sSql = "select id from district where state_id = ' + `state_id`
##                    result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
##                    if result != 'NONE' and int(result[0]['id']) > 0:
##                        ad_id = int(result[0]['id'])
##            if int(dicCity['country_id'][0]) > 0:
##                sSql = "select id from states where name = '" + dicCity['name'][0] +"'"
##                result = self.xmlrpc_executeNormalQuery(sSql, dicUser)
##                print 'zipCity 1', result
##                if result == 'NONE':
##                    print 'zipCity 2', result
##                    result = self.xmlrpc_saveRecord('states', -1, dicCity, dicUser, liBigEntries='NO') 
##                    print 'zipCity 3', result
##                else:
##                    result = self.xmlrpc_saveRecord('states', result[0]['id'], dicCity, dicUser, liBigEntries='NO')
##                    print 'zipCity 4', result
##                return result
        else:
            print 'No Country or state  found'
            print '___________________________'
        return result 
                        
    def bindSql(self, liFields ):
        #print 'bindSql start'
        sSql = ''
        for liValues in liFields:
            sSql += liValues[0] + ' as ' + liValues[1] + ', '
        
        
        sSql = sSql[0:sSql.rfind(',')]
        #print 'bindSql = ', sSql
        
        return sSql
        
            
    def xmlrpc_getInternInformation(self, dicUser, Pers1=None, Pers2=None):
        #print 'Pers1 = ', Pers1
        
        dicRet = {}
        sSql = "select *  from staff where id = " + self.getStaffID(dicUser)
        liResult = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        if liResult and liResult not in ['NONE','ERROR']:
            dicPers = liResult[0]
            for key in dicPers.keys():
                
                dicRet['userinfo_' + key] = dicPers[key]
                    
            
            
        if Pers1:
            sSql = "select * from staff where id = " + `Pers1`
            liResult = self.xmlrpc_executeNormalQuery(sSql, dicUser)
            if liResult and liResult not in ['NONE','ERROR']:
                dicPers = liResult[0]
                for key in dicPers.keys():
                    dicRet['person1_' + key] = dicPers[key]
                    
        if Pers2:
            sSql = "select * from staff where id = " + `Pers2`
            liResult = self.xmlrpc_executeNormalQuery(sSql, dicUser)
            if liResult and liResult not in ['NONE','ERROR']:
                dicPers = liResult[0]
                for key in dicPers.keys():
                    dicRet['person2_' + key] = dicPers[key]
        
        if not dicRet:
            dicRet = 'NONE'
        #print dicRet
        return dicRet
    def xmlrpc_checkUpdateID(self, sTable, sField, liValue, dicUser):
        updateID = 0
        sSql = 'select id from ' + sTable + ' where ' + sField + ' = '
        if  liValue[1] == 'string':
            sSql += "'" + liValue[0] + "'"
        else:
            sSql += `liValue[0]` 
        
        sSql += self.getWhere('',dicUser,2)
        liResult = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        print liResult
        if liResult and liResult not in ['NONE','ERROR']:
            updateID = liResult[0]['id']
            
        return updateID
        
    def xmlrpc_updateBank(self, dicUser):
        updateID = 0    
        sSql = "update bank set address_id = (select address.id from address, bank where bank.shortDesignation = address.status_info "
        sSql += self.getWhere('',dicUser,2,'bank.') + ')'
        liResult = self.xmlrpc_executeNormalQuery(sSql, dicUser)
        print liResult
        return True

    def xmlrpc_getDMSRights(self,sName):
        value = None
        rights = 'NONE'
        groups = 'NONE'
        try:
                       
            cpServer, f = self.getParser(self.CUON_FS + '/sql.ini')
            #print cpServer
            #print cpServer.sections()
            if sName == 'INVOICE':
                value = self.getConfigOption('DEFAULT_MODUL_RIGHTS_DMS','INVOICE', cpServer)
            elif sName == 'EMAIL':
                value = self.getConfigOption('DEFAULT_MODUL_RIGHTS_DMS','EMAIL', cpServer)
        
        except:
            pass
        if value:
            liS = value.split(',')
            if liS:
                try:
                    rights = liS[0]
                    groups = liS[1]
                    
                except:
                    pass
                    
        return rights,groups
        
    def xmlrpc_getDIC_USER(self):
        return self.DIC_USER
        
