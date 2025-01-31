from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["quiz_db"]
collection = db["quiz_schluesselwoerter"]
leaderboard_collection = db["leaderboard"]

@app.route("/api/question", methods=["GET"])
def get_question():
    question_data = collection.aggregate([{ "$sample": { "size": 1 } }]).next()
    attribute = question_data["attribute"]

    # Hole alle Städte für das gleiche Attribut
    options = list(collection.find({"attribute": attribute}))
    random.shuffle(options)

    question = {
        "_id": str(question_data["_id"]),
        "text": f"Welche Stadt hat folgende Eigenschaft: {attribute}?",
        "correct_answer": question_data["name"],
        "options": [opt["name"] for opt in options[:3]]  # 3 Antwortmöglichkeiten
    }

    return jsonify(question)

@app.route("/api/answer", methods=["POST"])
def check_answer():
    data = request.json
    question_id = data.get("question_id")
    answer = data.get("answer")
    name = data.get("name", "Anonym")

    question_data = collection.find_one({"_id": ObjectId(question_id)})
    if not question_data:
        return jsonify({"error": "Frage nicht gefunden"}), 400

    is_correct = answer == question_data["name"]

    # Falsche Antworten mit richtigen Werten
    all_options = list(collection.find({"attribute": question_data["attribute"]}))
    incorrect_answers = {opt["name"]: opt["value"] for opt in all_options if opt["name"] != question_data["name"]}

    if is_correct:
        message = "Richtig!"
        score = 1
    else:
        message = f"Falsch! Die richtige Antwort ist {question_data['name']}."
        score = 0

    # Punkte speichern
    leaderboard_collection.insert_one({"name": name, "score": score})

    return jsonify({
        "correct": is_correct,
        "message": message,
        "incorrect_answers": incorrect_answers
    })

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    top_players = list(leaderboard_collection.aggregate([
        {"$group": {"_id": "$name", "total_score": {"$sum": "$score"}}},
        {"$sort": {"total_score": -1}},
        {"$limit": 3}
    ]))
    return jsonify([{"name": p["_id"], "score": p["total_score"]} for p in top_players])

if __name__ == "__main__":
    app.run(debug=True)
