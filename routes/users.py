from sqlalchemy import or_
from flask import Blueprint, request, jsonify
from config.database import User,UserRole,Order,OrderStatusEnum,SessionLocal

users_routes = Blueprint('users_routes', __name__)
session = SessionLocal()

@users_routes.route('/users/<int:userId>', methods=['GET'])

def show(userId):
    try:
        if  request.user.get('userId') == userId:
            user = session.query(User).filter_by(userId=userId).first()

            if not user:
                return jsonify({'error': 'User not found'}), 404
            return jsonify({
                'userId': user.userId,
                'username': user.username,
                'email': user.email,
                'verifiedUser': user.verifiedUser
            })
        else: 
            return jsonify({"error": 'Opps something went wrong'}), 400
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@users_routes.route('/users/<int:userId>', methods=['PUT'])
def update(userId):    
    try:
        if  request.user.get('userId') == userId:
            user = session.query(User).filter_by(userId=userId).first()
            user_data = request.get_json()

            if not user:
                return jsonify({'error': 'User not found'}), 404

            if 'username' in user_data:
                new_username = user_data.get('username')

                existing_user = session.query(User).filter(User.username == new_username, User.userId != userId).first()

                if existing_user:
                    return jsonify({'error': 'Username already exists'}), 400
                
                user.username = new_username

            if 'email' in user_data:
                new_email = user_data.get('email')

                existing_user = session.query(User).filter(User.email == new_email, User.userId != userId).first()

                if existing_user:
                    return jsonify({'error': 'Email already exists'}), 400
                
                user.email = new_email
                
            session.commit()

            return jsonify({
                'userId': user.userId,
                'username': user.username,
                'email': user.email,
            })
        else:
            return jsonify({"error": 'Opps something went wrong'}),400 
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

        
@users_routes.route('/users/<int:userId>', methods=['DELETE'])
def delete(userId):
    try:
        if request.user.get('userId') == userId:

            user = session.query(User).filter_by(userId=userId).first()
            if not user:
                return jsonify({'error': 'User not found'}), 404

            user_role = session.query(UserRole).filter_by(userId=userId).first()
            if user_role:
                session.delete(user_role)

            orders = session.query(Order).filter(
                or_(Order.customerId == userId, Order.driverId == userId)
            ).all()
            for order in orders:
                if order.orderStatus == OrderStatusEnum.on_route:
                    return jsonify({"error": 'Cannot delete user with on-route orders'}), 400
                elif order.orderStatus == OrderStatusEnum.pending:
                    if order.driverId is None:
                        session.delete(order)
                    else:
                        order.driverId = None
                        session.commit()
            session.delete(user)
            session.commit()

            return jsonify({'message': 'User deleted successfully'}), 200
        else: 
            return jsonify({"error": 'Opps something went wrong'}),400 

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()