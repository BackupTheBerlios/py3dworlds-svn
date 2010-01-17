# -*- coding: utf-8 -*-

##Copyright (C) [2003]  [Juergen Hamel, D-32584 Loehne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 


import SingleData, cyr_load_table, cyr_table, cyr_column
import cyr_load_entries
import xmlrpc.xmlrpc
import string
import cPickle
import sys, os
import codecs
import ConfigParser
from constants import constants
from basics import basics 
class databases(constants,  basics):
    """
    @author: Jürgen Hamel
    @organization: Cyrus-Computer GmbH, D-32584 Löhne
    @copyright: by Jürgen Hamel
    @license: GPL ( GNU GENERAL PUBLIC LICENSE )
    @contact: jh@cyrus.de
    """
    
    def __init__(self, servermod = False):
      
        constants.__init__(self)
        basics.__init__(self)
        # self.setLogLevel(self.INFO)
        self.allTables = {}
       
#        self.xml.signal_autoconnect({ 'on_close1_activate' : self.on_close1_activate} )
#        self.xml.signal_autoconnect({ 'on_dbcheck1_activate' : self.on_dbcheck1_activate} )
#        self.xml.signal_autoconnect({ 'on_load_defaults1_activate' : self.on_load_defaults1_activate} )

        self.rpc = xmlrpc.xmlrpc.myXmlRpc()
        
        print 'database:',  self.rpc.server
        
        
        # User auf zope setzen
        #self.oUser.setUserName('zope')
        #self.oUser.setUserPassword('test')
        
        self.dicUser = {'Name':'griddata'}
        # set to 0 for disable 'where client =  '
        self.dicUser['client'] = 0
        #self.DIC_USER = self.rpc.callRP('Database.getDIC_USER')
     
     
    def checkClient(self):
        pass
           
    def on_start_complete_update1_activate(self, event):
        print 'start complete Update'
        self.iPB = 1
        self.startProgressBar(Title='Complete Update')
        
        self.activateClick('dbcheck1')
        self.iPB = 35
        self.setProgressBar(self.iPB)
        
        self.activateClick('trigger1')
        self.iPB = 45
        self.setProgressBar(self.iPB)
        
        self.activateClick('grants1')
        self.iPB = 65
        self.setProgressBar(self.iPB)
        
        self.activateClick('load_defaults1')
        self.iPB = 85
        self.setProgressBar(self.iPB)
        
        self.activateClick('save_client1')
        self.iPB = 100
        self.setProgressBar(self.iPB)
        
        self.stopProgressBar()
        
        
    def on_save_client1_activate(self,event):

        liAllTables = cPickle.loads(eval(self.doDecode(self.rpc.callRP('Database.getInfo', 'allTables'))))

        print `liAllTables`
        
        try:
            clt = cuon.Databases.cyr_load_table.cyr_load_table()
            for lt in liAllTables:
                self.allTables[lt] =  clt.loadTable(lt)
        except Exception, param:
            print 'ERROR '
            print Exception
            print param
            
            
        sc = cuon.Databases.SingleCuon.SingleCuon(self.allTables)
        cpParser = ConfigParser.ConfigParser()
        f = file('version.cfg','r')
        cpParser.readfp(f)
        sFile = None
        try:
            
            n1 = cpParser.get('version', 'Name')
            v1 = cpParser.get('version', 'Major') + '.' + cpParser.get('version', 'Minor') + '.' + cpParser.get('version', 'Rev')
            sFile = cpParser.get('version', 'File')
        except Exception, param:
            print "Error read version-configfile" + `sFile`
            print Exception
            print param
        
        try:
            f = file(sFile,'rb')
            b = f.read()
            f.close()
            print 'Read by saveClient f = ', sFile
            print 'len = ', len(b)
            
            dicValues = {'name':[n1,'string'],'version' : [v1,'string'], 'clientdata':[b,'app']}
            sc.newRecord()
            sc.saveExternalData(dicValues,['clientdata'])

        except Exception, param:
            print "Error open Versionsfile " + `sFile`
            print Exception
            print param
 
        f.close()
        
                            
        
    
    def on_close1_activate(self, event):
        win1 = self.xml.get_widget('DatabasesMainwindow')
        win1.hide()


    def on_dbcheck1_activate(self, event):
        
      
        clt = cyr_load_table.cyr_load_table()
        ### for Server-functions set the td-object
        #clt.td = self.td
        tableList = []
        for key in self.nameOfXmlTableFiles.keys():
            print  "start check for : " + `key`
  
            lTable = clt.getListOfTableNames(self.nameOfXmlTableFiles[key])
            tableList = self.startCheck(key,lTable, tableList)
            print 'check finished - now create sequences'
            # Sequences !!
            lSequences = clt.getListOfSequenceNames(key)
            print 'Sequences'
            print `lSequences`
            
            # Sequences per client
            liClients = self.rpc.callRP('Database.getListOfClients', self.dicUser)
            print `liClients`
            for cli in liClients:
                for s in range(len(lSequences)):
                    seq = lSequences[s]
                    print 'seq 1 ' + seq
                    seq = seq + '_client_' + `cli`
                    lSequences[s] = seq
                    print 'seq 2 ' + seq
            print `lSequences`        
            self.startCheckSequences(key,lSequences)
           
        print 'allTables = '
        print tableList    
        #self.rpc.callRP('Database.saveInfo', 'allTables', self.doEncode(repr(cPickle.dumps(tableList) )))
        
        
    def on_trigger1_activate(self, event):
         print 'create procedures and trigger'
         
         self.createProcedureAndTrigger()
       
    def on_load_defaults1_activate(self, event):
        cle = cuon.Windows.cyr_load_entries.cyr_load_entries()
        self.out( 'before Key ')
        ### for Server-functions set the td-object
        cle.td = self.td
        for key in self.td.nameOfXmlEntriesFiles.keys():
            print 'xml = ' + key
            lEntry = cle.getListOfEntriesNames(key)
            for i in lEntry:
                self.out( i.toxml())
                sNameOfTable = key[6:(len(`key`) -7)]
                print  "sNameOfTable" , sNameOfTable 
                self.startXMLCheck(key,i , sNameOfTable)        


        print '----------------------------------------------- Glade-Files -------------------------------------------------------------------------'
        print '------------------------------------------------------------------------------------------------------------------------------------------'
        print '------------------------------------------------------------------------------------------------------------------------------------------'
        
        #save glade-files
        self.saveGladeFiles()       

        #save report-files
        self.saveReportFiles()       

        print '----------------------------------------------- Report files -------------------------------------------------------------------------'
        print '------------------------------------------------------------------------------------------------------------------------------------------'
        print '------------------------------------------------------------------------------------------------------------------------------------------'


    def on_grants1_activate(self, event):
        self.setGrants()


    def on_import_zipcode1_activate(self, event):
        self.fd.show()
        

    def on_fd_ok_button1_clicked(self,event):
        filename = self.fd.get_filename()
        self.out( filename)
        self.fd.hide()
        self.importZip(filename)
        
    def on_fd_cancel_button1_clicked(self,event):
        self.fd.hide()
            
    def on_import_generic1_activate(self,event):
        imf = cuon.Databases.import_generic1.import_generic1()

    def on_import_generic2_activate(self,event):
        imf = cuon.Databases.import_generic2.import_generic2()
       
        
    def startCheck(self, key, lTable, tableList):
 
        clt = cyr_load_table.cyr_load_table()
       ### for Server-functions set the td-object
        
        # first - the infotable cuon must be setup
        #print 'User:', self.dicUser
        #ok =  self.rpc.callRP('Database.createCuon', self.dicUser)

        # now check the rest
        
        for i in lTable:
            print 'tableDefinition = ' ,key,i
            table = clt.getTableDefinition(key,i)
            print '1---clt.savetable', table.getName()
            clt.saveTable(i,table )
            print '1+++++++++++++++++++++++++++++++++++++++++++++++++++'
            
            print '2---dbcheck', table.getName()
            self.dbcheck(table)
            print '2+++++++++++++++++++++++++++++++++++++++++++++++++++'
            
            print '3---List of tables', `tableList`
            tableList.append(table.getName())
            print '3--------------------------------------------------------------------------------------'
        return tableList

    def startCheckSequences(self, key, lSequences):
        print 'start check Sequences'
        clt = cyr_load_table.cyr_load_table()
       ### for Server-functions set the td-object
       
 
        for i in lSequences:
            print 'Check this Sequence = ' , `i`
            ok =  self.rpc.callRP('Database.checkExistSequence',i, self.dicUser)
            if ok == 0:
                print 'create Sequence'
                iSeq = i.upper().find('_CLIENT_')
                if iSeq > 0:
                    seqname =i[0:iSeq]
                else:
                    seqname = i
                dicSeq = clt.getSequenceDefinition(key, seqname)
                print dicSeq
                sSql = "create sequence " + i
                if dicSeq['increment']:
                    sSql = sSql + ' INCREMENT ' + dicSeq['increment']
                if dicSeq['minvalue']:
                    sSql = sSql + ' MINVALUE ' + dicSeq['minvalue']
                if dicSeq['maxvalue']:
                    sSql = sSql + ' MAXVALUE ' + dicSeq['maxvalue']
                if dicSeq['start']:
                    sSql = sSql + ' START ' + dicSeq['start']
                if dicSeq['cache'] != '0':
                    sSql = sSql + ' CACHE ' + dicSeq['cache']
                if dicSeq['cycle'] == 'Yes':
                    sSql = sSql + ' CYCLE ' 


                    
                self.out( sSql)
                print 'Sql Sequence = ', sSql
                result = self.rpc.callRP('Database.executeNormalQuery', sSql, self.dicUser)
        

