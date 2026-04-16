from helper import db
import os
from dotenv import load_dotenv
load_dotenv()

USERS = os.getenv("USERS_COLLECTION")

class UserService:
    users_collection = db[USERS]
    
    def create_user(self, name: str, email: str, password):
        user = {
            "name": name,
            "email": email,
            "password": password
        }
        result = self.users_collection.insert_one(user)
        return result.inserted_id


    def get_user(self, email):
        return self.users_collection.find_one({"email": email})

    def update_user(self, email, name=None, password=None):
        update_data = {}
        if name:
            update_data["name"] = name
        if password:
            update_data["password"] = password
        if update_data:
            result = self.users_collection.update_one({"email": email}, {"$set": update_data})
            if result.matched_count == 0:
                return "User not found"
        return "User updated successfully"

    def delete_user(self, email):
        result = self.users_collection.delete_one({"email": email})
        if result.deleted_count == 0:
            return "User not found"
        return "User deleted successfully"
