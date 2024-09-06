#  IMPORTS

from flask import Blueprint, request, jsonify

#  MODEL

from config.database import Order,OrderStatusEnum, SessionLocal

# EXPORTED FUNCTION

from utils.validate_data import validate_date

# EXPORT ROUTES

admin_order_routes = Blueprint('admin_order_routes', __name__)

@admin_order_routes.route('/admin/orders', methods=['GET'])

def index():
    session = SessionLocal()
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
    session = SessionLocal()
    try:
        order_data = request.get_json()

        validate_result = validate_date(order_data)

        if validate_result.get('error'):
            return jsonify(validate_result.get('message')), 400
        
        # Admin can create orders with whatever status

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
    session = SessionLocal()
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
    session = SessionLocal()
    try:
        
        order = session.query(Order).filter_by(orderId=id).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order_data = request.get_json()
        validate_result = validate_date(order_data)

        if validate_result.get('error'):
            return jsonify(validate_result.get('message')), 400

        # Admin can update any field
        order.pickupLocation = order_data.get('pickupLocation')
        order.dropoffLocation = order_data.get('dropoffLocation')
        order.vehicleType = order_data.get('vehicleType')
        order.dimensions = order_data.get('dimensions')
        order.weightValue = order_data.get('weightValue')
        order.orderStatus = order_data.get('orderStatus')
        session.commit()
        
        return jsonify(order.to_dict()), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@admin_order_routes.route('/admin/orders/<id>', methods=['DELETE'])

def delete(id):
    session = SessionLocal()
    try:
        order = session.query(Order).filter_by(orderId=id).first()

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Admin can delete any order, no status check needed
        session.delete(order)
        session.commit()

        return jsonify("Order deleted successfully"), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()
    