##    def startCheckForeignKey(self, key, liForeign):
##        print 'start check Foreign'
##        clt = cyr_load_table.cyr_load_table()
##       ### for Server-functions set the td-object
##        clt.td = self.td
## 
##        for i in liForeign:
##            print 'Check this Foreign key = ' , `i`
##            dicForeign = clt.getForeignKeyDefinition(key, i)
##            # alter table partner ADD CONSTRAINT "f_address" foreign key (addressid) references address (id) on delete restrict on update restrict ;
##
##            sSql = 'alter table ' + dicForeign['table']
##            sSql += ' ADD CONSTRAINT "f_' + dicForeign['name'] +'" '
##            sSql += dicForeign['sql']
##            
##            self.out( sSql)
##            print 'Sql Sequence = ', sSql
##            result = self.rpc.callRP('Database.executeNormalQuery', sSql, self.dicUser)
##        


    def dbcheck(self, table):
        print "check Databases"
        #ok = self.rpc.callRP('src.Databases.py_packCuonFS')
        ok = self.rpc.callRP('Database.checkExistTable',table.getName(), self.dicUser)
        print  "Ok = " ,  `ok`
        
        if ok == 0:
            # create table
            self.createTable(table)
        
        self.checkColumn(table)
        

    def createTable(self, table):
        self.out( table.getName())
        self.out( table.getSpecials())

        sSql = 'create table ' + str(table.getName()) + ' () ' 
        
        if  table.getSpecials() :
               sSql = sSql + str(table.getSpecials())

        sSql1 = string.replace(sSql,';',' ')    
        self.out( sSql1)
        
        self.rpc.callRP('Database.executeNormalQuery',sSql1, self.dicUser)

        # create the sequence
        
        sSql1 = "create sequence " + str(table.getName()) +"_id " 
        self.out( sSql1)
   
        self.rpc.callRP('Database.executeNormalQuery',sSql1, self.dicUser)

 


    def checkColumn(self, table):
        
        for i in range(len(table.Columns)):
            co = table.Columns[i]
            self.out( ('Name OfColumn : ' + str(co.getName() ) ) )
            #print `self.dicUser`
            ok = self.rpc.callRP('Database.checkExistColumn',table.getName(), co.getName() , self.dicUser)
            self.out("column-ok = " + str(ok),1)
            
            if ok == 0:
                print "column-ok = " + str(ok) + ' , Column must be created' 

                # create Column
                print 'create Column ' + str(co.getName())
                self.createColumn(table, co)
            
            print 'Column exist, now check Column Type'
            ok = self.rpc.callRP('Database.checkTypeOfColumn',table.getName(), co.getName(), co.getType(), co.getSizeOfDatafield() , self.dicUser )

                
            self.out("column-ok = " +`co.getType()` + ', ' + ` co.getSizeOfDatafield()` + ', -- ' +  str(ok),1)
            print "column-ok = " +`co.getType()` + ', ' + ` co.getSizeOfDatafield()` + ', -- ' +  str(ok) 
            if ok == 0:
                print 'Column Type false, modify !'
                # change column
                self.modifyColumn(table, co)
            
