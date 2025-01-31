from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import random
import time
import os
from flask import send_from_directory

app = Flask(__name__, static_folder="dist")
CORS(app)  # Enable Cross-Origin Resource Sharing for the React frontend

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["quiz_db"]
keywords_collection = db["quiz_schluesselwoerter"]
stats_collection = db["quiz_statistiken"]

def get_keywords(attribute):
    pipeline = [
        {"$match": {"attribute": attribute, "value": {"$exists": True, "$ne": None}}},
        {"$sample": {"size": 1}}
    ]
    correct_entry = keywords_collection.aggregate(pipeline).next()
    correct_value = correct_entry["value"]
    correct_name = correct_entry["name"]

    # Filter incorrect values
    incorrect_entries = []
    for entry in keywords_collection.find({"attribute": attribute, "value": {"$ne": None}}):
        if entry["name"] != correct_name:
            incorrect_entries.append(entry)

    incorrect_values = random.sample(incorrect_entries, k=min(2, len(incorrect_entries)))

    return correct_entry, incorrect_values

@app.route('/quiz', methods=['GET'])
def quiz():
    attribute = request.args.get('attribute')
    if attribute not in ["Fläche", "Einwohner", "Hauptstadt", "Höchster Berg"]:
        return jsonify({"error": "Invalid attribute"}), 400

    correct_entry, incorrect_entries = get_keywords(attribute)
    correct_value = correct_entry["value"]
    correct_name = correct_entry["name"]

    # Generate options
    all_options = [correct_value] + [entry["value"] for entry in incorrect_entries]
    random.shuffle(all_options)

    return jsonify({
        "question": f"Was ist die {attribute} von {correct_name}?",
        "options": all_options,
        "correct_value": correct_value,
        "correct_name": correct_name
    })

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    name = data["name"]
    score = data["score"]
    elapsed_time = data["time"]
    
    stats_collection.insert_one({
        "name": name,
        "score": score,
        "time": elapsed_time
    })
    
    top_stats = stats_collection.find().sort([("score", -1), ("time", 1)]).limit(3)
    top_results = [{"name": stat["name"], "score": stat["score"], "time": stat["time"]} for stat in top_stats]

    return jsonify(top_results)

# Serve React build files (after running `npm run build`)
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
