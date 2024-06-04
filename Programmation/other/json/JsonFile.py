import json
from jsonschema import validate
from pathlib import Path

paths = Path(__file__).parent.resolve()



class readJsonFileSchema:
    """
    class pour lire un fichier json selon un schéma ce qui permets d'avoir un fichier json 
    avec des donnée tout ecrite de la meme façon
    """

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
        except Exception as e:
            print(e)
            return False
        else:
            return True
        
    
    def get(self):
        return self.data["elements"]



class readJsonFile:
    """
    class pour extraire les donnée d'un fichier.json
    """

    def __init__(self, file):
        try:
            with open(file, encoding='utf-8') as data_file:
                self.jsonFile = json.load(data_file)
        except:
            self.jsonFile = {}
        
        self.data = self.jsonFile
        
    
    def get(self):
        return self.data



def addDataJsonFile(dataAdd):
    """
    fonction pour ajouter des valeurs dans un fichier json
    """

    dataFile = readJsonFile(paths / "../../data/data.json").get()
    dataFile["score"].append(dataAdd)

    with open(paths / "../../data/data.json", 'w') as json_file:
        json.dump(dataFile, json_file, indent=4)