#            if co.getName() == 'id':
#                print 'create unique index', table.getName()
#                sSql =  'create unique index index_' + table.getName() + '_id on ' + table.getName() + " (id)"
#                ok = self.rpc.callRP('Database.executeNormalQuery',sSql, self.dicUser)
#                
    def getSqlField(self,sSql, co):
        if (string.find(co.getType(), 'char' )>= 0 ) :
            # find char, so take size to it
            sSql = sSql + ' (' + str(co.getSizeOfDatafield()) +') '
        if (string.find(co.getType(), 'numeric' )>= 0 ) :
            # find numeric, so take size to it
            print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
            sSql = sSql + '(' + str(co.getSizeOfDatafield()) +') '    
        return sSql 
    def createColumn(self, table, co):
        self.out( co.getName())

        
        sSql = 'alter table ' + str(table.getName()) + ' add column  ' + co.getName() + ' ' + co.getType()
        sSql = self.getSqlField(sSql, co)
        print sSql
        print '----------------------------------------------------------------'
        if  co.isAllowNull()  == 0 :
            self.out( co.isAllowNull())
            sSql = sSql + ' not null '

        if co.getPrimaryKey() == 1:
            sSql = sSql + ' PRIMARY KEY '
            
        print sSql
        
        res = self.rpc.callRP('Database.executeNormalQuery',sSql, self.dicUser)

        if co.getDefaultValue():
            sSql = 'alter table ' + str(table.getName()) + ' alter column  ' + co.getName()
            sSql = sSql + " SET DEFAULT " + co.getDefaultValue()

            res = self.rpc.callRP('Database.executeNormalQuery',sSql, self.dicUser)
    
    #
    # start xml defaults, entries, etc.
    #

    def modifyColumn(self, table, co):
        #at this time to many problems with Postgres 
        #sSql = 'alter table ' + str(table.getName()) + ' alter column ' + co.getName() + ' type ' + ' ' + co.getType()  
        #sSql = self.getSqlField(sSql,co)
        #res = self.rpc.callRP('Database.executeNormalQuery',sSql, self.dicUser)
        pass
 
    def startXMLCheck(self, key, lEntry, sNameOfTable):
        self.out( 'XML-Check')
        self.out( key)
        self.out( lEntry)
        self.out( '------------------------------------------------------------------------------------')
        
        cle = cuon.Windows.cyr_load_entries.cyr_load_entries()
        ### for Server-functions set the td-object
        cle.td = self.td
         
        entrySet = cle.getEntriesDefinition(key,lEntry, sNameOfTable)
        self.out( 'entry-Set = ' + str(entrySet.getName()))
        cle.saveEntries('entry_' + entrySet.getName() + '.xml', entrySet )
        self.out( 'end startXMLCheck')
        #ok = self.rpc.callRP('src.Databases.py_packCuonFS')    

       
    def saveGladeFiles(self):

        self.out( 'start save glade-files to zodb')
        self.out( self.td.nameOfGladeFiles, self.INFO)
        nameOfGladeFiles = []
        for key in self.td.nameOfGladeFiles.keys():
            self.out( 'xml = ' + key, self.INFO)
            print  'glade-xml = ' + key
            
            gladeName = self.td.nameOfGladeFiles[key]
            self.out( 'gladename = ' + `gladeName`, self.INFO)
            print 'gladename = ' + `gladeName`
            f1 = open(gladeName)
            xml1 = f1.read()
            f1.close()
            self.rpc.callRP('Database.saveInfo',key, self.doEncode(repr(cPickle.dumps(xml1) )))
            nameOfGladeFiles.append(key)
        print 'nameOfGladeFiles',nameOfGladeFiles
        ok = self.rpc.callRP('Database.saveInfo', 'nameOfGladeFiles', self.doEncode(repr(cPickle.dumps(nameOfGladeFiles) )))
        print 'ok = ', ok 
