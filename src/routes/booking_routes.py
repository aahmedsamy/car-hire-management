# src/routes/booking_routes.py
from flask import Blueprint, request, jsonify
from database import get_db, close_db, query_db, execute_db

booking_bp = Blueprint('booking', __name__,  url_prefix='/booking')


@booking_bp.route('/add_booking', methods=['POST'])
def add_booking():
    data = request.get_json()
    customer_id = data.get('customer_id')
    vehicle_id = data.get('vehicle_id')
    date_of_hire = data.get('date_of_hire')
    return_date = data.get('return_date')

    if not customer_id or not vehicle_id or not date_of_hire or not return_date:
        return jsonify({'message': 'Customer ID, vehicle ID, date of hire, and return date are required'}), 400

    # Check if the booking is within a week
    if (return_date - date_of_hire).days > 7:
        return jsonify({'message': 'Booking cannot exceed one week'}), 400

    # Check vehicle availability
    vehicle = query_db("SELECT * FROM Vehicles WHERE VehicleID = %s", (vehicle_id,))
    if not vehicle or not vehicle['Availability']:
        return jsonify({'message': 'Vehicle not available'}), 409

    # Add the booking to the database
    query = "INSERT INTO Bookings (CustomerID, VehicleID, DateOfHire, ReturnDate) VALUES (%s, %s, %s, %s)"
    execute_db(query, (customer_id, vehicle_id, date_of_hire, return_date))

    # Update vehicle availability
    execute_db("UPDATE Vehicles SET Availability = 0 WHERE VehicleID = %s", (vehicle_id,))

    return jsonify({'message': 'Booking added successfully'}), 201
