 
 
class constants:
     
    def __init__(self):
 
        self.nameOfXmlTableFiles ={ 'tables.xml' : 'etc/tables.xml',  'ext1' : 'etc/ext1.xml' }
        self.RegionSize = 256 
        self.TerrainPatchSize = 16 
        self.DefaultTexture = "89556747-24cb-43ed-920b-47caed15465f"

        self.dtd1 = 'InventoryCollection xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        self.dtd1_2 = 'xmlns:xsd="http://www.w3.org/2001/ XMLSchema"'
        # Permissions
        self.Group = 4
        self.Everyone = 8
        self.NextOwner = 16

        self.Copy = 0x00008000
        self.Modify = 0x00004000
        self.Move = 0x00080000
        self.Transfer = 0x00002000

        self.InventoryTextures = 0
        self.InventorySounds = 1
        self.InventoryCallingCards = 2
        self.InventoryLandmarks = 3
        self.InventoryClothing = 5
        self.InventoryObjects = 6
        self.InventoryNotecards = 7
        self.InventoryRoot = 8
        self.InventoryScripts = 10

        self.InventoryBodyParts = 13
        self.InventoryTrash = 14
        self.InventoryPhotoAlbum = 15

        self.InventoryLostAndFound = 16
        
        self.InventoryAnimations = 20
        self.InventoryGestures = 21
        
