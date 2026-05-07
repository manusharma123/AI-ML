import logging
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from db import get_all_documents
from bson import json_util
import json
from folder_locker import lock_folder, unlock_folder
from register_user import main as register_user_main
from theft_recorder import main as theft_recorder_main
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register-user")
def register_user_api():
    # This will call the CLI-based registration (camera required)
    register_user_main()
    return {"status": "User registration complete"}

@app.post("/monitor-unlock")
def monitor_unlock_api(folder_path: str = Form(...)):
    # This will call the CLI-based monitoring (camera required)
    theft_recorder_main(folder_path)
    return {"status": "Monitoring complete (folder unlocked if authorized)"}

@app.post("/lock-folder")
def lock_folder_api(folder_path: str = Form(...)):
    print(f"Received request to lock folder: {folder_path}")
    lock_folder(folder_path)
    return {"status": f"Folder locked: {folder_path}"}

@app.post("/unlock-folder")
def unlock_folder_api(folder_path: str = Form(...)):
    print(f"Received request to unlock folder: {folder_path}")
    unlock_folder(folder_path)
    return {"status": f"Folder unlocked: {folder_path}"}



@app.get("/documents/")
def get_documents_api():
    """
    Fetch all documents from the given collection
    """
    documents = get_all_documents("folders")

    # Convert MongoDB ObjectId to JSON-serializable format
    return JSONResponse(
        content=json.loads(json_util.dumps(documents))
    )

