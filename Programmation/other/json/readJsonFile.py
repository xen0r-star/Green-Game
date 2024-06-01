import json
from jsonschema import validate
from pathlib import Path

paths = Path(__file__).parent.resolve()

class readJsonFileSchema:
    def __init__(self, file):
        try:
            with open(file, encoding='utf-8') as data_file:
                self.jsonFile = json.load(data_file)
        except:
            self.jsonFile = {'elements': []}

        with open(paths / 'schema.json', encoding='utf-8') as schema_file:
            self.schema = json.load(schema_file)
        
        if self.validateJson():
            self.data = self.jsonFile
        else:
            self.data = {'elements': []}


    def validateJson(self):
        try:
            validate(self.jsonFile, self.schema)
        except Exception as _:
            return False
        else:
            return True
        
    
    def get(self):
        return self.data["elements"]



class readJsonFile:
    def __init__(self, file):
        try:
            with open(file, encoding='utf-8') as data_file:
                self.jsonFile = json.load(data_file)
        except:
            self.jsonFile = {}
        
        self.data = self.jsonFile
        
    
    def get(self):
        return self.data
