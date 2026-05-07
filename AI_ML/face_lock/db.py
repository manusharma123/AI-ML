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

def add_document(collection_name, document):
    """Add a document to the specified collection."""
    try:
        result = db[collection_name].insert_one(document)
        print(f"Document inserted with id: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        print(f"Failed to insert document: {e}")
        return None

def get_all_documents(collection_name, query=None):
    """Get all documents from the specified collection matching the query (or all if query is None)."""
    try:
        if query is None:
            query = {}
        documents = list(db[collection_name].find(query))
        print(f"Documents found: {documents}")
        return documents
    except Exception as e:
        print(f"Failed to get documents: {e}")
        return []
    
def delete_document(collection_name, query):
    """Delete documents from the specified collection matching the query."""
    try:
        result = db[collection_name].delete_many(query)
        print(f"Deleted {result.deleted_count} document(s) from {collection_name}.")
        return result.deleted_count
    except Exception as e:
        print(f"Failed to delete document(s): {e}")
        return 0
    
def update_document(collection_name, query, update_values):
    """Update documents in the specified collection matching the query with the provided update values."""
    try:
        result = db[collection_name].update_many(query, {'$set': update_values})
        print(f"Updated {result.modified_count} document(s) in {collection_name}.")
        return result.modified_count
    except Exception as e:
        print(f"Failed to update document(s): {e}")
        return 0

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
