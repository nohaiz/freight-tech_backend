#  IMPORTS

from flask import Blueprint , request, jsonify

#  MODEL

from config.database import Order, session

# EXPORT ROUTES

order_routes = Blueprint('order_routes',__name__)

@order_routes.route('/orders', methods=['POST'])

def create_order():
  try:      
    order_data = request.get_json()
    new_order = Order(
      customerId = validate_date({'customerId':order_data.get('customerId')}) ,
      driverId = validate_date({'driverId':order_data.get('driverId')}),
      pickupLocation = validate_date({'pickupLocation':order_data.get('pickupLocation')}),
      dropoffLocation = validate_date({'dropoffLocation':order_data.get('dropoffLocation')}),
      orderStatus = validate_date({'orderStatus':order_data.get('orderStatus')}),
      paymentAmount = validate_date({'paymentAmount':order_data.get('paymentAmount')}),
      vehicleType = validate_date({'vehicleType':order_data.get('vehicleType')}),
      dimensions = validate_date({'dimensions':order_data.get('dimensions')}),
      weightValue = validate_date({'weightValue':order_data.get('weightValue')}),
      deliveryTime = validate_date({'deliveryTime':order_data.get('deliveryTime')})
    )
    print(new_order)
    session.add(new_order)
    session.commit()

    return jsonify(order_data), 201
  except Exception as e:
    return(e), 400
  
def validate_date(data):

  customerId = data.get(['customerId'])
  driverId = data.get(['driverId'])
  pickupLocation = data.get(['pickupLocation'])
  dropoffLocation = data.get(['dropoffLocation'])
  orderStatus = data.get(['orderStatus'])
  paymentAmount = data.get(['paymentAmount'])
  vehicleType = data.get(['vehicleType'])
  dimensions = data.get(['dimensions'])
  weightValue = data.get(['weightValue'])
  deliveryTime = data.get(['deliveryTime'])

  if not all([customerId, driverId, pickupLocation, dropoffLocation, orderStatus, paymentAmount, vehicleType, dimensions, weightValue, deliveryTime]):
    return jsonify({"error": 'Request cannot be processed due to incomplete data.'}), 400
  
  # for key in data:
  #   return data[key]

