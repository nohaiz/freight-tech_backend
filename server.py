# IMPORT

from flask import Flask
from flask_cors import CORS

# IMPORTED ROUTES

from routes.order import order_routes


# INITIALIZE FLASK

app = Flask(__name__)
CORS(app)

# MIDDLEWARE

app.register_blueprint(order_routes)

# RUN APPLICATION 
# This is to check if the file is being ran directly or being imported from somewhere else

if __name__ == '__main__':
    app.run()
