from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from streamer import screen_stream

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Screen Share ML API is running"}

@app.get("/video")
def video_feed():
    return StreamingResponse(
        screen_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
