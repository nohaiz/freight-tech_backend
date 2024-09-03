# IMPORT

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# IMPORT DATABASE CONNECTION

from config.database import get_db_connection

# INITIALIZE FLASK

app = Flask(__name__)
CORS(app)

# ROUTE

@app.route('/')
def index():
  return 'Successful connection'


# RUN APPLICATION 

app.run()