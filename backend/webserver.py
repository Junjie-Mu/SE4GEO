# -*- coding: UTF-8 -*-
'''
@Project ：SE4GEO 
@File    ：webserver.py
@IDE     ：PyCharm 
@Author  ：JUNJIE MU
@Date    ：2024/6/21 上午1:24
@explain : 
'''

from flask import Flask, jsonify, request, send_from_directory
import psycopg2
import os
from dotenv import load_dotenv, set_key
import database.creat_user as cu

app = Flask(__name__, static_folder='../frontend', static_url_path='')


load_dotenv('database/.env')
db_name = os.getenv('DB_NAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')


def get_db_connection(dbName):
    conn = psycopg2.connect(
        dbname=dbName,
        user=user,
        password=password,
        host=host
    )
    return conn


def close_db_connection(conn):
    if conn:
        conn.close()


# Index
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

#Set .env
@app.route('/updateEnv', methods=['POST'])
def update_env():
    dbName = request.form['dbName']
    env_user = request.form['env_user']
    env_password = request.form['env_password']
    env_host = request.form['env_host']

    if not dbName or not env_user or not env_password or not env_host:
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    try:
        set_key('./database/.env', 'DB_NAME', dbName)
        set_key('./database/.env', 'USER', env_user)
        set_key('./database/.env', 'PASSWORD', env_password)
        set_key('./database/.env', 'HOST', env_host)
        return jsonify({'success': True, 'message': 'Set Environment Successful! Please restart flask.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Test database connection
@app.route('/testDb', methods=['GET'])
def test_db_connection():
    try:
        conn = get_db_connection(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        close_db_connection(conn)
        return jsonify({'success': True, 'message': 'Database connection successful! '})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Database connection failed: {str(e)}'})


# Creat 'user' table
@app.route('/createUser', methods=['GET'])
def create_user():
    try:
        cu.creat_user()
        return jsonify({'success': True, 'message': "Successfully Created Database!"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


# Register
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    conn = get_db_connection("postgres")
    cursor = conn.cursor()

    insert_query = 'INSERT INTO users (user_name, user_password) VALUES (%s, %s)'

    cursor.execute(insert_query, (username, password)),
    conn.commit()
    close_db_connection(conn)
    return jsonify({'success': True, 'message': 'Registration Success!'})

# Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if not username or not password:
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    conn = get_db_connection("postgres")
    cursor = conn.cursor()

    select_query = 'SELECT * FROM users WHERE user_name = %s AND user_password = %s'
    cursor.execute(select_query, (username, password))
    login_user = cursor.fetchone()
    close_db_connection(conn)

    if login_user:
        return jsonify({'success': True, 'message': 'Login Successful!'})
    else:
        return jsonify({'success': False, 'message': 'Wrong User Name or Password.'})


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
