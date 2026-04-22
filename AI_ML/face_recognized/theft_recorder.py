import cv2
import time
import torch
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
from torch.nn.functional import cosine_similarity
from datetime import datetime
import os
import logging
import pygame

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize pygame mixer
pygame.mixer.init()

# Models
mtcnn = MTCNN(image_size=160, margin=20)
model = InceptionResnetV1(pretrained='vggface2').eval()

def load_authorized_embeddings(directory="authorized"):
    """Load all authorized user embeddings from the specified directory."""
    embeddings = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".pt"):
                filepath = os.path.join(directory, filename)
                embeddings.append(torch.load(filepath))
        logging.info(f"Loaded {len(embeddings)} authorized embeddings.")
    except FileNotFoundError:
        logging.error(f"Authorized directory '{directory}' not found.")
    except Exception as e:
        logging.error(f"Error loading authorized embeddings: {e}")
    return embeddings

def is_authorized(face_embedding, authorized_embeddings, threshold=0.7):
    """Check if the face embedding matches any authorized embedding."""
    for authorized_embedding in authorized_embeddings:
        similarity = cosine_similarity(face_embedding, authorized_embedding).item()
        logging.info(f"Similarity: {similarity:.4f}")
        if similarity > threshold:
            return True
    return False

def save_intruder_image(frame, directory="intruders"):
    """Save an image of the intruder with a timestamped filename."""
    try:
        os.makedirs(directory, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(directory, f"intruder_{timestamp}.jpg")
        cv2.imwrite(filename, frame)
        logging.info(f"Intruder image saved: {filename}")
    except Exception as e:
        logging.error(f"Failed to save intruder image: {e}")

def play_alert_sound(sound_file, repeat=3):
    """Play an alert sound a specified number of times."""
    try:
        for _ in range(repeat):
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
    except Exception as e:
        logging.error(f"Failed to play alert sound: {e}")

def main():
    """Main function to monitor and detect unauthorized access."""
    authorized_embeddings = load_authorized_embeddings()
    if not authorized_embeddings:
        logging.error("Exiting program due to missing authorized embeddings.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Unable to access the webcam.")
        return

    unknown_start_time = None
    warning_triggered = False
    authorized_present_before = False

    logging.info("Monitoring started. Press 'q' to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logging.error("Failed to read frame from webcam.")
                break

            face = mtcnn(frame)

            if face is not None:
                emb = model(face.unsqueeze(0))

                if is_authorized(emb, authorized_embeddings):
                    if not authorized_present_before:
                        logging.info("✅ Authorized user detected.")
                    authorized_present_before = True
                    unknown_start_time = None
                    warning_triggered = False
                else:
                    authorized_present_before = False

                    if unknown_start_time is None:
                        unknown_start_time = time.time()

                    elapsed = time.time() - unknown_start_time

                    if elapsed > 5 and not warning_triggered:
                        save_intruder_image(frame)
                        play_alert_sound("fahhh_KcgAXfs.mp3")
                        logging.warning("⚠️ Unauthorized access detected!")
                        warning_triggered = True
            else:
                logging.info("No face detected.")
                unknown_start_time = None

            cv2.imshow("Theft Recorder", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logging.info("Monitoring stopped.")

if __name__ == "__main__":
    main()