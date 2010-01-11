 
 
class constants:
     
    def __init__(self):
 
        self.nameOfXmlTableFiles ={ 'tables.xml' : 'etc/tables.xml',  'ext1' : 'etc/ext1.xml' }
        self.RegionSize = 256 
        self.TerrainPatchSize = 16 
        self.DefaultTexture = "89556747-24cb-43ed-920b-47caed15465f"

        # Permissions
        Group = 4
        Everyone = 8
        NextOwner = 16

        Copy = 0x00008000
        Modify = 0x00004000
        Move = 0x00080000
        Transfer = 0x00002000
