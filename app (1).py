import csv
import os
from flask import Flask, request, jsonify
from pyairtable import Table
from pyairtable.formulas import match

app = Flask(__name__)

AIRTABLE_API_KEY = "patYSIH6IVDWelJEN.1636f141b98908a23db44cd8ba77fc1591375664143771ddb314f1eed6543203"
BASE_ID = "appd0dHaHu9yR1C1x"
TABLE_NAME = "Council Minutes"

@app.route("/")
def home():
    return "Ormstown GPT Backend is Running"

@app.route("/load_csv", methods=["POST"])
def load_csv_to_airtable():
    try:
        table = Table(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)

        with open("airtable_final_batch.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            records = [row for row in reader]

            for record in records:
                existing = table.first(formula=match({"Date": record["Date"], "Title": record["Title"]}))
                if not existing:
                    table.create(record)

        return jsonify({"message": "CSV uploaded to Airtable successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
