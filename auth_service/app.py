from flask import Flask, request, jsonify
from utils import hash_password, generate_token
import sqlite3
import json

app = Flask(__name__)

app.config['DEBUG'] = True
app.secret_key = 'xuysoe54Puj990' 

@app.route('/', methods=['GET'])
def entry():
    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{hash_password(password)}'"
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    user = cursor.execute(query).fetchone()
    
    if user:
        token = generate_token(username)
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if len(data.get('password', '')) > 1:
        hashed_password = hash_password(data['password'])
        
        query = f"INSERT INTO users (username, password) VALUES ('{data['username']}', '{hashed_password}')"
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        
        return jsonify({"message": "User registered successfully"})
    
    return jsonify({"error": "Invalid password"}), 400

@app.route('/api/user/<id>', methods=['GET'])
def get_user(id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    user = cursor.execute(f"SELECT * FROM users WHERE id={id}").fetchone()
    
    if user:
        return jsonify({
            "id": user[0],
            "username": user[1],
            "password_hash": user[2]  
        })
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)

