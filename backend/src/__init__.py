
from flask import Flask, request, jsonify
from flask_cors import CORS
from config.config import Config

from dotenv import load_dotenv

# loads enviroment variables
load_dotenv()

# API
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, origins=["http://localhost:5173", "http://192.168.1.77:5173"], supports_credentials=True)

# calling the dev configuration
config = Config().dev_config

# setting the API to use dev env
app.env = config.ENV

# import api blueprint to register it with app
from routes.api import api
app.register_blueprint(api, url_prefix="/api")