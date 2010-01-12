import MySQLdb
import base64 
import types 
from databases.basics import basics 

class convertBlobs(basics):
    
    def __init__(self):
        basics.__init__(self)
        
        
    def executeNormalQueryOS(self, sSql):
        conn = MySQLdb.connect(host="sim-linuxmain.org", user="opensim", passwd="Aabi3eis", db="opensim")
        print conn
        cursor = conn.cursor()
        print sSql
        cursor.execute(sSql)
        result = cursor.fetchall()
        print result
        
        cursor.close()
        conn.commit()
        conn.close()
        return result 
        
        
    def dump(self, table, liBlobs,  sBegin):
        sSql = " select * from " + table
    

        result = self.executeNormalQueryOS(sSql)
    
        print 'len of result = ',  len(result)
        print ' len of row = ',  len(result[0])
        
        f = open(table +".sql",  "wb")
        f.write(sBegin)
        for i in range(len(result)):
            for j in range(len(result[0])):
                if j not in liBlobs:
                    #print "i, j = ",  i,  j
                    #print 'result = ',  result[i][j]
                    if result[i][j] == None:
                        f.write(' ,  ')
                    else:
                        
                        if isinstance(result[i][j], types.IntType) or isinstance(result[i][j], types.LongType):
                            print 'Found intType at ',  i, j
                            f.write(self.convertTo(result[i][j], 'String') + ',  ' )
                        else:
                            
                            f.write (`result[i][j]` + ',  ')
                else:
                    #f2 = open('result_'+`i`+'_' +`j`, 'wb')
                    #f2.write(result[i][j])
                    #f2.close()
                    
                    s1 = base64.encodestring(`result[i][j]` )
                    #print `s1`
                    #s1.replace('\n', '')
                    f.write(`s1` + ',  ')
                    
            f.write(' ) ,  ( ')
        f.close()
        
            
        
    def dump_avatarappearance(self):
        
        sBegin = "INSERT INTO avatarappearance (Owner, Serial, Visual_Params, Texture, Avatar_Height, Body_Item, Body_Asset, Skin_Item, Skin_Asset, Hair_Item, Hair_Asset, Eyes_Item, Eyes_Asset, Shirt_Item, Shirt_Asset, Pants_Item, Pants_Asset, Shoes_Item, Shoes_Asset, Socks_Item, Socks_Asset, Jacket_Item, Jacket_Asset, Gloves_Item, Gloves_Asset, Undershirt_Item, Undershirt_Asset, Underpants_Item, Underpants_Asset, Skirt_Item, Skirt_Asset) VALUES ("
        self.dump('avatarappearance', [2,3],  sBegin)

cb = convertBlobs()
cb.dump_avatarappearance()
