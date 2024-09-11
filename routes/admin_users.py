import bcrypt
from flask import Blueprint, request, jsonify 
from sqlalchemy import or_
from config.database import User, Role, UserRole,Order,UserRoleEnum, SessionLocal

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/admins/users', methods=['GET'])
def index():
    session = SessionLocal()
    if request.user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 401
    
    try:
        users = session.query(User).all()
        user_list = [user.to_dict() for user in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@admin_routes.route('/admins/users/<int:userId>', methods=['GET'])
def show(userId):
    session = SessionLocal()

    if request.user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 401
    
    try:
        user = session.query(User).filter_by(userId=userId).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


@admin_routes.route('/admins/users', methods=['POST'])
def create():
    session = SessionLocal()

    if request.user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 401

    user_data = request.get_json()

    roles = user_data.get('role') 

    if not roles or not isinstance(roles, list):
        return jsonify({'error': 'Roles cannot be empty. Please provide at least one valid role.'}), 400
    
    invalid_roles = [role for role in roles if role not in UserRoleEnum.__members__]
    if invalid_roles:
        return jsonify({'error': f"Invalid roles: {', '.join(invalid_roles)}"}), 400
    
    for role_name in set(roles):  
        set_role = session.query(Role).filter_by(role=UserRoleEnum[role_name]).first()

        if role_name == 'shipper' and 'driver' in roles:
            return jsonify({'error': 'A user cannot be both a shipper and a driver'}), 400
    


    password = user_data.get('password')
    confirm_password = user_data.get('confirmPassword')

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    try:
        existing_user = session.query(User).filter_by(email=user_data.get('email')).first()

        if existing_user:
            return jsonify({'error': 'User already exists'}), 400

        new_user = User(
            username=user_data.get('username'),
            email=user_data.get('email'),
            password=bcrypt.hashpw(user_data.get('password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            verifiedUser=True
        )
        session.add(new_user)
        session.commit()

        for role_name in set(roles):  
            set_role = session.query(Role).filter_by(role=UserRoleEnum[role_name]).first()
            # make that you can't create a user with the role of shipper and driver

            if role_name == 'shipper' and 'driver' in roles:
                return jsonify({'error': 'A user cannot be both a shipper and a driver'}), 400
            if set_role:
                user_role = UserRole(userId=new_user.userId, roleId=set_role.roleId)
                session.add(user_role)
            else:
                return jsonify({'error': f'Role {role_name} not found'}), 400

        session.commit()

        return jsonify({
            'userId': new_user.userId,
            'username': new_user.username,
            'email': new_user.email,
            'verifiedUser': new_user.verifiedUser
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()


        
@admin_routes.route('/admins/users/<int:userId>', methods=['PUT'])
def update(userId):
    session = SessionLocal()

    if request.user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 401

    try:
        user = session.query(User).filter_by(userId=userId).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_data = request.get_json()

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

        if 'verifiedUser' in user_data:
            user.verifiedUser = user_data.get('verifiedUser')

        if 'roles' in user_data:
            roles = user_data.get('roles')
            if not roles:
                return jsonify({'error': 'Roles cannot be empty'}), 400
            if len(roles) != len(set(roles)):
                return jsonify({'error': 'Duplicate roles are not allowed'}), 400

            invalid_roles = [role for role in roles if role not in UserRoleEnum.__members__]
            if invalid_roles:
                return jsonify({'error': f"Invalid roles: {', '.join(invalid_roles)}."}), 400
            
            for role_name in set(roles):
                if role_name == 'shipper' and 'driver' in roles:
                    return jsonify({'error': 'A user cannot be both a shipper and a driver'}), 400
                
            for user_role in user.roles:
                session.delete(user_role)

            for role_name in roles:
                role = session.query(Role).filter_by(role=role_name).first()
                if role:
                    user_role = UserRole(userId=user.userId, roleId=role.roleId)
                    session.add(user_role)
                else:
                    return jsonify({'error': f'Role {role_name} does not exist'}), 400

        session.commit()

        return jsonify(user.to_dict()), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()



@admin_routes.route('/admins/users/<int:userId>', methods=['DELETE'])
def delete(userId):
    session = SessionLocal()

    if request.user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 401

    try:
        user = session.query(User).filter_by(userId=userId).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_roles = session.query(UserRole).filter_by(userId=userId).all()
        for user_role in user_roles:
            session.delete(user_role)
        
        orders = session.query(Order).filter(or_(Order.customerId == userId, Order.driverId == userId)).all()
        for order in orders:
            session.delete(order)
        session.delete(user)
        session.commit()

        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': f'Opps something went wrong: {str(e)}'}), 400
    finally:
        session.close()
