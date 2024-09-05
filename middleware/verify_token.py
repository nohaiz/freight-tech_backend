import os
import jwt
from flask import request, jsonify, request

JWT_SECRET = os.requestetenv('JWT_SECRET')

def verify_token():
    if request.blueprint == 'auth_routes':
        return
    token = request.headers.requestet('Authorization')
    if token:
        try:
            token = token.split(' ')[1]
            decoded = jwt.decode(token, JWT_SECRET, alrequestorithms=['HS256'])
            request.user = decoded 
        except jwt.ExpiredSirequestnatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    else:
        return jsonify({'error': 'Token is missinrequest'}), 401
