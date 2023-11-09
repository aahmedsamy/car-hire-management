# src/routes/customer_routes.py
from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from src.routes.auth_routes import requires_auth

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')


@customer_bp.route('/add_customer', methods=['POST'])
@requires_auth
def add_customer():
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

    if not name or not email or not phone or not user_id:
        return jsonify({'message': 'user_id, name, email and phone are required'}), 400

    # Check if the customer already exists by email
    existing_user = query_db("SELECT * FROM User WHERE UserID = %s", (user_id,))
    if not existing_user:
        return jsonify({'message': 'User with this user_id does not exist'}), 409

    # Check if the customer already exists by email
    existing_customer = query_db("SELECT * FROM Customers WHERE UserID = %s OR Email = %s OR Phone= %s",
                                 (user_id, email, phone))
    if existing_customer:
        return jsonify({'message': 'Customer with this data already exists'}), 409

    # Add the customer to the database
    query = "INSERT INTO Customers (UserID, Name, Email, Phone) VALUES (%s, %s, %s, %s)"
    execute_db(query, (user_id, name, email, phone))

    return jsonify({'message': 'Customer added successfully'}), 201


@customer_bp.route('/update_customer/<int:customer_id>', methods=['PUT'])
@requires_auth
def update_customer(customer_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

    if not name or not email:
        return jsonify({'message': 'Name and email are required'}), 400

    # Check if the customer exists by ID
    customer = query_db("SELECT * FROM Customers WHERE CustomerID = %s", (customer_id,))
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    # Update the customer's information
    query = "UPDATE Customers SET Name = %s, Email = %s, Phone = %s WHERE CustomerID = %s"
    execute_db(query, (name, email, phone, customer_id))

    return jsonify({'message': 'Customer updated successfully'}), 200


@customer_bp.route('/delete_customer/<int:customer_id>', methods=['DELETE'])
@requires_auth
def delete_customer(customer_id):
    # Check if the customer exists by ID
    customer = query_db("SELECT * FROM Customers WHERE CustomerID = %s", (customer_id,))
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    # Delete the customer
    query = "DELETE FROM Customers WHERE CustomerID = %s"
    execute_db(query, (customer_id,))

    return jsonify({'message': 'Customer deleted successfully'}), 200


@customer_bp.route('/get_customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    # Get customer by ID
    customer = query_db("SELECT * FROM Customers WHERE CustomerID = %s", (customer_id,))
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    return jsonify({'customer': customer}), 200
