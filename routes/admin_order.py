#  IMPORTS
from flask import Blueprint, request, jsonify

#  MODEL

from config.database import Order,User,SessionLocal

# EXPORTED FUNCTION

from utils.validate_data import validate_date

# EXPORT ROUTES

admin_order_routes = Blueprint('admin_order_routes', __name__)
session = SessionLocal()

@admin_order_routes.route('/admin/orders', methods=['GET'])

def index():
    if request.user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 401
    
    try:
        orders = session.query(Order).all()

        if not orders:
            return jsonify({'error': 'Order not found'}), 404
        
        order_list = [order.to_dict() for order in orders]
        return jsonify(order_list), 200
    
    except Exception as e: 
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@admin_order_routes.route('/admin/orders', methods=['POST'])


def create_order():
    if request.user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 401
    
    try:
        order_data = request.get_json()

        validate_result = validate_date(order_data)

        if validate_result.get('error'):
            return jsonify(validate_result.get('message')), 400
        
        customer_user = session.query(User).filter(User.userId == order_data.get('customerId')).first()
        driver_user = session.query(User).filter(User.userId == order_data.get('driverId')).first()

        if not customer_user or not driver_user:
            return jsonify({'error': 'Invalid customer or driver ID'}), 400
        if order_data.get('customerId') != customer_user.userId and order_data.get('driverId') != driver_user.userId:
            return jsonify({'error': 'Invalid customer or driver ID'}), 400
        
        else:    
            new_order = Order(
                customerId=order_data.get('customerId'),
                driverId=order_data.get('driverId'),
                pickupLocation=order_data.get('pickupLocation'),
                dropoffLocation=order_data.get('dropoffLocation'),
                orderStatus=order_data.get('orderStatus'),
                paymentAmount=order_data.get('paymentAmount'),
                vehicleType=order_data.get('vehicleType'),
                dimensions=order_data.get('dimensions'),
                weightValue=order_data.get('weightValue'),
                deliveryTime=order_data.get('deliveryTime')
            )
            session.add(new_order)
            session.commit()
            return jsonify(new_order.to_dict()), 201
    
    except Exception as e:
        session.rollback() 
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@admin_order_routes.route('/admin/orders/<id>', methods=['GET'])

def show(id):
    if request.user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 401
    try:
        order = session.query(Order).filter_by(orderId=id).first()

        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify(order.to_dict()), 200
    
    except Exception as e: 
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@admin_order_routes.route('/admin/orders/<id>', methods=['PUT'])

def update(id):
    if request.user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 401
    
    try:    
        order = session.query(Order).filter_by(orderId=id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order_data = request.get_json()
        validate_result = validate_date(order_data)

        if validate_result.get('error'):
            return jsonify(validate_result.get('message')), 400
        
        customer_user = session.query(User).filter(User.userId == order_data.get('customerId')).first()
        driver_user = session.query(User).filter(User.userId == order_data.get('driverId')).first()

        if not customer_user or not driver_user:
            return jsonify({'error': 'Invalid customer or driver ID'}), 400
        if int(order_data.get('customerId')) != customer_user.userId and int(order_data.get('driverId')) != driver_user.userId:
            return jsonify({'error': 'Wrong assginment for the customer and driver ID'}), 400
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
        
        return jsonify(order.to_dict()), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@admin_order_routes.route('/admin/orders/<id>', methods=['DELETE'])

def delete(id):
    if request.user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 401
    try:
        order = session.query(Order).filter_by(orderId=id).first()

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        session.delete(order)
        session.commit()

        return jsonify("Order deleted successfully"), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()
    
