#  IMPORTS

from flask import Blueprint , request, jsonify

#  MODEL

from config.database import Order, session

# EXPORTED FUNCTION

from utils.validate_data import validate_date

# EXPORT ROUTES

order_routes = Blueprint('order_routes',__name__)

@order_routes.route('/orders', methods=['POST'])

def create_order():
  try:      
    order_data = request.get_json()

    validate_result = validate_date(order_data)

    if validate_result.get('error'):
      return jsonify(validate_result.get('message')), 400
    else:
      new_order = Order(
        customerId = order_data.get('customerId'),
        driverId = order_data.get('driverId'),
        pickupLocation = order_data.get('pickupLocation'),
        dropoffLocation = order_data.get('dropoffLocation'),
        orderStatus = order_data.get('orderStatus'),
        paymentAmount = order_data.get('paymentAmount'),
        vehicleType = order_data.get('vehicleType'),
        dimensions = order_data.get('dimensions'),
        weightValue = order_data.get('weightValue'),
        deliveryTime = order_data.get('deliveryTime')
      )
      session.add(new_order)
      session.commit()
      return jsonify(order_data), 201
    
  except Exception as e:
    return jsonify({'error': str(e)}), 400
  
@order_routes.route('/orders/<id>', methods=['PUT'])

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
      order.customerId = order_data.get('customerId')
      order.driverId = order_data.get('driverId')
      order.pickupLocation = order_data.get('pickupLocation')
      order.dropoffLocation = order_data.get('dropoffLocation')
      order.orderStatus = order_data.get('orderStatus')
      order.paymentAmount = order_data.get('paymentAmount')
      order.vehicleType = order_data.get('vehicleType') 
      order.dimensions = order_data.get('dimensions')
      order.weightValue = order_data.get('weightValue')
      order.deliveryTime = order_data.get('deliveryTime')
    session.commit()

    order_dict = {
            'orderId': order.orderId,
            'customerId': order.customerId,
            'driverId': order.driverId,
            'pickupLocation': order.pickupLocation,
            'dropoffLocation': order.dropoffLocation,
            'orderStatus': order.orderStatus.value,
            'paymentAmount': order.paymentAmount,
            'vehicleType': order.vehicleType.value,
            'dimensions': order.dimensions,
            'weightValue': order.weightValue,
            'deliveryTime': order.deliveryTime
        }
    return jsonify(order_dict), 200  
      
  except Exception as e:
    return jsonify({'error': str(e)}), 400
  
@order_routes.route('/orders/<id>', methods=['DELETE'])

def delete(id): 
  try:  
    order = session.query(Order).filter_by(orderId=id).first()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    session.delete(order)
    session.commit()

    return jsonify("Order deleted successfully"),200
  except Exception as e:
    return jsonify({'error': str(e)}), 400
