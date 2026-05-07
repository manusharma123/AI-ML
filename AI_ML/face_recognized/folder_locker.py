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

def unlock_folder(FOLDER_PATH):
    subprocess.run(
        f'icacls "{FOLDER_PATH}" /remove:d Everyone',
        shell=True,
        check=True
    )
    print("🔓 Folder unlocked successfully")

if __name__ == "__main__":
    path = input("Enter the folder path to lock/unlock: ")
    choice = input("Type 'lock' or 'unlock': ").lower()
    if choice == "lock":
        lock_folder(path)
    elif choice == "unlock":
        unlock_folder(path)
    else:
        print("Invalid choice.")
