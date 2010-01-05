# -*- coding: utf-8 -*-
##Copyright (C) [2003]  [Jürgen Hamel, D-32584 Löhne]

##This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as
##published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

##This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
##warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
##for more details.

##You should have received a copy of the GNU General Public License along with this program; if not, write to the
##Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA. 

import shelve
import sys
import os
import os.path
import pickle
import base64
import time
import datetime 
import time
import random
import types
import bz2
from basics import basics


#import os.path

class dumps(basics):
    def __init__(self, td=None):
        basics.__init__(self)
        self.dbase = None
        self.decimalLocale = {}
        self.decimalLocale['coma'] = ['de','nl','it','pl','au','ch']
        self.td = None
        #print '------------------------------------------------'
        if td:
            #print 'td is not None'
            self.td = td
        else:
            #print 'set td new'
            #self.td = cuon.TypeDefs.typedefs.typedefs()
            print 'hallo'
        try:
            print 'td', self.td.server
            print self.td.cuon_path
        except:
            pass
        #print '------------------------------------------------'
        
    def openDB(self):
        #print 'PATH = ', self.td.cuon_path
        
        self.dbase = shelve.open(os.path.normpath('../' + 'cuonObjects'))

    def closeDB(self):
       
        self.dbase.close()
        
    def saveObject(self, key, oValue):
        # print "Save = " + `key` + ", " + self.td.cuon_path + '/' + 'cuonObjects'
        
        self.dbase[key] = oValue

    def loadObject(self, key):
        # print "Home = " + self.td.cuon_path + '/' + 'cuonObjects'
        # print key
        oValue = None
        # dbase  = shelve.open(os.path.normpath(self.td.cuon_path + '/' + 'cuonObjects'))
   
        try:
            oValue = self.dbase[key]
        except:
            oValue = None
            
        # dbase.close()
        return oValue
    

    def pickleObject(self, key, obj):
        # print key
        pkey = os.path.normpath(self.td.cuon_path +'/' + `key`)
        fkey = open(pkey,'w')
        pickle.dump(obj,fkey, 1)
        fkey.close()
        

    def unpickleObject(self, key):
        #print key
        pkey = os.path.normpath(self.td.cuon_path +'/' + `key`)
        fkey = open(pkey)
        obj =  pickle.load(fkey)
        fkey.close()
        return obj
    
        
    
    def doEncode(self, s):
        return base64.encodestring(s)

    def doDecode(self, s):
        return  base64.decodestring(s)


    def doCompress(self,s):
        return bz2.compress( s)
    def doUncompress(self,s):
        return bz2.decompress( s)
        
    def saveTmpData(self, data, typ):
        s = ''
        if not typ:
            typ = 'pdf'
            
        n = random.randint(0,1000000000)
        for i in range(27):
            ok = True
            while ok:
                r = random.randint(65,122)
                if r < 91 or r > 96:
                    ok = False
                    s = s + chr(r)
    
        s = s + `n`
        s =  os.path.normpath(self.td.cuon_path + '/cuon__' +  s + `time.time()` + '.' + typ)
        f = open(s,'wb')
        f.write(data)
        f.close()
        return s
        
    def showPdf(self, Pdf, dicUser, cDoc = 'PDF'):
        #print "PDF", Pdf
        
        s = self.doDecode(Pdf)
        fname = self.saveTmpData(s, 'pdf')
        print "fname = ",  fname
        #print 'PDF-App = ', dicUser['prefApps']['PDF']
        if cDoc == 'PDF':
            sOutput = os.system(dicUser['prefApps']['PDF'] + ' ' + fname + ' &')
        elif cDoc == 'SUPPLY':
            print "Supply using",  dicUser['prefApps']['printSupply'] 
            sOutput = os.system(dicUser['prefApps']['printSupply'] + ' ' + fname + ' &')
        elif cDoc == 'PICKUP':
            sOutput = os.system(dicUser['prefApps']['printPickup'] + ' ' + fname + ' &')
        elif cDoc == 'INCOMING':
            sOutput = os.system(dicUser['prefApps']['printPickup'] + ' ' + fname + ' &')    
        elif cDoc == 'INVOICE':
            print "Invoice using",  dicUser['prefApps']['printInvoice'] 
            sOutput = os.system(dicUser['prefApps']['printInvoice'] + ' ' + fname + ' &')
        elif cDoc == 'PRINTNEWSLETTER':
            sOutput = os.system(dicUser['prefApps']['printNewsletter'] + ' ' + fname + ' &')
            
          
        else:
            sOutput = os.system(dicUser['prefApps']['PDF'] + ' ' + fname + ' &')
            
        return fname
        

    def getCheckedValue(self, value, type, min = None, max = None):
        retValue = None
        try:
            assert type
            if type == 'int':
                if isinstance(value, types.IntType) or isinstance(value, types.LongType) :
                
                
                    try:
                        retValue = int(value)
                    except:
                        retValue = 0
                    

                else:
                    try:
                        assert value != None
                        if isinstance(value, types.StringType):
                            value = value.strip()
                            if value[0] == 'L'  or value[0] == 'l':
                                value = value[1:]
                            
                        retValue = int(value)
                    except:
                        retValue = 0
                
                        
            elif type == 'float':
                if not isinstance(value, types.FloatType):
                    try:
                        assert value != None

                        if isinstance(value, types.StringType):
                            
                            value = value.strip()
                            convert = False
                            print 'convert userlocales = ', self.dicUser['Locales']
                            for sLocale in self.decimalLocale['coma']:
                                #print sLocale
                                if sLocale == self.dicUser['Locales']:
                                    convert = True
                            if convert:
                                #print 'convert to normal float'
                                value = value.replace('.','')
                                value = value.replace(',','.')
                                
                                    
                            if value[0] == 'L'  or value[0] == 'l':
                                value = value[1:]
                        retValue = float(value)
                    except:
                        retValue = 0.0
                else:
                    retValue =  value 
            elif type == 'toStringFloat':
                if isinstance(value, types.StringType):
                    if value == 'NONE':
                        value = '0.00'
                    elif value == 'None':
                        value = '0.00'
                        
                        
                    convert = False
                    print 'convert userlocales = ', self.dicUser['Locales']
                    for sLocale in self.decimalLocale['coma']:
                        #print sLocale
                        if sLocale == self.dicUser['Locales']:
                            convert = True
                    if convert:
                        #print 'convert to normal float'
                        value = value.replace('.',',')
                        #value = value.replace(',','.')
                    retValue = value 

            elif type == 'toLocaleString':
                retValue = value
                try:
                    if isinstance(value, types.FloatType):
                        convert = False
                        for sLocale in self.decimalLocale['coma']:
                            #print sLocale
                            if sLocale == self.dicUser['Locales']:
                                convert = True
                        if convert:
                            value = `value`.replace('.',',') 
                        else:
                            value = `value`
                        
                        retValue = value
                except:
                    retValue = '0'
                
            elif type == 'date':
                #print 'value by date', value
                print 'date1',  value
                retvalue = time.strptime(value, self.dicUser['DateformatString'])
                print 'dt2 = ', retvalue
                
                        
                    #elif entry.getVerifyType() == 'date' and isinstance(sValue, types.StringType):
                    #    dt = datetime.datetimeFrom(sValue)
                    #dt = datetime.strptime(sValue, "YYYY-MM-DD HH:MM:SS.ss")
                    #dt = datetime.datetime(1999)
                    #    # self.out( dt)
                    #    sValue = dt.strftime(self.sDateFormat)
                    
            elif type == 'formatedDate':
                print 'value by formatedDate', value
                checkvalue = []
                retValue = ''
                try:
                    checkvalue = time.strptime(value, self.dicUser['DateformatString'])
                    self.printOut( 'dtFormated2 = ', checkvalue)
                except:
                    retValue = ''
                    checkvalue = []
                if checkvalue and checkvalue[0] == 1900 and checkvalue[1] == 1 and checkvalue[2] == 1:
                    # 1900/1/1 --> set to empty
                    retvalue = ''
                elif checkvalue:
                    retValue = value
                    
                
                
                    
            elif type == 'toStringDate':
                print 'value by toStringDate', value
                retValue = time.strftime(self.dicUser['DateformatString'],value)
                self.printOut( 'dt5 = ', retValue) 
                
            elif type == 'string':    
                #print 'check string = ', value
                
                if not isinstance(value, types.StringType):
                    value = `value`
                if value == 'NONE':
                    value = ''
                elif value == 'None':
                    value = ''
                
                retValue = value
                
                
                
            else:
                retValue = value
        
        except AssertionError:
            print 'No type set '
            retValue = value
        except Exception,params:
            print Exception, params
            retValue = value
        
        #print 'retvalue = ', retValue
        
        return retValue
        
    
    def getTime(self,s ):
        try:
            if isinstance(s,types.StringType):
                iS = int(s)
            else:
                iS = s
                
            Hour,Minute = divmod(iS,4)
            Minute = Minute * 15
        except:
            Hour = 0
            Minute = 0
            
        
        return Hour, Minute
        
    def getTimeString(self, s):
        Hour, Minute = self.getTime(s)
        #print Hour, Minute
        sHour = `Hour`
        if Minute == 0:
            sMinute = '00'
        else:
            sMinute = `Minute`
        
        s = sHour + ':' + sMinute
        return s
        
        
    def getActualDateTime(self):
        newTime = time.localtime()
        tDate =  time.strftime(self.dicUser['DateformatString'], newTime)
        tTime =  time.strftime(self.dicUser['TimeformatString'], newTime)
        tStamp = time.strftime(self.dicUser['DateTimeformatString'], newTime)
        dicTime = {'date':tDate, 'time':tTime, 'timestamp':tStamp }
        
        return dicTime
        
       
    
    def getDateTime(self,dateString,strFormat="%Y-%m-%d"):
        # Expects "YYYY-MM-DD" string
        # returns a datetime object
        eSeconds = time.mktime(time.strptime(dateString,strFormat))
        return datetime.datetime.fromtimestamp(eSeconds)
    
    def formatDate(self,dtDateTime,strFormat="%Y-%m-%d"):
        # format a datetiself, me object as YYYY-MM-DD string and return
        return dtDateTime.strftime(strFormat)
    
    def getFirstOfMonth2(self, dtDateTime):
        #what is the first day of the current month
        ddays = int(dtDateTime.strftime("%d"))-1 #days to subtract to get to the 1st
        delta = datetime.timedelta(days= ddays)  #create a delta datetime object
        return dtDateTime - delta                #Subtract delta and return
    
    def getFirstOfMonth(self, dtDateTime):
        #what is the first day of the current month
        #format the year and month + 01 for the current datetime, then form it back
        #into a datetime object
        return self.getDateTime(self.formatDate(dtDateTime,"%Y-%m-01"))
        
    def getFirstOfYear(self, dtDateTime):
        #what is the first day of the current month
        #format the year and month + 01 for the current datetime, then form it back
        #into a datetime object
        return self.getDateTime(self.formatDate(dtDateTime,"%Y-01-01"))
    
    def getLastOfMonth(self, dtDateTime):
        dYear = dtDateTime.strftime("%Y")        #get the year
        dMonth = str(int(dtDateTime.strftime("%m"))%12+1)#get next month, watch rollover
        if int(dMonth) == 1:
            iYear = int(dYear)
            iYear += 1
            dYear = `iYear`
        print dMonth, len(dMonth)
        print dYear, len(dYear)
        
        dDay = "1"                               #first day of next month
        nextMonth = self.getDateTime("%s-%s-%s"%(dYear,dMonth,dDay))#make a datetime obj for 1st of next month
        delta = datetime.timedelta(seconds=1)    #create a delta of 1 second
        return nextMonth - delta                 #subtract from nextMonth and return
        
    def getLastOfYear(self, dtDateTime):
        dYear = dtDateTime.strftime("%Y")        #get the year
        
        return self.getDateTime(self.formatDate(dtDateTime,"%Y-12-31"))
    
    
    def getFirstDayOfMonth(self,sdate=None):
        if sdate == None:
            dDate = datetime.date.today()   
        else:
            dDate = sdate
            
        return self.getFirstOfMonth(dDate)
        
    def getLastDayOfMonth(self,sdate=None):
        if sdate == None:
            dDate = datetime.date.today()   
        else:
            dDate = sdate
            
        return self.getLastOfMonth(dDate)
        
        
    def getSeconds(self, dt):
        eSeconds = time.mktime( dt.timetuple())
        return eSeconds

    
    def getFirstDayOfMonthAsSeconds(self,sdate=None):
        return self.getSeconds(self.getFirstDayOfMonth(sdate))
        
    def getLastDayOfMonthAsSeconds(self,sdate=None):
        return self.getSeconds(self.getLastDayOfMonth(sdate))
        
        
    def getFirstLastDayOfLastMonthAsSeconds(self,sdate=None):
        currentFirstDay = self.getFirstDayOfMonth(sdate)
        secs = self.getSeconds(currentFirstDay) - 10
        print 'secs' , secs
        ddate = datetime.datetime.fromtimestamp(secs)
        
        dBegin = self.getFirstDayOfMonthAsSeconds(ddate)
        dEnd = self.getLastDayOfMonthAsSeconds(ddate)
        print dBegin,dEnd
        return dBegin,dEnd
        
        
    def startExternalPrg (self, sProgramName, *args):
        "Start an external program and return immediately, returning proc id"
        print 'program = ',sProgramName
        print 'args = ', args
        
        if os.name == "posix": 
            spawn = os.spawnvp #not available on windows though
            print 'posix system found'
            sret = spawn(os.P_NOWAIT, sProgramName, (sProgramName,) + args)
            print sret
            return sret 
        else:
            sArgs = ''
            for s in args:
                sArgs += s + ' ' 
            return os.system(sProgramName + ' ' + sArgs )
    


    def writeEmailLog(self, sMessage):
        try:
            f = open(os.path.normpath(self.td.cuon_path + '/' + 'cuonmail.log'),'a')
            f.write(time.ctime(time.time() ))
            f.write('     ')
            f.write(sMessage)
            f.write('\n')
            f.close()  
        except:
            pass
            
    def checkType(self, oType, sType):
        bRet = False
        if sType == 'string':
            if isinstance(oType, types.StringType):
                bRet = True
        elif sType == 'int':
            if isinstance(oType, types.IntType):
                bRet = True
        elif sType == 'float':
            if isinstance(oType, types.FloatType):
                bRet = True
                                              
        return bRet

    
    
            
##    if __name__=="__main__":
##        for i in range(12):
##            thisMonth = ("0%i"%(i+1,))[-2:]
##            print thisMonth
##            #d = getDateTime("2004-%s-02"%thisMonth)
##        d = datetime.date.today() 
##            print formatDate(d)
##            print formatDate(d,"%Y%m%d")
##            print getFirstOfMonth(d)
##            print getFirstOfMonth2(d)
##            print getLastOfMonth(d)
##    
##        t1 =  datetime.date.today()
##        print 't1= ',`t1`
##        print t1.month
##    
##        print t1.month   
        
