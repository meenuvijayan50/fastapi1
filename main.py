from fastapi import FastAPI, HTTPException
import psycopg2
from pymongo import MongoClient

# FastAPI app
app = FastAPI()

# Database configuration for PostgreSQL
def get_postgres_connection():
    connection = psycopg2.connect(
        dbname="base",
        user="demo",
        password="meenu",
        host="localhost",
    )
    return connection

# Database configuration for MongoDB
mongo_client = MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client["profile_pictures"]
mongo_collection = mongo_db["pictures"]

# User Registration Endpoint
@app.post("/register/")
async def register_user(
    first_name: str, email: str, password: str, phone: str
):
    # Check if the email already exists in PostgreSQL
    connection = get_postgres_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    # Insert user into PostgreSQL
    cursor.execute(
        "INSERT INTO users (first_name, email, password, phone) VALUES (%s, %s, %s, %s) RETURNING id",
        (first_name, email, password, phone),
    )
    user_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    # Placeholder implementation to store profile picture in MongoDB
    profile_picture = {"user_id": user_id, "picture_data": "base64_encoded_image"}
    mongo_collection.insert_one(profile_picture)

    return {"user_id": user_id, "first_name": first_name, "email": email, "phone": phone}

# Get User Details Endpoint
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    # Placeholder implementation to retrieve user details from PostgreSQL
    connection = get_postgres_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_details = cursor.fetchone()

    if not user_details:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="User not found")

    # Placeholder implementation to retrieve profile picture from MongoDB
    profile_picture = mongo_collection.find_one({"user_id": user_id})
    user_details = {
        "user_id": user_details[0],
        "first_name": user_details[1],
        "email": user_details[2],
        "phone": user_details[4],
        "profile_picture": profile_picture.get("picture_data", None),
    }

    cursor.close()
    connection.close()

    return user_details
