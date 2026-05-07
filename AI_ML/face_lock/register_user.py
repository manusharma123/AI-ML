import cv2
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize face detection and recognition models
mtcnn = MTCNN(image_size=160, margin=20)
model = InceptionResnetV1(pretrained='vggface2').eval()

def capture_face():
    """Capture a face from the webcam and return its embedding."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        logging.error("Unable to access the webcam.")
        return None

    logging.info("Look at the camera and press 's' to save your face.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logging.error("Failed to read frame from webcam.")
                break

            cv2.imshow("Register Face", frame)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                face = mtcnn(frame)
                # print(face.shape)
                if face is not None:
                    logging.info("Face detected successfully.")
                    # print(face.unsqueeze(0).shape)
                    embedding = model(face.unsqueeze(0))
                    # print(embedding.shape)
                    return embedding
                else:
                    logging.warning("No face detected. Please try again.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return None

def save_embedding(embedding, directory="authorized"):
    """Save the face embedding to a file in the authorized directory."""
    try:
        os.makedirs(directory, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(directory, f"authorized_embedding_{timestamp}.pt")
        torch.save(embedding, filename)
        logging.info(f"Embedding saved successfully as {filename}.")
    except Exception as e:
        logging.error(f"Failed to save embedding: {e}")

def main():
    """Main function to capture and save face embeddings."""
    while True:
        embedding = capture_face()
        if embedding is not None:
            save_embedding(embedding)
        else:
            logging.error("Face registration failed.")

        cont = input("Do you want to register another user? (y/n): ").strip().lower()
        if cont != 'y':
            break

if __name__ == "__main__":
    main()