#        ok = self.rpc.callRP('src.Databases.py_packCuonFS')

    def saveReportFiles(self):
        pass
##        self.out( 'start save report-files to zodb')
##        self.out( self.td.nameOfReportFiles, self.INFO)
##        nameOfReportFiles = []
##        for key in self.td.nameOfReportFiles.keys():
##            self.out( 'xml = ' + key, self.INFO)
##            reportName = self.td.nameOfReportFiles[key]
##            self.out( 'reportname = ' + `reportName`, self.INFO)
##            f1 = open(reportName)
##            xml1 = f1.read()
##            f1.close()
##            self.rpc.callRP('Database.saveInfo', key, self.doEncode(repr(cPickle.dumps(xml1) )))
##            nameOfReportFiles.append(key)
##
##        self.rpc.callRP('Database.saveInfo', 'nameOfReportFiles', self.doEncode(repr( cPickle.dumps(nameOfReportFiles) )))
##   
#        ok = self.rpc.callRP('src.Databases.py_packCuonFS')
   
    def importZip(self, filename):
        sDir = os.path.dirname(filename)
        dicPlanet = {}
        f = open(sDir + '/planet.txt')
        
        if f:
            line = f.readline()
            while line:
                line = unicode(line)
                liLines = line.split(';')
                #dicPlanet['SolarSystem'] = 1
                dicPlanet['name'] = [liLines[0],'string']
                dicPlanet['name2'] = [liLines[1],'string']
                dicPlanet['orbit'] = [liLines[2],'float']
                dicPlanet['diameter'] = [liLines[3],'float']

                dicPlanet['solar_system_id'] = [1,'int']
                
                print dicPlanet
                result = self.rpc.callRP('Database.saveZipPlanet', dicPlanet, self.dicUser)
                print 'result = ' + `result`
                line = f.readline()
            f.close()
        # read  country
        dicCountry = {}
        f = open(sDir + '/country.txt','rb')
        
        if f:
            line = f.readline()
            while line:
                #line = line.decode('iso-8859-15')
