import csv
import os
from flask import Flask, request, jsonify
from pyairtable import Table
from pyairtable.formulas import match

app = Flask(__name__)

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = "appXXXXXXXXXXXXXX"  # ← Replace with your real base ID
TABLE_NAME = "Council Minutes"

@app.route("/")
def home():
    return "Ormstown GPT Backend is Running"

@app.route("/load_csv", methods=["POST"])
def load_csv_to_airtable():
    if not AIRTABLE_API_KEY:
        return jsonify({"error": "Missing Airtable API key"}), 500

    try:
        table = Table(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)

        with open("airtable_final_batch.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            records = [row for row in reader]

            for record in records:
                # Optional: check if record already exists
                existing = table.first(formula=match({"Date": record["Date"], "Title": record["Title"]}))
                if not existing:
                    table.create(record)

        return jsonify({"message": "CSV uploaded to Airtable successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

