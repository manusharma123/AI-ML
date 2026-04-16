import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Create Mongo client
client = MongoClient(MONGO_URI)

# Database reference
db = client[DB_NAME]

def verify_connection():
    try:
        # The 'ping' command is used to check the connection to the database
        client.admin.command('ping')
        print("Database connection verified successfully.")
        return True
    except Exception as e:
        print(f"Failed to verify database connection: {e}")
        return False

# Example usage
if __name__ == "__main__":
    verify_connection()
