import os
data:str = ""

folder_path = "./data"

files= os.listdir(folder_path)
print("files in data folder : ", files)



with open(f"files","r") as file:
    data = file.read()
    print("data loaded successfully")



def LLM_response(data):
    # This is a mock function to simulate LLM response
    prompt = """
    remove duplicates in the given data {data}
"""
    client= azure.chat(queries.format(prompt))
