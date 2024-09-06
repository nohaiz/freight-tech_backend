from flask import Blueprint, request, jsonify
import bcrypt
from config.database import User, Role, UserRole, UserRoleEnum, SessionLocal

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

@admin_routes.route('/admins/users', methods=['POST'])
def create():
    session = SessionLocal()

    if request.user.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 401

    user_data = request.get_json()
    role = user_data.get('role')
    if role == 'shipper':
        verified_user = True
    elif role == 'driver':
        verified_user = False

    password = user_data.get('password')
    confirm_password = user_data.get('confirmPassword')

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    try:
        if session.query(User).filter_by(username=user_data.get('username')).first():
            return jsonify({'error': 'Username already exists'}), 400

        if session.query(User).filter_by(email=user_data.get('email')).first():
            return jsonify({'error': 'Email already exists'}), 400

        new_user = User(
            username=user_data.get('username'),
            email=user_data.get('email'),
            password=bcrypt.hashpw(user_data.get('password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            verifiedUser=verified_user
        )
        session.add(new_user)

        set_role = session.query(Role).filter_by(role=UserRoleEnum[role]).first()
        if set_role:
            user_role = UserRole(userId=new_user.userId, roleId=set_role.roleId)
            session.add(user_role)
        else:
            return jsonify({'error': 'Role not found'}), 400

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

        session.commit()

        return jsonify({
            'userId': user.userId,
            'username': user.username,
            'email': user.email,
            'verifiedUser': user.verifiedUser
        })

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

        session.delete(user)
        session.commit()

        return jsonify("User deleted successfully"), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()
