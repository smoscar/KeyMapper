
class Config:
    """docstring for Config"""
    def __init__(self, file="./config.cfg"):
        self.path = file
    
    def addMapping(self, map):
        if len(map) <> 2:
            return False
        # Save the config
        config = open(self.path, "w")
        config.writelines([str(line) + "\n" for line in map])
        config.close()
        return True
