# database.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load env explicitly
load_dotenv(".env")

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI not found in .env")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
    tls=True,
    tlsAllowInvalidCertificates=True
)

# Force connection early (fail-fast)
client.admin.command("ping")

db = client["medical_ai"]

users = db["users"]
reports = db["reports"]

users.create_index("email", unique=True)
reports.create_index("user_id")
