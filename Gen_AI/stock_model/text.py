
import os
folder_path ="."

# folder_path = os.path.dirname(os.path.abspath(__file__))
files = os.listdir(folder_path)
for f in os.listdir(folder_path):
        print(f) 

# print("files in stock_model folder : ", files)