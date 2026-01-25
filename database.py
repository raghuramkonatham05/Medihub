# database.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# =============================
# LOAD ENV VARIABLES (FORCED)
# =============================
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# =============================
# MONGODB CONNECTION (ATLAS)
# =============================
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI not found in .env file")

client = MongoClient(MONGO_URI)

# =============================
# DATABASE
# =============================
db = client["medical_ai"]

# =============================
# COLLECTIONS
# =============================
users = db["users"]
reports = db["reports"]

# =============================
# INDEXES (SAFE TO RUN MULTIPLE TIMES)
# =============================
users.create_index("email", unique=True)
reports.create_index("user_id")

# =============================
# SAMPLE SCHEMA (REFERENCE)
# =============================
"""
users document example:
{
    _id: ObjectId,
    email: "user@example.com",
    password: "<hashed_password>",
    created_at: datetime
}

reports document example:
{
    _id: ObjectId,
    user_id: ObjectId,
    original_file: "uuid_report.pdf",
    converted_file: "uuid.txt",
    patient: {
        name: "Ratna Kumari",
        age: 65,
        gender: "Female"
    },
    lab_values: {...},
    flags: {...},
    report_types: ["CBC"],
    created_at: datetime
}
"""
