from db import add_document, update_document, get_all_documents
import os
import subprocess

# FOLDER_PATH = r"C:\Practicestudy\java\test"

def lock_folder(FOLDER_PATH):
    subprocess.run(
        f'icacls "{FOLDER_PATH}" /deny Everyone:(OI)(CI)F',
        shell=True,
        check=True
    )
    
    print("🔒 Folder locked successfully")
    # Update folder info in DB if exists, else add
    existing = get_all_documents("folders", {"path": FOLDER_PATH})
    if existing:
        update_document("folders", {"path": FOLDER_PATH}, {"status": "locked"})
    else:
        add_document("folders", {"path": FOLDER_PATH, "status": "locked"})

def unlock_folder(FOLDER_PATH):
    subprocess.run(
        f'icacls "{FOLDER_PATH}" /remove:d Everyone',
        shell=True,
        check=True
    )
    print("🔓 Folder unlocked successfully")
    # Update folder info in DB if exists, else add
    existing = get_all_documents("folders", {"path": FOLDER_PATH})
    if existing:
        update_document("folders", {"path": FOLDER_PATH}, {"status": "unlocked"})
    else:
        add_document("folders", {"path": FOLDER_PATH, "status": "unlocked"})


def main():
    """Main function to monitor and detect unauthorized access."""
    path = input("Enter the folder path to lock/unlock: ")
    choice = input("Type 'lock' or 'unlock': ").lower()
    if choice == "lock":
        lock_folder(path)
    elif choice == "unlock":
        from theft_recorder import main as theft_recorder_main
        theft_recorder_main(path)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
