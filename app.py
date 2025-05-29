from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
 
load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client.foody
designers = db.designers

app = Flask(__name__)
CORS(app)

@app.route('/api/listings', methods=['GET'])
def get_listings():
    data = list(designers.find())
    for item in data:
        item['_id'] = str(item['_id'])   
    # print(data)  
    return jsonify(data)



@app.route('/api/toggle-shortlist/<id>', methods=['POST'])
def toggle_shortlist(id):
    designer = designers.find_one({'_id': ObjectId(id)})
    if designer:
        new_status = not designer.get('shortlisted', False)
        designers.update_one({'_id': ObjectId(id)}, {'$set': {'shortlisted': new_status}})
        return jsonify({'success': True, 'shortlisted': new_status})
    return jsonify({'error': 'Designer not found'}), 404



if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True, port=5000)
