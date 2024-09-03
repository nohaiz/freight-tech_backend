# IMPORT

from flask import Flask
from flask_cors import CORS


# INITIALIZE FLASK

app = Flask(__name__)
CORS(app)

# ROUTE

@app.route('/')
def index():
  return 'Successful connection'


# RUN APPLICATION 

app.run()