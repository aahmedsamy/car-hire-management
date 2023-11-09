# src/routes/vehicle_routes.py
from flask import Blueprint, request, jsonify
from src.routes.auth_routes import requires_auth
from database import query_db, execute_db

vehicle_bp = Blueprint('vehicle', __name__, url_prefix='/vehicle')


@vehicle_bp.route('/add_vehicle', methods=['POST'])
@requires_auth
def add_vehicle():
    data = request.get_json()
    vehicle_type_id = data.get('vehicle_type_id')
    price = data.get('price')

    if not vehicle_type_id or not price:
        return jsonify({'message': 'Vehicle type and price are required'}), 400

    # Check if the vehicle type exists
    vehicle_type = query_db("SELECT * FROM VehicleTypes WHERE VehicleTypeID = %s", (vehicle_type_id,))
    if not vehicle_type:
        return jsonify({'message': 'Vehicle type not found'}), 404

    # Add the vehicle to the database
    query = "INSERT INTO Vehicles (VehicleTypeID, Price) VALUES (%s, %s)"
    execute_db(query, (vehicle_type_id, price))

    return jsonify({'message': 'Vehicle added successfully'}), 201


@vehicle_bp.route('/update_vehicle/<int:vehicle_id>', methods=['PUT'])
@requires_auth
def update_vehicle(vehicle_id):
    data = request.get_json()
    price = data.get('price')
    availability = data.get('availability')

    if not price:
        return jsonify({'message': 'Price is required'}), 400

    # Check if the vehicle exists
    vehicle = query_db("SELECT * FROM Vehicles WHERE VehicleID = %s", (vehicle_id,))
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404

    # Update the vehicle information
    query = "UPDATE Vehicles SET Price = %s, Availability = %s WHERE VehicleID = %s"
    execute_db(query, (price, availability, vehicle_id))

    return jsonify({'message': 'Vehicle updated successfully'}), 200


@vehicle_bp.route('/delete_vehicle/<int:vehicle_id>', methods=['DELETE'])
@requires_auth
def delete_vehicle(vehicle_id):
    # Check if the vehicle exists
    vehicle = query_db("SELECT * FROM Vehicles WHERE VehicleID = %s", (vehicle_id,))
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404

    # Delete the vehicle
    query = "DELETE FROM Vehicles WHERE VehicleID = %s"
    execute_db(query, (vehicle_id,))

    return jsonify({'message': 'Vehicle deleted successfully'}), 200


@vehicle_bp.route('/get_vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    # Get vehicle information by ID
    vehicle = query_db("SELECT * FROM Vehicles WHERE VehicleID = %s", (vehicle_id,))
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404

    return jsonify({'vehicle': vehicle}), 200
