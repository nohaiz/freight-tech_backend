import os , jwt
from flask import Blueprint, request, jsonify

JWT_SECRET = os.getenv('JWT_SECRET')

verify_token = Blueprint('verify_token', __name__)

@verify_token.route('/verify-token', methods=['GET'])
def verifyToken():
    token = request.headers.get('Authorization')
    if token:
        try:
            token = token.split(' ')[1]
            decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    else:
        return jsonify({'error': 'Token is missing'}), 401
