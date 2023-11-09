# database.py
import mysql.connector
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME']
        )
        g.cursor = g.db.cursor(dictionary=True)
    return g.db, g.cursor


def close_db(e=None):
    db = g.pop('db', None)
    cursor = g.pop('cursor', None)
    if db is not None:
        db.close()
    if cursor is not None:
        cursor.close()


def query_db(query, args=(), one=False):
    cursor = g.cursor
    cursor.execute(query, args)
    data = cursor.fetchall()
    return (data[0] if data else None) if one else data


def execute_db(query, args=()):
    print(args)
    cursor = g.cursor
    cursor.execute(query, args)
    g.db.commit()