##                print line
##                line = unicode(line)
##                print 'ö ä ü ß Ö Ä Ü'
##                print u'ö ä ü ß Ö Ä Ü'
##                print line
##                line = line.decode('latin-1')
##                print line
                
                liLines = line.split(';')
                
                dicCountry['planet_id'] = [1,'int']
                dicCountry['name'] = [liLines[0],'string']
                dicCountry['short_name'] = [liLines[1],'string']
                dicCountry['name2'] = [liLines[2],'string']
                
                print dicCountry
                result = self.rpc.callRP('Database.saveZipCountry', dicCountry, self.dicUser)
                print 'result = ' + `result`
                line = f.readline()
            f.close()           
        
        dicState = {}
        f = codecs.open(sDir + '/states.txt','rb',encoding="utf-8")
        
        if f:
            line = f.readline()
            while line:
                #line = unicode(line)
                print line
                print 'öäüßÖÄÜ'
                print u'öäüßÖÄÜ'
                print line
                #line = line.decode('latin-1')
                print line
                #line = line.decode('utf-8')
                print line
                
                liLines = line.split(';')
                
                dicState['country_id'] = [liLines[0],'int']
                dicState['name'] = [liLines[2].strip(),'string']
                dicState['state_short'] = [liLines[1].strip(),'string']
                
                print dicState
                result = self.rpc.callRP('Database.saveZipState', dicState, self.dicUser)
                print 'result = ' + `result`
                line = f.readline()
            f.close()
            
        dicCity = {}
        f = codecs.open(filename,'rb',encoding="utf-8")
        print f
        if f:
            line = f.readline()
            while line :
                if len(line.strip()) > 1 and line[0] != '#':
                    dicCity = {}
                    dicZip = {}
                    liLines = line.split(';')
                    if liLines[1] == 'DE':
                        liLines[1] = 'D'
                    dicCity['country_id'] = [liLines[1].strip(),'int']
                    dicCity['state_id'] = [liLines[2].strip(),'int']
                    dicCity['ad_id'] = [liLines[3].strip(),'int']
                    dicCity['district_id'] = [liLines[4].strip(),'int']
    
                    dicCity['name'] = [liLines[6].strip(),'string']
                    dicCity['longitude'] = [float(liLines[10].strip()),'float']
                    dicZip['zipcode'] = [liLines[13].strip(),'string']
                    
                    print dicCity
                    result = self.rpc.callRP('Database.saveZipCity', dicCity, dicZip, self.dicUser)
                    print 'result = ' + `result`
                line = f.readline()
            f.close()
                
                    
                #singleImportZip.Zips = zips
                #singleImportZip.newRecord()
                #singleImportZip.save()
                
                
                


        
    
    def setGrants(self):
        self.out("set grants")
        self.out(self.td.nameOfXmlGrantFiles)
        
        #for key in self.td.nameOfXmlGrantFiles.keys():
        
        #doc = self.readDocument(self.td.nameOfXmlGrantFiles[key])
        doc = self.readDocument('etc/grants.xml')
        # groups
        if doc:
            cyRootNode = self.getRootNode(doc)
            cyNode = self.getNode(cyRootNode,'groups')
            cyNodes = self.getNodes(cyNode[0],'group')
            if cyNodes:
                for i in cyNodes:
                    groupNode = self.getNodes(i,'nameOfGroup')
                    group = self.getData(groupNode[0])
                    self.out(group)
                    print 'group = ' + `group`
                    print `self.dicUser`
                    ok = self.rpc.callRP('Database.createGroup', group, self.dicUser)       
                    self.out(ok)
        
        # user
        if doc:
            cyRootNode = self.getRootNode(doc)
            cyNode = self.getNode(cyRootNode,'users')
            cyNodes = self.getNodes(cyNode[0],'user')
            self.out('CyNodes' + `cyNodes`) 
            if cyNodes:
                for i in cyNodes:
                    userNode = self.getNodes(i,'nameOfUser')
                    user = self.getData(userNode[0])
                    self.out('User = ' + `user`)
                    print 'User = ' + `user`
                    ok = self.rpc.callRP('Database.createUser', user,'None', self.dicUser, 1)       
                    self.out(ok)


        # add user to group
        if doc:
            cyRootNode = self.getRootNode(doc)
            cyNode = self.getNode(cyRootNode,'addgroups')
            cyNodes = self.getNodes(cyNode[0],'addgroup')
            self.out('CyNodes' + `cyNodes`) 
            if cyNodes:
                for i in cyNodes:
                    userNode = self.getNodes(i,'this_user')
                    user = self.getData(userNode[0])
                    groupNode = self.getNodes(i,'this_group')
                    group = self.getData(groupNode[0])
                    self.out('User = ' + `user` + ' , Group = ' + group)
                    ok = self.rpc.callRP('Database.addUserToGroup', user, group, self.dicUser)       
                    self.out(ok)

        # add grants to group
        if doc:
            cyRootNode = self.getRootNode(doc)
            cyNode = self.getNode(cyRootNode,'setGrants')
            cyNodes = self.getNodes(cyNode[0],'grant')
            self.out('CyNodes' + `cyNodes`) 
            if cyNodes:
                for i in cyNodes:
                    grantNode = self.getNodes(i,'this_grants')
                    grants = self.getData(grantNode[0])
                    tableNode = self.getNodes(i,'this_tables')
                    tables = self.getData(tableNode[0])
                    groupNode = self.getNodes(i,'this_group')
                    group = self.getData(groupNode[0])
                    print'Grants = ' + `grants` + ' , Group = ' + group + ', Tables = ' + tables
                    ok = self.rpc.callRP('Database.addGrantToGroup', grants, group, tables, self.dicUser)       
                    self.out(ok)
                                                                
        # now set public-right to the numerical seqeunces
        sSql = "SELECT relname FROM PG_CLASS WHERE RELKIND = 'S' and relname ~* 'numerical.*' "
        res = self.rpc.callRP('Database.executeNormalQuery',sSql, self.dicUser)
        print res
        if res not in ['NONE','ERROR']:
            for seqs in res:
                sSql = 'GRANT select, update on ' + seqs['relname'] + ' TO PUBLIC'
                ok = self.rpc.callRP('Database.executeNormalQuery',sSql, self.dicUser)
                
        
    def createProcedureAndTrigger(self):
        self.setLogLevel(0)
        self.out("set procedures and trigger")
     
        os.system('scp -P ' + self.td.sshPort + ' ' + self.td.sPrefix + '/etc/cuon/server.ini inifiles')
        
        for configfile in ['sql.xml', 'basics.xml', 'order.xml', 'address.xml', 'garden.xml', 'graves.xml']:
            os.system('scp -P ' + self.td.sshPort + ' ' + self.td.sPrefix + '/etc/cuon/sql/'+configfile + ' inifiles')
            doc = self.readDocument('inifiles/'+configfile)
            # procedures
            if doc:
                cyRootNode = self.getRootNode(doc)
                cyNode = self.getNode(cyRootNode,'postgre_sql')
                cyNodes = self.getNodes(cyNode[0],'function')
                f = file('inifiles/server.ini','r')
                cpParser = ConfigParser.ConfigParser()
                cpParser.readfp(f)
                sFile = None
                f.close()
                
                try:
                
                    SQL_DB = cpParser.get('POSTGRES', 'POSTGRES_DB')
                    SQL_HOST = cpParser.get('POSTGRES', 'POSTGRES_HOST')
                    SQL_USER = cpParser.get('POSTGRES', 'POSTGRES_USER')
                    SQL_PORT = cpParser.get('POSTGRES', 'POSTGRES_PORT')
                except Exception, param:
                    print Exception, param
                    
                if cyNodes:
                    for i in cyNodes:
                        self.out("Werte in xml")
                                                
                        funcNode = self.getNodes(i,'nameOfFunction')
                        newName = self.getData(funcNode[0])
                        self.out(newName)
    
                        #funcNode = self.getNodes(i,'old_name')
                        #oldName = self.getData(funcNode[0])
                        #self.out(oldName)
    
                        funcNode = self.getNodes(i,'language')
                        sql_lang = self.getData(funcNode[0])
                        self.out(sql_lang)
    
                        funcNode = self.getNodes(i,'textOfFunction')
                        func = self.getData(funcNode[0])
                        self.out(func)
                        # first delete the function ( specified in Old_name )
                        #sSql = 'DROP FUNCTION ' + oldName + ' CASCADE'
                        #ok = self.rpc.callRP('Database.createPsql', 'cuon','sat1','5432','jhamel', sSql)
                        
                        
                        #ok = self.rpc.callRP('Database.createPsql', SQL_DB, SQL_HOST, SQL_PORT, SQL_USER, sSql)       
                        #self.out(ok)
                        #print sSql                       
                        #print ok
    
                        
                        sSql = 'CREATE OR REPLACE FUNCTION ' + newName + ' AS \$\$  '  
                        sSql = sSql + func
                        sSql = sSql + ' \$\$'
                        sSql = sSql + ' LANGUAGE \'' + sql_lang + '\'; '
                        self.out('sql = ' + sSql)
                        #sSql = string.replace(sSql,';', '\\;')
                        #sSql = string.replace(sSql,'$', '\\$')
                        #sSql = string.replace(sSql,"'", "\'")
                        ok = self.rpc.callRP('Database.createPsql', SQL_DB, SQL_HOST, SQL_PORT, SQL_USER, sSql)
                        #ok = self.rpc.callRP('Database.executeNormalQuery', sSql, self.dicUser)
                        self.out(ok)
                        print sSql                       
                        print ok
    
                # Indexe 
                cyNodes = self.getNodes(cyNode[0],'index')
                if cyNodes:
                    for i in cyNodes:
                        self.out("Werte in xml")
                        dicIndex = {}                        
                        indexNode = self.getNodes(i,'index_name')
                        dicIndex['name'] = self.getData(indexNode[0])
    
                        indexNode = self.getNodes(i,'index_special')
                        dicIndex['special'] = self.getData(indexNode[0])
                        
                        indexNode = self.getNodes(i,'index_table')
                        dicIndex['table'] = self.getData(indexNode[0])
                        
                        indexNode = self.getNodes(i,'index_column')
                        dicIndex['column'] = self.getData(indexNode[0])
                        try:
                            ok = True
                            while ok: 
                                if dicIndex['column'] and dicIndex['column'].find('##')>=0:
                                    searchWord = dicIndex['column'][dicIndex['column'].find('##')+2:dicIndex['column'].find(';;')]
                                    dicIndex['column'] [dicIndex['column'].find('##'):dicIndex['column'].find(';;') +2] = self.DIC_USER[searchWord]
                                else:
                                    ok = False
                                    
                        except Exception,  param:
                            print Exception, param
                            
                        
                        # first drop index
                        
                        sSql = "drop index " + dicIndex['name']
                        print 'Sql INDEX = ', sSql
                        result = self.rpc.callRP('Database.executeNormalQuery', sSql, self.dicUser)
                     
                        # now set new index
                        sSql = "create " 
                        if len(dicIndex['special']) > 1:
                            sSql += dicIndex['special']
                        sSql += " index " + dicIndex['name']
                        sSql += " on " + dicIndex['table']
                        sSql += " (" + dicIndex['column'] + ")"
                        
                        
                        
                        print 'Sql INDEX = ', sSql
                        result = self.rpc.callRP('Database.executeNormalQuery', sSql, self.dicUser)
                        print result
    
    
                # Foreign keys
                cyNodes = self.getNodes(cyNode[0],'foreign_key')
                print 'cyNodes = ', cyNodes
                if cyNodes:
                    for i in cyNodes:
                        print i.toxml()
                        self.out("Werte in xml")
                        dicForeign = {}                        
                        foreignNode = self.getNodes(i,'foreign_key_name')
                        dicForeign['name'] = self.getData(foreignNode[0])
    
                        foreignNode = self.getNodes(i,'foreign_table')
                        dicForeign['table'] = self.getData(foreignNode[0])
    
                        foreignNode = self.getNodes(i,'foreign_key_sql')
                        dicForeign['sql'] = self.getData(foreignNode[0])
    
                        sSql = 'alter table ' + dicForeign['table']
                        sSql += ' ADD CONSTRAINT "f_' + dicForeign['name'] +'" '
                        sSql += dicForeign['sql']
                        
                        self.out( sSql)
                        print '--------------------------------------------------------------'
                        print 'Sql Foreign key = ', sSql
                        print '--------------------------------------------------------------\n\n'
    
                        result = self.rpc.callRP('Database.executeNormalQuery', sSql, self.dicUser)
                    
                        
                
                
                # Trigger
                cyNodes = self.getNodes(cyNode[0],'trigger')
                if cyNodes:
                    for i in cyNodes:
                        self.out("Werte in xml")
                                                
                        triggerNode = self.getNodes(i,'nameOfTrigger')
                        newName = self.getData(triggerNode[0])
                        self.out(newName)
    
                        triggerNode = self.getNodes(i,'table')
                        table = self.getData(triggerNode[0])
                        self.out(table)
    
                        triggerNode = self.getNodes(i,'action')
                        action = self.getData(triggerNode[0])
                        self.out(action)
    
                        triggerNode = self.getNodes(i,'cursor')
                        cursor = self.getData(triggerNode[0])
                        self.out(cursor)
    
                        triggerNode = self.getNodes(i,'textOfTrigger')
                        triggerText = self.getData(triggerNode[0])
                        self.out(triggerText)
    
                        
                        # first delete the trigger called newName
                        sSql = 'DROP TRIGGER ' + newName + ' on ' + table 
                        
                        ok = self.rpc.callRP('Database.createPsql', SQL_DB,SQL_HOST,SQL_PORT, SQL_USER, sSql)       
                        self.out(ok) 
                        print sSql                       
                        print ok
    
                        #then create the trigger called newName
                        sSql = 'CREATE TRIGGER ' + newName + ' '
                        sSql = sSql + action + ' ON ' + table
                        sSql = sSql + ' ' + cursor + ' ' + triggerText 
                        
                        ok = self.rpc.callRP('Database.createPsql', SQL_DB,SQL_HOST,SQL_PORT, SQL_USER, sSql)       
                        self.out(ok)
                        print sSql                       
                        print ok

