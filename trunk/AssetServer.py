# coding=utf-8
from twisted.web import xmlrpc
from databases.basics import basics
import databases.DB_Com
import uuid
from xmlrpc.xmlrpc import myXmlRpc
from misc.usefullThings import usefullThings

class AssetServer( xmlrpc.XMLRPC, basics, myXmlRpc,  usefullThings):
    def __init__(self):
        xmlrpc.XMLRPC.__init__(self)
        basics.__init__(self)
        self.db_com = databases.DB_Com.DB_Com()
        myXmlRpc.__init__(self)
        usefullThings.__init__(self)
