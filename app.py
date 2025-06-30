
from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = "Documents"

@app.route("/documents", methods=["GET"])
def get_documents():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500
    data = response.json()
    return jsonify(data["records"])

if __name__ == "__main__":
    app.run(debug=True)
