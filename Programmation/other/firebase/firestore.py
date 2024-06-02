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
            ref = db.collection('Duo').document(str(self.token.upper()))
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
                'connexion': False
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
