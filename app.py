from flask import Flask, request
import pandas as pd
import requests
import os

app = Flask(__name__)

# Airtable configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = "app8k5RQqX7xSAVbx"
TABLE_NAME = "Council Minutes"
AIRTABLE_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def index():
    return "Ormstown GPT Backend is Running"

@app.route("/load_csv", methods=["POST"])
def load_csv():
    try:
        path = "airtable_final_batch.csv"
        df = pd.read_csv(path)

        records = []
        for _, row in df.iterrows():
            fields = {
                "Date": row["Date"],
                "Type": row["Type"],
                "Title": row["Title"],
                "Summary": row["Summary"],
                "Adopted Resolutions": row["Adopted Resolutions"],
                "Source PDF": row["Source PDF"]
            }
            records.append({"fields": fields})

        for i in range(0, len(records), 10):
            batch = {"records": records[i:i+10]}
            r = requests.post(AIRTABLE_URL, headers=HEADERS, json=batch)
            if r.status_code != 200:
                return f"Error: {r.status_code} - {r.text}", 500

        return "Successfully uploaded to Airtable", 200

    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
