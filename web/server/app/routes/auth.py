from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            'code': 400,
            'msg': 'Username and password are required'
        }), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'code': 400,
            'msg': 'Username already exists'
        }), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data.get('email'),
        role=data.get('role', 'user')  # Default role is 'user'
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': 'User registered successfully',
        'data': user.to_dict()
    })

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Debug logging
    print(f"[DEBUG] Received data: {data}")
    print(f"[DEBUG] Content-Type: {request.content_type}")
    
    if not data or not data.get('username') or not data.get('password'):
        print(f"[DEBUG] Missing username or password")
        return jsonify({
            'code': 400,
            'msg': 'Username and password are required'
        }), 400
    
    username = data['username']
    password = data['password']
    print(f"[DEBUG] Looking for user: {username}")
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        print(f"[DEBUG] User not found: {username}")
        return jsonify({
            'code': 401,
            'msg': 'Invalid username or password'
        }), 401
    
    print(f"[DEBUG] User found, checking password...")
    password_valid = user.check_password(password)
    print(f"[DEBUG] Password valid: {password_valid}")
    
    if not password_valid:
        return jsonify({
            'code': 401,
            'msg': 'Invalid username or password'
        }), 401
    
    # Convert user.id to string for JWT
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'code': 200,
        'msg': 'Login successful',
        'data': {
            'token': access_token,
            'user': user.to_dict()
        }
    })

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'code': 404,
            'msg': 'User not found'
        }), 404
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': user.to_dict()
    })

