from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import random

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["quiz_db"]
keywords_collection = db["quiz_schluesselwoerter"]
scores_collection = db["quiz_scores"]  # Neue Collection für Scores

@app.route("/api/question", methods=["GET"])
def get_question():
    """Zufällige Quizfrage aus der Datenbank abrufen."""
    attributes = ["Einwohner", "Fläche"]
    attribute = random.choice(attributes)

    entries = list(keywords_collection.find({"attribute": attribute}))
    if len(entries) < 3:
        return jsonify({"error": "Nicht genug Daten"}), 500

    correct_entry = random.choice(entries)
    incorrect_entries = random.sample([e for e in entries if e["_id"] != correct_entry["_id"]], 2)

    question = {
        "_id": str(correct_entry["_id"]),
        "text": f"Wie viel {attribute} hat {correct_entry['name']}?",
        "options": [
            correct_entry["value"],
            incorrect_entries[0]["value"],
            incorrect_entries[1]["value"]
        ],
        "correct": correct_entry["value"],
        "details": {
            correct_entry["name"]: correct_entry["value"],
            incorrect_entries[0]["name"]: incorrect_entries[0]["value"],
            incorrect_entries[1]["name"]: incorrect_entries[1]["value"],
        }
    }
    random.shuffle(question["options"])
    return jsonify(question)

@app.route("/api/answer", methods=["POST"])
def check_answer():
    """Antwort überprüfen und alle Ergebnisse anzeigen."""
    data = request.json
    question_id = data.get("question_id")
    answer = data.get("answer")
    player_name = data.get("name")

    try:
        question = keywords_collection.find_one({"_id": ObjectId(question_id)})
    except:
        return jsonify({"error": "Ungültige Frage-ID"}), 400

    if not question:
        return jsonify({"error": "Frage nicht gefunden"}), 404

    correct = question["value"] == answer
    score_change = 1 if correct else 0

    # Punkte in der Datenbank speichern oder aktualisieren
    scores_collection.update_one(
        {"name": player_name},
        {"$inc": {"score": score_change}},
        upsert=True
    )

    return jsonify({
        "correct": correct,
        "message": "Richtig!" if correct else f"Falsch! Die richtige Antwort ist {question['value']}.",
        "details": {
            question["name"]: question["value"]
        }
    })

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    """Die Top 3 Spieler mit den höchsten Scores abrufen."""
    top_players = list(scores_collection.find().sort("score", -1).limit(3))
    leaderboard = [{"name": player["name"], "score": player["score"]} for player in top_players]
    return jsonify(leaderboard)

if __name__ == "__main__":
    app.run(debug=True)
