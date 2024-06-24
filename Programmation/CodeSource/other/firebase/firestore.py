import firebase_admin
from firebase_admin import credentials, firestore
from random import choice
from pathlib import Path
from logzero import logger

paths = Path(__file__).parent.resolve()


"Connexion à la base de données Firebase"
cred = credentials.Certificate(paths / "key.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()



class joinGroup:
    """
        Classe permettant de connecter le joueur invité au groupe via la base de données
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
        Classe permettant de créer le groupe dans la base de données pour que le joueur invité puisse rejoindre
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
            self.listener = ref.on_snapshot(self.on_snapshot)
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
        

    "Attendre une notification de la base de données (attendre la modification)"
    def on_snapshot(self, doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'MODIFIED':
                doc = change.document.to_dict()
                if doc.get('connexion') is True:
                    self.report = True
    
    "Arreter d'attendre une notification de la base de données"
    def stop_listening(self):
        logger.warn("Stop listening")
        self.listener.unsubscribe()



class connexionPortail:
    """
        Classe permettant de connecter le portail à la base de données
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
        Classe permettant de stocker les questions du joueur hôte dans la base de données lors du jeu à deux (Duo)
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
        Classe permettant de stocker les questions du joueur hôte dans la base de données lors du jeu à deux (Duo)
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
        Classe permettant de modifier les points et de récupérer les points des joueurs lors d'un jeu à deux (Duo)
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
                return [data['score'][0], data['score'][1]]
        except:
            logger.warn("Connection token not found")



class endGame:
    """
        Classe permettant d'écrire dans la base de données que le joueur a fini de répondre aux questions
        pour l'indiquer à l'autre joueur
    """

    def __init__(self, token, user):
        self.token = token
        self.user = user

        try:
            ref = db.collection('Duo').document(self.token.upper())
            document = ref.get()

            if document.exists:
                data = document.to_dict()
                data['progress'][self.user - 1] = 1
                
                ref.set(data)
                self.report = True
            else:
                self.report = False
        except:
            logger.warn("Connection token not found")


class waitEnd:
    """
        Classe permettant de vérifier si les deux joueurs ont fini. Si ce n'est pas le cas,
        attendre la notification de la base de données pour indiquer la fin de l'autre joueur.
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
            else:
                self.report = False
            
            self.listener = ref.on_snapshot(self.on_snapshot)
        except:
            logger.warn("Connection token not found")
        

    "Attendre une notification de la base de données (attendre la modification)"
    def on_snapshot(self, doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'MODIFIED':
                doc = change.document.to_dict()
                if doc.get('progress') == [1, 1]:
                    self.report = True
                
    "Arreter d'attendre une notification de la base de données"
    def stop_listening(self):
        logger.warn("Stop listening")
        self.listener.unsubscribe()



class storageQuestionPortail:
    """
        Classe permettant de stocker les questions pour le portail
    """

    def __init__(self, token, data, list, progress):
        self.token = token
        self.data = data
        self.progress = progress
        self.list = list

        self.ref = db.collection('Portail').document(self.token.upper())

        document = self.ref.get()

        if document.exists:
            self.ref.update({"question": self.data, "listQuestion": self.list, "progress": self.progress})
            self.report = True
        else:
            self.report = False



class portailNotify:
    """
        Classe permettant de vérifier s'il y a eu une interaction avec le portail
    """

    def __init__(self, token, currentQuestion):
        self.token = token
        self.currentQuestion = currentQuestion
        self.report = 0

        try:
            ref = db.collection('Portail').document(self.token.upper())
            document = ref.get()

            if document.exists:
                data = document.to_dict()
                self.report = data["progress"][self.currentQuestion]
            else:
                self.report = 0
            
            self.listener = ref.on_snapshot(self.on_snapshot)
        except:
            logger.warn("Connection token not found")
        

    "Attendre une notification de la base de données (attendre la modification)"
    def on_snapshot(self, doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'MODIFIED':
                doc = change.document.to_dict()
                self.report = doc["progress"][self.currentQuestion]
    
    "Arreter d'attendre une notification de la base de données"
    def stop_listening(self):
        logger.warn("Stop listening")
        self.listener.unsubscribe()