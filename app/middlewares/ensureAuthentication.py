from functools import wraps
from flask import request, jsonify
import jwt
from app import key

def verifyToken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers.get('Authorization').split()[1]
            jwt.decode(token, key, algorithms=["HS256"])
        
        except:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(*args, **kwargs)
    
    return decorated