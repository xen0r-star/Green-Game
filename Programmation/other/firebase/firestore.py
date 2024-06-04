import firebase_admin
from firebase_admin import credentials, firestore
from random import choice
from pathlib import Path
from logzero import logger

paths = Path(__file__).parent.resolve()


"connexion a la basse de donnée FireBase"
cred = credentials.Certificate(paths / "key.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()



class joinGroup:
    """
    class permettant de connecter le joueur invitée au groupe avec la base de donnée
    """

    def __init__(self, token):
        try:
            self.token = token
            
            self.report = False
            self.join_group()

        except Exception as e:
            logger.error(f"Error during initialization: {e}")
    

    def join_group(self):
        try:
            ref = db.collection('Duo').document(self.token.upper())
            document = ref.get()

            if document.exists:
                ref.update({"connexion": True})
                self.report = True
            else:
                self.report = False
        except:
            logger.warn("Connection token not found")



class createGroup:
    """
    class permettant de crée le groupe dans la base de donnée pour que le joueur invitée rejoins 
    """

    def __init__(self):
        try:
            characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            self.id = '-'.join(''.join(choice(characters) for _ in range(3)) for _ in range(3)) # crée le token xxx-xxx-xxx

            ref = db.collection('Duo').document(self.id)
            ref.set({
                "connexion": False, 
                "score": [0, 0], 
                "question": {},
                "listQuestion": {},
                "progress": [0, 0]
            })

            self.report = False
            ref.on_snapshot(self.on_snapshot)
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
        

    "notification de la base"
    def on_snapshot(self, doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'MODIFIED':
                doc = change.document.to_dict()
                if doc.get('connexion') is True:
                    self.report = True



class connexionPortail:
    """
    class permettant de connecter le portail au la base de donnée
    """

    def __init__(self, token):
        try:
            self.token = token
            
            self.report = False
            self.join_group()

        except Exception as e:
            logger.error(f"Error during initialization: {e}")
    

    def join_group(self):
        try:
            ref = db.collection('Portail').document(self.token.upper())
            document = ref.get()

            if document.exists:
                ref.update({"connexion": True})
                self.report = True
            else:
                self.report = False
        except:
            logger.warn("Connection token not found")



class storageQuestion:
    """
    class permettant de stockée les question du joueur hote dans la base de donnée lors du jeux a 2 (Duo)
    """

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
    """
    class permettant de stockée les question du joueur hote dans la base de donnée lors du jeux a 2 (Duo)
    """

    def __init__(self, token):
        try:
            self.token = token
            self.question, self.listQuestion = [], []
            self.ref = db.collection('Duo').document(self.token.upper())
            self.load()
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
    
    
    def load(self):
        try:
            document = self.ref.get()
            if document.exists:
                data = document.to_dict()
                self.question = data['question']
                self.listQuestion = data['listQuestion']
        except:
            logger.warn("Connection token not found")



class userPoints:
    """
    class permettant de modifier les point et recuperer les point des joueur lors d'un jeux a deux (Duo)
    """

    def __init__(self, user, token):
        self.user = user
        self.token = token
        
    
    def set(self, addPoints):
        try:
            ref = db.collection('Duo').document(self.token.upper())
            document = ref.get()

            if document.exists:
                data = document.to_dict()
                data['score'][self.user - 1] += addPoints
                
                ref.set(data)
        except:
            logger.warn("Connection token not found")
    
    
    def get(self):
        try:
            ref = db.collection('Duo').document(self.token.upper())
            document = ref.get()

            if document.exists:
                data = document.to_dict()
                return [data['score'][0], data['score'][0]]
        except:
            logger.warn("Connection token not found")



class endGame:
    def __init__(self, token, user):
        self.token = token
        self.user = user

        try:
            ref = db.collection('Duo').document(self.token.upper())
            document = ref.get()

            if document.exists:
                ref.update({"progress": []})
                self.report = True
            else:
                self.report = False
        except:
            logger.warn("Connection token not found")


class waitEnd:
    """
    class permets de verifier si les deux joueur on finie et si non attendre la fin des deux
    """

    def __init__(self, token):
        self.token = token
        self.report = False


        try:
            ref = db.collection('Duo').document(self.token.upper())
            document = ref.get()

            if document.exists:
                data = document.to_dict()
                if data["progress"] == [1, 1]:
                    self.report = True
        except:
            logger.warn("Connection token not found")
        

    "notification de la base"
    def on_snapshot(self, doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'MODIFIED':
                doc = change.document.to_dict()
                if doc.get('progress') == [1, 1]:
                    self.report = True