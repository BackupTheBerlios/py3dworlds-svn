import sys


class setOfEntries:

    def __init__(self):
        self.nameOfSet="EMPTY"
        self.EntrySet = []
        #self.out("setOfEntries startet")
        self.iOldTab = 0
        self.xml = None
        self.za1 = 0
        
    def setXml(self, xml):
        self.xml = xml
        

    def setName(self,s):
        self.nameOfSet = s

    def getName(self):
        return self.nameOfSet

    def addEntry(self, entry):
       self.EntrySet.append(entry)

    def getEntryAtIndex(self, i):
        return self.EntrySet[i]

    def getCountOfEntries(self):
        return len(self.EntrySet)
    

    def getEntryByName(self, sName):
        entry = None
        for i in range(self.getCountOfEntries()):
            entry = self.getEntryAtIndex(i)
            #self.out( entry.getSqlField() + ' = ' + sName )
            if entry.getSqlField() == sName:
                return entry
        return None
        

           

 
    
