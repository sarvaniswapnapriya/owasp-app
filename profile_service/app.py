from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient
import pickle
from flask_cors import CORS  

import json

app = Flask(__name__)


CORS(app)


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

    if file.filename.split('.')[-1].lower() not in ['jpg', 'jpeg', 'png']:
        return jsonify({"error": "Invalid file type. Only JPG, JPEG, and PNG are allowed."}), 400

    try:
        file_content = file.read()
        
        return jsonify({"message": "Image uploaded successfully", "file_size": len(file_content)}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 400



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
