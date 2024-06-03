import firebase_admin
from firebase_admin import credentials, firestore
from random import choice
from pathlib import Path

paths = Path(__file__).parent.resolve()


cred = credentials.Certificate(paths / "key.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()



class joinGroup:
    def __init__(self, token):
        try:
            self.token = token
            
            self.report = False
            self.join_group()

        except Exception as e:
            print(f"Error during initialization: {e}")
    
    def join_group(self):
        ref = db.collection('Duo').document(self.token.upper())
        document = ref.get()

        if document.exists:
            ref.update({"connexion": True})
            self.report = True
        else:
            self.report = False



class createGroup:
    def __init__(self):
        try:
            characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            self.id = '-'.join(''.join(choice(characters) for _ in range(3)) for _ in range(3))

            ref = db.collection('Duo').document(self.id)
            ref.set({
                "connexion": False, 
                "score": [0, 0], 
                "question": {},
                "listQuestion": {}
            })

            self.report = False
            ref.on_snapshot(self.on_snapshot)
        except Exception as e:
            print(f"Error during initialization: {e}")
        
    def on_snapshot(self, doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'MODIFIED':
                doc = change.document.to_dict()
                if doc.get('connexion') is True:
                    self.report = True



class connexionPortail:
    def __init__(self, token):
        try:
            self.token = token
            
            self.report = False
            self.join_group()

        except Exception as e:
            print(f"Error during initialization: {e}")
    
    def join_group(self):
        ref = db.collection('Portail').document(self.token.upper())
        document = ref.get()

        if document.exists:
            ref.update({"connexion": True})
            self.report = True
        else:
            self.report = False



class storageQuestion:
    def __init__(self, token, data, list):
        self.token = token
        self.data = data
        self.list = list

        self.ref = db.collection('Duo').document(self.token.upper())

        document = self.ref.get()

        if document.exists:
            self.ref.update({"question": self.data, "listQuestion": self.list})
            self.report = True
        else:
            self.report = False



class loadQuestion:
    def __init__(self, token):
        self.token = token
        self.question, self.listQuestion = [], []
        self.ref = db.collection('Duo').document(self.token.upper())
        self.load()
    
    def load(self):
        document = self.ref.get()
        if document.exists:
            data = document.to_dict()
            self.question = data['question']
            self.listQuestion = data['listQuestion']



class userPoints:
    def __init__(self, user, token):
        self.user = user
        self.token = token
        
    def set(self, addPoints):
        ref = db.collection('Duo').document(self.token.upper())
        document = ref.get()

        if document.exists:
            data = document.to_dict()
            data['score'][self.user - 1] += addPoints
            
            ref.set(data)
    
    def get(self):
        ref = db.collection('Duo').document(self.token.upper())
        document = ref.get()

        if document.exists:
            data = document.to_dict()
            return [data['score'][0], data['score'][0]]