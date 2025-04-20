import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["user_info"]
users_collection = db["auth_cred"]

def upsert_user(profile):
    user_id = profile.get("sub") or profile.get("email")
    if not user_id:
        print(" No valid user identifier (sub/email) found in profile. Skipping insert.")
        return

    print(f" Attempting to upsert user: {user_id}")
    print(f" Profile data: {profile}")

    result = users_collection.update_one(
        {"_id": user_id},
        {"$set": {
            "name": profile.get("name"),
            "email": profile.get("email"),
            "nickname": profile.get("nickname"),
            "picture": profile.get("picture"),
            "email_verified": profile.get("email_verified"),
            "last_login": profile.get("updated_at")
        }},
        upsert=True
    )

    if result.upserted_id:
        print(f" Inserted new user with _id: {result.upserted_id}")
    elif result.matched_count > 0:
        print(f" Updated existing user with _id: {user_id}")
    else:
        print(" No changes made to the user document.")

