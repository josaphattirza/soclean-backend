from flask import Flask
from config import Config
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

mongo1 = PyMongo(app, "mongodb+srv://rephaelc:rephaelcmongodb@cluster0.oz7vg.mongodb.net/SoClean?retryWrites=true&w=majority")
mongo2 = PyMongo(app, "mongodb://localhost:27017/local")

from app import routes
