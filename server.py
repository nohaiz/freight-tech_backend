from flask import Flask
from flask_cors import CORS

# Import your middleware and routes
from middleware.verify_token import verify_token
from routes.users import auth_routes
from routes.shippers_order import shipper_order_routes
from routes.drivers_order import driver_order_routes

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Register the global middleware
app.before_request(verify_token)

# Register blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(shipper_order_routes)
app.register_blueprint(driver_order_routes)

# Run the application
if __name__ == '__main__':
    app.run()
