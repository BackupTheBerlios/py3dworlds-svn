import sys
import string


class dataEntry:

    def __init__(self):
        self.nameOfEntry="EMPTY"
        self.typeOfEntry="EMPTY"
        self.bDuty = False
        self.iRound = 0
        self.nextWidget = 'EMPTY'


    def setName(self,s):
        self.nameOfEntry = s

    def getName(self):
        return self.nameOfEntry



    def setType(self,s):
        self.typeOfEntry = s

    def getType(self):
        return self.typeOfEntry


    def setSizeOfEntry(self,s):
        self.sizeOfEntryOfEntry = s

    def getSizeOfEntry(self):
        return self.sizeOfEntryOfEntry


    def setVerifyType(self,s):
        self.verifyType = s

    def getVerifyType(self):
        return self.verifyType


    def setCreateSql(self,s):
        self.createSql = s

    def getCreateSql(self):
        return self.createSql


    def setSqlField(self,s):
        self.sqlFieldOfEntry = s

    def getSqlField(self):
        return self.sqlFieldOfEntry.encode("utf-8")


    def setBgColor(self,sColor):
        self.bgColor = sColor

      
    def getBgColor(self):
        return self.bgColor

    def setFgColor(self,sColor):
        self.fgColor = sColor
      
    def getFgColor(self):
        return self.fgColor

    def setDuty(self, bDuty = False):
        if bDuty == 'EMPTY':
            bDuty = False
            
        self.bDuty = bDuty

    def getDuty(self):
        return self.bDuty
    

    def setRound(self,sRound):
        iRound1 = -1
        if sRound != 'EMPTY':
            try:
                iRound1 = int(sRound)
            except:
                pass
                #print 'ERROR - No Integer'
                
        self.iRound = iRound1
        
    def getRound(self):
        return self.iRound
    
    def setNextWidget(self, sName):
        self.nextWidget = sName
        
    def getNextWidget(self):
        return self.nextWidget
        
        
