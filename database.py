# database.py

from pymongo import MongoClient
from datetime import datetime

# =============================
# MONGODB CONNECTION
# =============================
client = MongoClient("mongodb://localhost:27017")

# Database name
db = client["medical_ai"]

# =============================
# COLLECTIONS
# =============================

# Users collection
users = db["users"]

# Reports collection
reports = db["reports"]

# =============================
# OPTIONAL: INDEXES (SAFE)
# =============================

# Ensure unique email per user
users.create_index("email", unique=True)

# Faster lookup for user reports
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
