#  IMPORTS

from flask import Blueprint , request, jsonify

#  MODEL

from config.database import Order, session

#  DELEVIRY TIME VALIDATION INCOMPLETE WILL DO LTR
def validate_date(data):
  customerId = data.get('customerId')
  driverId = data.get('driverId')
  pickupLocation = data.get('pickupLocation')
  dropoffLocation = data.get('dropoffLocation')
  orderStatus = data.get('orderStatus')
  paymentAmount = data.get('paymentAmount')
  vehicleType = data.get('vehicleType')
  dimensions = data.get('dimensions')
  weightValue = data.get('weightValue')
  deliveryTime = data.get('deliveryTime')

  if not all([customerId, driverId, pickupLocation, dropoffLocation, orderStatus, paymentAmount, vehicleType, dimensions, weightValue, deliveryTime]):
    return {'error': True , 'message': 'Data entry is invalid. Please fill in all the fields'}
  try:
      customerId = int(customerId)
      driverId = int(driverId)
  except ValueError:
      return {'error': True, 'message': 'Data entry is invalid. Customer ID and Driver ID must be valid integers.'}

  valid_statuses = {'pending', 'completed', 'on-going'}
  if orderStatus not in valid_statuses:
    return {'error': True , 'message': 'Data entry is invalid. Order status is invalid'}

  valid_vehicle_types = {'car', 'truck', 'van'}
  if vehicleType not in valid_vehicle_types:
    return {'error': True , 'message': 'Data entry is invalid. Vehicle type is invalid'}

  if not isinstance(paymentAmount, (float, int)) or paymentAmount < 0:
      return {'error': True, 'message': 'Data entry is invalid. Payment amount must be a positive number.'}
  
  if not isinstance(weightValue, (float, int)) or weightValue < 0:
      return {'error': True, 'message': 'Data entry is invalid. Weight value must be a positive number.'}
  
  return data

# EXPORT ROUTES

order_routes = Blueprint('order_routes',__name__)

@order_routes.route('/orders', methods=['POST'])

def create_order():
  try:      
    order_data = request.get_json()

    validate_result = validate_date(order_data)
    print(validate_result) 
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
