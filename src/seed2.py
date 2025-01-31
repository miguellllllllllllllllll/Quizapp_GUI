from pymongo import MongoClient

# Verbindung zur MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["quiz_db"]
keywords_collection = db["quiz_schluesselwoerter"]

# Aggregation: Durchschnittliche Einwohnerzahl und Gesamtfläche berechnen
pipeline = [
    {
        "$match": {"attribute": {"$in": ["Einwohner", "Fläche"]}}
    },
    {
        "$group": {
            "_id": "$attribute",
            "total_value": {"$sum": "$value"},
            "average_value": {"$avg": "$value"}
        }
    }
]

# Aggregation ausführen
result = list(keywords_collection.aggregate(pipeline))

# Ergebnisse ausgeben
for entry in result:
    print(f"{entry['_id']}: Gesamt = {entry['total_value']}, Durchschnitt = {entry['average_value']}")