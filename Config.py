import json

class Config:
    """docstring for Config"""
    def __init__(self, file="./config.cfg"):
        self.path = file
        
    def getContents(self):
        config = open(self.path, "r")
        jsonMap = config.read()
        contents = {} if jsonMap == '' else json.loads(jsonMap)
        config.close()
        return contents
        
    def setContents(self, content):
        config = open(self.path, "w")
        config.seek(0)
        config.write(json.dumps(content))
        config.close()
    
    def addMapping(self, map, type='buttonToKey'):
        if len(map) <> 2:
            return False
        # Save the config
        currentConfig = self.getContents()
        
        # Check for non existing types
        if type not in currentConfig:
            currentConfig[type] = {}
        if type == 'analogToKey':
            mapKey = map[0].keys()[0]
            currentConfig[type][mapKey] = {"axeValues": map[0][mapKey], "mappedKey": map[1]}
        else:
            currentConfig[type][str(map[0])] = map[1]
        self.setContents(currentConfig)
        
        return True
