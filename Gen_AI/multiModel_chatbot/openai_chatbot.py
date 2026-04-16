from openai import OpenAI
from dotenv import load_dotenv
import os

def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")  # standard name
    print("Loaded key:", api_key)  # debug

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4o-mini",
        input="Hello!"
    )

    print(response.output_text)

if __name__ == "__main__":
    main()