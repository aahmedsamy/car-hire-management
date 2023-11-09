# src/routes/auth_routes.py
from functools import wraps

from flask import Blueprint, request, jsonify, session
from database import query_db, execute_db
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def requires_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized access'}), 401
        return func(*args, **kwargs)

    return decorated


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Both username and password are required'}), 400

    # Check if the username is already taken
    existing_user = query_db("SELECT * FROM User WHERE username = %s", (username,))
    print(existing_user)
    if existing_user:
        return jsonify({'message': 'Username is already taken'}), 409

    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password)

    # Insert the user into the database
    query = "INSERT INTO User (username, password) VALUES (%s, %s)"
    execute_db(query, (username, hashed_password))

    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Both username and password are required'}), 400

    user = query_db("SELECT * FROM User WHERE username = %s", (username,))
    user = user[0] if user else None
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['UserID']
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200
