import os
import cv2
from fastapi import FastAPI
import time
# Initialize FastAPI app
app = FastAPI()

# Define the directory to save photos (sibling directory to the server)
PHOTO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "photo")

# Ensure the photo directory exists
os.makedirs(PHOTO_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Photo capture server is running. Use /photo to take a picture."}

@app.get("/photo")
async def take_photo():
    try:
        # Initialize the camera (device 0)
        cap = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not cap.isOpened():
            return {"error": "Could not open camera"}
        
        time.sleep(.1)
        # Capture a frame
        ret, frame = cap.read()
        
        # Release the camera
        cap.release()
        
        if not ret:
            return {"error": "Failed to capture image"}
        
        # Save the image to the photo directory
        filename = os.path.join(PHOTO_DIR, "latest_photo.jpg")
        
        # Save the image, overwriting any existing file
        cv2.imwrite(filename, frame)
        
        return {
            "message": "Photo captured successfully",
            "filename": filename
        }
    
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 5000
    uvicorn.run(app, host="0.0.0.0", port=5001)