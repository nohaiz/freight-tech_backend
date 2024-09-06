#  IMPORTS
from sqlalchemy import or_
from flask import Blueprint , request, jsonify

#  MODEL

from config.database import Order,OrderStatusEnum, SessionLocal

# EXPORTED FUNCTION

from utils.validate_data import validate_date

# EXPORT ROUTES

driver_order_routes = Blueprint('driver_order_routes',__name__)
session = SessionLocal()

@driver_order_routes.route('/drivers/orders')


def index():
  try:
    orders = session.query(Order).filter(
    or_(
        Order.driverId == request.user.get('userId'),
        Order.driverId == None)).all()
    if not orders:
      return jsonify({'error': 'Order not found'}), 404
    
    order_list = [order.to_dict() for order in orders ]
    return jsonify(order_list),200      
  
  except Exception as e: 
    session.rollback()
    return jsonify({'error': str(e)}), 400
  finally:
      session.close()

@driver_order_routes.route('/drivers/orders/<id>', methods=['GET'])

def show(id):
  try:
      order = session.query(Order).filter_by(orderId=id).first()
      if  request.user.get('userId') == order.driverId:
        if not order:
          return jsonify({'error': 'Order not found'}), 404        
        return jsonify(order.to_dict())
      elif order.driverId is None:
        return jsonify(order.to_dict())          
      else:
        return jsonify({"error": 'Opps something went wrong'}),400  
  except Exception as e:
    session.rollback() 
    return jsonify({'error': str(e)}), 400
  finally:
      session.close()

@driver_order_routes.route('/drivers/orders/<id>', methods=['PUT'])
def update(id):
    try:
        order = session.query(Order).filter_by(orderId=id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order_data = request.get_json()
        validate_result = validate_date(order_data)
        
        if validate_result.get('error'):
            return jsonify({'error': validate_result.get('message')}), 400
        
        if request.user.get('userId') == order.driverId:

          if order.orderStatus == OrderStatusEnum.completed:
            return jsonify({"error": "The order is completed; Changes can not be made to this order."}), 400
          order.orderStatus = order_data.get('orderStatus')

        elif order.driverId is None:
            
            if order.orderStatus != OrderStatusEnum.pending:
              return jsonify({"error": "The order is unclaimed; please set the order status to 'pending'."}), 400
            order.driverId = request.user.get('userId')
            order.orderStatus = OrderStatusEnum.pending

        else:
          return jsonify({"error": 'Opps something went wrong'}),400  
        
        session.commit()
        return jsonify(order.to_dict()), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        session.close()
