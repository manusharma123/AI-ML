import random

def predict(frame):
    """
    Dummy ML prediction function.
    Replace with your actual model.
    """
    labels = ["No Object", "Person", "Laptop", "Phone"]
    return random.choice(labels)
