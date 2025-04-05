import subprocess
import base64
import cv2
import sys
from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")

@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"

@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"

@mcp.tool()
async def add_list_of_numbers(numbers: list[int]) -> int:
    """Add a list of numbers"""
    return sum(numbers)

@mcp.tool()
def count_letter_in_text(text: str, letter: str) -> int:
    """Count occurrences of a letter in a text"""
    return text.count(letter)

@mcp.tool()
def test(text: str) -> str:
    return "OMG OMG OMG OMG"

@mcp.tool()
def plusTwoNums(first: int, second: int) -> int:
    return first + second + 5

@mcp.tool()
def take_webcam_screenshot() -> Optional[str]:
    """
    Take a screenshot from the webcam and return it as a base64 encoded string.
   
    Args:
        device_id: The camera device ID (default is 0 for the primary webcam)
   
    Returns:
        Base64 encoded string of the image or None if capture fails
    """
    try:
        # Initialize the webcam
        cap = cv2.VideoCapture(0)
       
        if not cap.isOpened():
            return None
           
        # Capture a single frame
        ret, frame = cap.read()
       
        # Release the webcam
        cap.release()
       
        if not ret:
            return None
           
        # Convert the image to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
       
        # Convert to base64 string
        image_base64 = base64.b64encode(buffer).decode('utf-8')
       
        return image_base64
       
    except Exception as e:
        print(f"Error capturing image: {str(e)}", file=sys.stderr)
        return None

@mcp.tool()
async def run_azure_cli_command(command: str) -> str:
    """Run an Azure CLI command"""
    # if command starts with "az", remove it
    if command.startswith("az "):
        command = command[3:]
    result = subprocess.run(
        ["az"] + command.split(),
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout

if __name__ == "__main__":
    mcp.run()