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
    
def add_document(collection_name, document):
    """Add a document to the specified collection."""
    try:
        result = db[collection_name].insert_one(document)
        print(f"Document inserted with id: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        print(f"Failed to insert document: {e}")
        return None

def get_history_content_only(document):
    """
    Given a document with a 'history' field (list of dicts with 'content'),
    return a list of only the 'content' values.
    """
    if "history" in document:
        return [entry.get("content") for entry in document["history"] if "content" in entry]
    return []

def get_all_history_by_session_id(collection_name, session_id):
    """Get all documents from the specified collection for a given session ID."""
    try:
        documents = list(db[collection_name].find({"session_id": session_id}))
        
        all_content = []
        for doc in documents:
            all_content.extend(get_history_content_only(doc))
        return all_content
    except Exception as e:
        print(f"Failed to get documents: {e}")
        return []
    
def get_all_session_ids(collection_name):
    """Get a list of all unique session IDs from the specified collection."""
    try:
        session_ids = db[collection_name].distinct("session_id")
        return session_ids
    except Exception as e:
        print(f"Failed to get session IDs: {e}")
        return []
    
def find_session_id_by_user(collection_name, user):
    """Find session IDs associated with a specific user."""
    try:
        session_ids = db[collection_name].distinct("session_id", {"user": user})
        return session_ids
    except Exception as e:
        print(f"Failed to find session IDs for user {user}: {e}")
        return []
    
def update_document_by_session_id(collection_name, session_id, history):
    """Update a document by adding history for a given session ID."""
    try:
        
        result = db[collection_name].update_one(
            {"session_id": session_id},
            {"$push": {"history": {"$each": history}}}
        )

        if result.matched_count > 0:
            print(f"Successfully updated document with session_id: {session_id}")
            return True
        else:
            print(f"No document found with session_id: {session_id}. Update failed.")
            return False
    except Exception as e:
        print(f"Failed to update document: {e}")
        return False
    

# Example usage
if __name__ == "__main__":
    verify_connection()
    print(get_all_session_ids(os.getenv("HISTORY_COLLECTION")))
