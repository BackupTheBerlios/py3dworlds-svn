class Utils:

    def __init__(self):
        pass
        
    def make64BitInt(self, x, y):
        z = `x` + `y`
        z = z.replace("'", "")
        return long(z)
     
