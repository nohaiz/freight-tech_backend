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
  
  try:
      paymentAmount = float(paymentAmount)
      if paymentAmount < 0:
          return {'error': True, 'message': 'Data entry is invalid. Payment amount must be a positive number.'}
  except ValueError:
      return {'error': True, 'message': 'Data entry is invalid. Payment amount must be a valid number.'}
  try:
      weightValue = float(weightValue)
      if weightValue < 0:
          return {'error': True, 'message': 'Data entry is invalid. Weight value must be a positive number.'}
  except ValueError:
      return {'error': True, 'message': 'Data entry is invalid. Weight value must be a valid number.'}
  
  return data
