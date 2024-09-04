#  IMPORTS

from flask import Blueprint , request, jsonify

#  MODEL

from config.database import Order, session

# EXPORTED FUNCTION

from utils.validate_data import validate_date

# EXPORT ROUTES

order_routes = Blueprint('order_routes',__name__)

@order_routes.route('/drivers/orders')

# Currently, the function displays all orders because we don't have a driverId to filter and show only the orders associated with a specific shipper. Eventually, this ID should be retrieved from the verifyToken middleware to enable proper filtering

def index():
  try:
    orders = session.query(Order).all()

    if not orders:
      return jsonify({'error': 'Order not found'}), 404
    
    order_list = [order.to_dict() for order in orders ]
    return jsonify(order_list),200
  
  except Exception as e: 
    return jsonify({'error': str(e)}), 400

@order_routes.route('/drivers/orders/<id>', methods=['GET'])

def show(id):
  try:
    order = session.query(Order).filter_by(orderId=id).first()

    if not order:
      return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(order.to_dict())
  except Exception as e: 
    return jsonify({'error': str(e)}), 400

@order_routes.route('/drivers/orders/<id>', methods=['PUT'])

def update(id):
  try:  

    order = session.query(Order).filter_by(orderId=id).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    order_data = request.get_json()
    validate_result = validate_date(order_data)

    if validate_result.get('error'):
      return jsonify(validate_result.get('message')), 400
    else:
      order.orderStatus = order_data.get('orderStatus') 
    session.commit()

    return jsonify(order.to_dict()), 200  
      
  except Exception as e:
    return jsonify({'error': str(e)}), 400
  