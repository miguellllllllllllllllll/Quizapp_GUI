from pymongo import MongoClient

# MongoDB-Verbindung herstellen
client = MongoClient("mongodb://localhost:27017/")
db = client["quiz_db"]

# Alle Collections löschen
for collection_name in db.list_collection_names():
    db.drop_collection(collection_name)

# Schlüsselwort-Daten einfügen
keywords_collection = db["quiz_schluesselwoerter"]
keywords_collection.insert_many([
    {"name": "Aurora", "attribute": "Crewgröße", "value": 2},
    {"name": "Constellation", "attribute": "Crewgröße", "value": 4},
    {"name": "Reclaimer", "attribute": "Crewgröße", "value": 5},
    {"name": "Carrack", "attribute": "Crewgröße", "value": 6},
    {"name": "Constellation", "attribute": "Länge", "value": 75.6},
    {"name": "Aurora", "attribute": "Länge", "value": 22.0},
    {"name": "Reclaimer", "attribute": "Länge", "value": 150.0},
    {"name": "Carrack", "attribute": "Länge", "value": 125.0},
    {"name": "Aurora", "attribute": "Preis", "value": 25000},
    {"name": "Constellation", "attribute": "Preis", "value": 27500},
    {"name": "Reclaimer", "attribute": "Preis", "value": 45000},
    {"name": "Carrack", "attribute": "Preis", "value": 60000},
    {"name": "Aurora", "attribute": "Frachtkapazität", "value": 2},
    {"name": "Constellation", "attribute": "Frachtkapazität", "value": 4},
    {"name": "Reclaimer", "attribute": "Frachtkapazität", "value": 6},
    {"name": "Carrack", "attribute": "Frachtkapazität", "value": 5}
])

print("Daten wurden erfolgreich in die MongoDB eingefügt.")
