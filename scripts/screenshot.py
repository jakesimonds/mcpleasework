import cv2
import base64
import sys
import os
import argparse
import time

def take_webcam_screenshot(device_id=0, output_file=None):
    """
    Take a screenshot from the webcam and either save to file or print base64 string.
   
    Args:
        device_id: The camera device ID (default is 0 for the primary webcam)
        output_file: Optional file path to save the image
   
    Returns:
        Base64 encoded string of the image or None if capture fails
    """
    try:
        # Initialize the webcam
        print(f"Initializing webcam with device ID {device_id}...")
        cap = cv2.VideoCapture(0)
       
        if not cap.isOpened():
            print("Error: Unable to open webcam", file=sys.stderr)
            return None
           
        # Capture a single frame
        print("Capturing image...")
        ret, frame = cap.read()
        # for i in range(5):  # Discard first few frames
        #     ret, frame = cap.read()
        #     time.sleep(0.1)
       
        # Release the webcam
        cap.release()
       
        if not ret:
            print("Error: Failed to capture image", file=sys.stderr)
            return None
        
        # If output file is specified, save the image
        if output_file:
            print(f"Saving image to {output_file}...")
            cv2.imwrite(output_file, frame)
            print(f"Image saved successfully to {output_file}")
            return None
           
        # Convert the image to JPEG format
        print("Converting image to base64...")
        _, buffer = cv2.imencode('.jpg', frame)
       
        # Convert to base64 string
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return image_base64
       
    except Exception as e:
        print(f"Error capturing image: {str(e)}", file=sys.stderr)
        return None

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Take a screenshot from the webcam')
    parser.add_argument('--device', type=int, default=0, help='Camera device ID (default: 0)')
    parser.add_argument('--output', type=str, help='Output file path (optional)')
    args = parser.parse_args()
    
    # Take the screenshot
    result = take_webcam_screenshot(device_id=args.device, output_file=args.output)
    
    # Print the result if no output file was specified
    if result and not args.output:
        print(result)
        print("\nBase64 image string returned. You can use this in HTML like:")
        print("<img src=\"data:image/jpeg;base64," + result + "\" />")

if __name__ == "__main__":
    main() 