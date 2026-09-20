from flask import Flask, request, jsonify
import pandas as pd
import requests
from io import BytesIO
import os
from datetime import datetime

app = Flask(__name__)

# ✅ Hugging Face bucket download link
DATASET_URL = "https://huggingface.co/buckets/Sandeshkum/sandesh-api/resolve/users.parquet?download=true"

HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

print("Loading dataset... यह थोड़ा समय ले सकता है")
response = requests.get(DATASET_URL, headers=headers)
response.raise_for_status()

df = pd.read_parquet(BytesIO(response.content))
print("Dataset loaded successfully!")

LOG_FILE = "search_logs.txt"

def save_log(mobile, result_found):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | Mobile: {mobile} | Found: {result_found}\n")

@app.route("/lookup", methods=["GET"])
def lookup():
    mobile = request.args.get("mobile")
    if not mobile:
        return jsonify({"error": "Mobile number देना जरूरी है"}), 400

    result = df[df["mobile"].astype(str) == str(mobile)]

    if not result.empty:
        save_log(mobile, True)
        return jsonify(result.iloc[0].to_dict())
    else:
        save_log(mobile, False)
        return jsonify({"message": "कोई record नहीं मिला"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
