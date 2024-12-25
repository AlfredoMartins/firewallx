from flask import Flask
from flask_cors import CORS
from config.config import Config
from dotenv import load_dotenv
from middlewares.custom_middleware import CustomMiddleware

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.wsgi_app = CustomMiddleware(app.wsgi_app)
app.config['SECRET_KEY'] = 'secret!'

CORS(app, origins=["http://localhost:5173", "http://192.168.1.77:5173"], supports_credentials=True)

# Load Firewall and Config
from firewall import Firewall
firewall = Firewall()

# Load environment config
config = Config().dev_config
app.env = config.ENV  # Set app environment

# Register API blueprint
from routes.api import api
app.register_blueprint(api, url_prefix="/api")