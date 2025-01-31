from pymongo import MongoClient

# MongoDB-Verbindung herstellen
client = MongoClient("mongodb://localhost:27017/")
db = client["quiz_db"]
keywords_collection = db["quiz_schluesselwoerter"]

# Beispiel-Daten einfügen
keywords_collection.insert_many([
    {"name": "Zürich", "attribute": "Einwohner", "value": 400000},
    {"name": "Bern", "attribute": "Einwohner", "value": 133000},
    {"name": "Basel", "attribute": "Einwohner", "value": 178120},
    {"name": "Genf", "attribute": "Einwohner", "value": 200000},
    {"name": "Lausanne", "attribute": "Einwohner", "value": 140000},
    {"name": "Zürich", "attribute": "Fläche", "value": 91.88},
    {"name": "Bern", "attribute": "Fläche", "value": 51.62},
    {"name": "Basel", "attribute": "Fläche", "value": 37.5},
    {"name": "Genf", "attribute": "Fläche", "value": 15.93},
    {"name": "Lausanne", "attribute": "Fläche", "value": 41.38},
    {"name": "Zürich", "attribute": "Hauptstadt", "value": "Zürich"},
    {"name": "Bern", "attribute": "Hauptstadt", "value": "Bern"},
    {"name": "Basel", "attribute": "Hauptstadt", "value": "Basel"},
    {"name": "Genf", "attribute": "Hauptstadt", "value": "Genf"},
    {"name": "Lausanne", "attribute": "Hauptstadt", "value": "Lausanne"},
    {"name": "Zürich", "attribute": "Höchster Berg", "value": "Uetliberg"},
    {"name": "Bern", "attribute": "Höchster Berg", "value": "Gurten"},
    {"name": "Basel", "attribute": "Höchster Berg", "value": "Dreisesselberg"},
    {"name": "Genf", "attribute": "Höchster Berg", "value": "Mont Salève"},
    {"name": "Lausanne", "attribute": "Höchster Berg", "value": "La Dôle"}
])

print("Daten wurden erfolgreich in die MongoDB eingefügt.")
