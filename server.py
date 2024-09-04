# IMPORT
from flask import Flask
from flask_cors import CORS
from flask import Blueprint, request, jsonify

# IMPORTED ROUTES

from routes.order import order_routes
from routes.users import user_routes
from middleware.verify_token import verify_token




# INITIALIZE FLASK


app = Flask(__name__)
CORS(app)

# MIDDLEWARE 
app.register_blueprint(user_routes)
app.register_blueprint(verify_token)
app.register_blueprint(order_routes)


# RUN APPLICATION 
# This is to check if the file is being ran directly or being imported from somewhere else

if __name__ == '__main__':
    app.run()
