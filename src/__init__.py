from flask import Flask, g
import mysql.connector

from src.routes import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config['SECRET_KEY'] = 'CAR-HIRE-MANAGEMENT-SECRET-KEY'
    # Database configuration
    app.config['DB_HOST'] = 'localhost'
    app.config['DB_USER'] = 'car_user'
    app.config['DB_PASSWORD'] = 'car_user'
    app.config['DB_NAME'] = 'car-database'

    @app.before_request
    def before_request():
        if 'db' not in g:
            g.db = mysql.connector.connect(
                host=app.config['DB_HOST'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD'],
                database=app.config['DB_NAME']
            )
            g.cursor = g.db.cursor(dictionary=True)

    @app.teardown_request
    def teardown_request(error=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()
            cursor = g.pop('cursor', None)
            if cursor is not None:
                cursor.close()

    app.register_blueprint(auth_bp)
    # app.register_blueprint(customer_bp)
    # app.register_blueprint(vehicle_bp)
    # app.register_blueprint(booking_bp)
    return app
