#  IMPORTS

from flask import Blueprint , request, jsonify

#  MODEL

from config.database import Order, session

# EXPORTED FUNCTION

from utils.validate_data import validate_date

# EXPORT ROUTES

order_routes = Blueprint('order_routes',__name__)

@order_routes.route('/shippers/orders')

# Currently, the function displays all orders because we don't have a shipperId or customerId to filter and show only the orders associated with a specific shipper. Eventually, this ID should be retrieved from the verifyToken middleware to enable proper filtering

def index():
  try:
    orders = session.query(Order).all()

    if not orders:
      return jsonify({'error': 'Order not found'}), 404
    
    order_list = [order.to_dict() for order in orders ]
    return jsonify(order_list),200
  
  except Exception as e: 
    return jsonify({'error': str(e)}), 400

@order_routes.route('/shippers/orders', methods=['POST'])

# This function requires a shipperId or customerId to create a new order. For the time being, I manually pass the required ID, but ideally, it should be retrieved through the verifyToken middleware.

def create_order():
  try:      
    order_data = request.get_json()

    validate_result = validate_date(order_data)

    if validate_result.get('error'):
      return jsonify(validate_result.get('message')), 400
    if order_data.get('orderStatus') != 'pending':
        return jsonify({'error': 'Invalid status for shipper'}), 400
    
    else:
      new_order = Order(
        customerId = order_data.get('customerId'),
        driverId = order_data.get('driverId'),
        pickupLocation = order_data.get('pickupLocation'),
        dropoffLocation = order_data.get('dropoffLocation'),
        orderStatus = 'pending',
        paymentAmount = order_data.get('paymentAmount'),
        vehicleType = order_data.get('vehicleType'),
        dimensions = order_data.get('dimensions'),
        weightValue = order_data.get('weightValue'),
        deliveryTime = order_data.get('deliveryTime')
      )
      session.add(new_order)
      session.commit()
      return jsonify(new_order.to_dict()), 201
    
  except Exception as e:
    return jsonify({'error': str(e)}), 400
  
@order_routes.route('/shippers/orders/<id>', methods=['GET'])

def show(id):
  try:
    order = session.query(Order).filter_by(orderId=id).first()

    if not order:
      return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(order.to_dict())
  except Exception as e: 
    return jsonify({'error': str(e)}), 400

@order_routes.route('/shippers/orders/<id>', methods=['PUT'])

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
      order.pickupLocation = order_data.get('pickupLocation')
      order.dropoffLocation = order_data.get('dropoffLocation')
      order.vehicleType = order_data.get('vehicleType') 
      order.dimensions = order_data.get('dimensions')
      order.weightValue = order_data.get('weightValue')
    session.commit()

    return jsonify({'pickupLocation' : order.pickupLocation, 'dropoffLocation': order.dropoffLocation, 'vehicleType': order.vehicleType.value, 'dimensions': order.dimensions, 'weightValue': order.weightValue}), 200  
      
  except Exception as e:
    return jsonify({'error': str(e)}), 400
  
@order_routes.route('/shippers/orders/<id>', methods=['DELETE'])

def delete(id): 
  try:  
    order = session.query(Order).filter_by(orderId=id).first()

    if not order:
        return jsonify({'error': 'Order not found'}), 404
    if order.orderStatus != 'on-route':
      session.delete(order)
      session.commit()

    return jsonify("Order deleted successfully"),200
  except Exception as e:
    return jsonify({'error': str(e)}), 400
