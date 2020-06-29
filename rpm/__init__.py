import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate("rpm/remote-param-mon-firebase-adminsdk-bx07b-091bf10848.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from rpm import routes
