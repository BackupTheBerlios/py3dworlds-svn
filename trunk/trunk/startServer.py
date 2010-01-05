#!/usr/bin/python

import databases.databases
import os,  sys
import commands


class startServer:
    def __init__(self):
        self.databases = databases.databases.databases()
        print self.databases
        
    def checkDatabaseStructure(self):
        self.databases.on_dbcheck1_activate('Server')
     
   
start = startServer()
start.checkDatabaseStructure()
