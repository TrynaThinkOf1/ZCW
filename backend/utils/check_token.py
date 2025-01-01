from flask import request, jsonify
from itsdangerous import BadSignature, SignatureExpired
from functools import wraps

def check_token(serializer):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session_token = request.cookies.get('zcw_secure_token')
            if not session_token:
                print("session token missing")
                return jsonify({"message": "Session invalid, please login again"}), 401
            try:
                serializer.loads(session_token, salt="session-token", max_age=36 * 3600)
            except SignatureExpired:
                print("session token expired")
                return jsonify({"message": "Session expired, please login again"}), 401
            except BadSignature:
                print("session token invalid")
                return jsonify({"message": "Session invalid, please login again"}), 401
            return func(*args, **kwargs)
        return wrapper
    return decorator
