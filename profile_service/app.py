from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient
import pickle
import json

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.userprofiles

@app.route('/profile', methods=['GET'])
def get_profile():
    username = request.args.get('username')
    query = json.loads(username) 
    
    profile = db.profiles.find_one(query)
    if profile:
        return jsonify(profile)
    return jsonify({"error": "Profile not found"}), 404

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
        
    file = request.files['file']
    
    try:
        data = pickle.loads(file.read())  
        return jsonify({"message": "File processed", "data": str(data)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/fetch-avatar', methods=['GET'])
def fetch_avatar():
    url = request.args.get('url')
    
    try:
        response = requests.get(url)
        return response.content
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5001, debug=True)
