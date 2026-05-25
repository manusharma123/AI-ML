import cv2
import numpy as np
import mss
from ml_model import predict

def screen_stream():
    with mss.mss() as sct:
        # Capture full screen
        monitor = sct.monitors[1]

        while True:
            # Capture frame
            frame = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Resize for performance (optional)
            frame = cv2.resize(frame, (800, 450))

            # Run ML prediction
            result = predict(frame)

            # Draw result on frame
            cv2.putText(
                frame,
                f"Prediction: {result}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # Encode frame
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Stream frame
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                frame_bytes +
                b'\r\n'
            )