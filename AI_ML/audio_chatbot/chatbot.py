import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
from text_seech_text import text_to_speech, speech_to_text

# Load environment variables from .env file
load_dotenv()

# Retrieve AWS credentials and model ID
aws_access_key_id = os.getenv("access_key")
aws_secret_access_key = os.getenv("secret_key")
model_id = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

def get_chatbot_response(user_message):
    """Send a user message to the model and get the response."""
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        # Send the message to the model, using a basic inference configuration.
        streaming_response = client.converse_stream(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )

        # Extract and return the streamed response text.
        response_text = ""
        for chunk in streaming_response["stream"]:
            if "contentBlockDelta" in chunk:
                text = chunk["contentBlockDelta"]["delta"]["text"]
                response_text += text
        return response_text

    except (ClientError, Exception) as e:
        return f"ERROR: Can't invoke '{model_id}'. Reason: {e}"

def main():
    print("Chatbot initialized. Say 'exit' to quit.")
    while True:
        user_input = speech_to_text()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = get_chatbot_response(user_input)
        print(f"Chatbot: {response}")
        text_to_speech(response)

if __name__ == "__main__":
    main()