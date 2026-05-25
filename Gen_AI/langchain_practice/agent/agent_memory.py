import uuid
import db_config

def create_session_id():
    return str(uuid.uuid4())

def check_User_session_exists_update_history(collection, doc):
    session_ids = db_config.find_session_id_by_user(collection, doc["user"])

    if session_ids:
        print(f"Found existing session(s) for user {doc['user']}: {session_ids}")

        for session_id in session_ids:
            if session_id == doc["session_id"]:
                print(f"Session ID {session_id} exists. Updating history.")
                history = doc["history"][-2:]
                return db_config.update_document_by_session_id(
                    collection, doc["session_id"], history
                )

        # ✅ Only reached if NO match found
        print(f"No matching session found. Creating new document.")
        return db_config.add_document(collection, doc)

    else:
        print(f"No sessions found for user. Creating new document.")
        return db_config.add_document(collection, doc)


def update_history(collection, session_id, user, history):
    """Update the history for a given session ID and user."""
    try:
        result = db_config.update_document_by_session_id(collection, session_id, history)
        if result.matched_count > 0:
            print(f"Successfully updated history for session_id: {session_id}")
            return True
        else:
            print(f"No document found with session_id: {session_id}. History not updated.")
            return False
    except Exception as e:
        print(f"Failed to update history: {e}")
        return False