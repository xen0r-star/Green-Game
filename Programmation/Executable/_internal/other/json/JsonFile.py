
import os
import json
from jsonschema import validate
from pathlib import Path

paths = Path(__file__).parent.resolve()



class readJsonFileSchema:
    """
        Classe pour lire un fichier JSON selon un schéma, ce qui permet d'avoir un fichier JSON
        avec des données écrites de manière uniforme.
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


data_directory = os.path.expanduser("~\\AppData\\Local\\GreenGenius")
Path(data_directory).mkdir(parents=True, exist_ok=True)
json_file_path = os.path.join(data_directory, "data.json")


def addDataJsonFile(dataAdd):
    """
    fonction pour ajouter des valeurs dans un fichier json
    """

    data_file = readJsonFile(json_file_path).get_data()
    data_file["score"].append(dataAdd)

    with open(json_file_path, 'w') as json_file:
        json.dump(data_file, json_file, indent=4)