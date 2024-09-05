import os
from flask import Blueprint, request, jsonify
import bcrypt
import jwt
from config.database import User, Role, UserRole, UserRoleEnum, SessionLocal

auth_routes = Blueprint('auth_routes', __name__)

JWT_SECRET = os.getenv('JWT_SECRET')


@auth_routes.route('/auth/sign-up', methods=['POST'])
def signup():
    
    session = SessionLocal()

    try:
        new_user_data = request.get_json()
        username = new_user_data.get('username')
        email = new_user_data.get('email')
        password = new_user_data.get('password')
        confirm_password = new_user_data.get('confirmPassword')
        verifiedUser = new_user_data.get('verifiedUser')

        if not all([username, email, password, confirm_password, verifiedUser is not None]):
            return jsonify({"error": "Incomplete data."}), 400

        if password != confirm_password:
            return jsonify({"error": "Passwords do not match."}), 400

        existing_user = session.query(User).filter((User.email == email)).first()

        if existing_user:
            return jsonify({"error": "Email already exists."}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            verifiedUser=verifiedUser
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        if verifiedUser:
          role_name = UserRoleEnum.shipper
          print(role_name)
        else:
          role_name = UserRoleEnum.driver

        role = session.query(Role).filter_by(role=role_name).first()

        user_role = UserRole(userId=new_user.userId, roleId=role.roleId)

        session.add(user_role)
        session.commit()

        token_payload = {
            'userId': new_user.userId,
            'role': role.role.value,
        }
        token = jwt.encode(token_payload, JWT_SECRET, algorithm='HS256')

        return jsonify({"token": token}), 201

    except Exception as e:
        session.rollback() 
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

@auth_routes.route('/auth/sign-in', methods=['POST'])
def signin():
    
    session = SessionLocal()

    try:
        user_data = request.get_json()
        email = user_data.get('email')
        password = user_data.get('password')

        if not all([email, password]):
            return jsonify({"error": "Incomplete data."}), 400

        user = session.query(User).filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            user_role = session.query(UserRole).filter_by(userId=user.userId).first()
            if user_role:
                role = session.query(Role).filter_by(roleId=user_role.roleId).first()
            else:
                return jsonify({"error": "User role not found."}), 404

            if not role:
                return jsonify({"error": "Role not found."}), 404

            token_payload = {
                'userId': user.userId,
                'role': role.role.value,
            }
            token = jwt.encode(token_payload, JWT_SECRET, algorithm='HS256')

            return jsonify({"token": token}), 200
        
        else:
            return jsonify({"error": "Invalid email or password."}), 401

    except Exception as e:
        return jsonify({"error": "An error occurred during signin."}), 500

    finally:
        session.close()
