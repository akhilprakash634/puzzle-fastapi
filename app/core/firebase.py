import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings

cred = credentials.Certificate(settings.get_firebase_credentials())
firebase_admin.initialize_app(cred)

db = firestore.client()