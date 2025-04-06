import subprocess
import base64
# import cv2
# import sys
# from typing import Optional
from rich import print
import requests
from mcp.server.fastmcp import FastMCP
import asyncio
from dash.robot import DashRobot, discover_and_connect

mcp = FastMCP("My App")

# Global robot instance for persistent connection
dash_robot = None

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
async def connect_to_dash() -> str:
    """Connect to the Dash robot if not already connected"""
    global dash_robot
    
    try:
        robot = await discover_and_connect()
        if not robot:
            return "No compatible robot found."

        if isinstance(robot, DashRobot):
            dash_robot = robot
            
            await dash_robot.drive(150)

            return "connected!"
        

    except Exception as e:
        return f"Error connecting to Dash robot: {str(e)}"

@mcp.tool()
async def move_dash_forward(distance: int = 100) -> str:
    """
    Move Dash robot forward at the specified speed
    
    Args:
        distance: Speed value (0-255), positive for forward movement
    """
    global dash_robot
    
    try:
        if not dash_robot:
            return "Dash robot is not connected. Use connect_to_dash() first."
        
        await dash_robot.drive(distance)
        await asyncio.sleep(2)  # Wait for movement to complete
        return f"Dash moved forward at speed {distance}"
    except Exception as e:
        print(f"[bold red]Error moving Dash: {str(e)}[/bold red]")
        return f"Error moving Dash: {str(e)}"

@mcp.tool()
async def disconnect_dash() -> str:
    """Disconnect from the Dash robot and clean up"""
    global dash_robot
    
    try:
        if not dash_robot:
            return "No Dash robot is currently connected."
        
        await dash_robot.reset(4)  # Soft reset as a gentle cleanup
        await dash_robot.disconnect()
        dash_robot = None
        return "Disconnected gracefully from Dash robot."
    except Exception as e:
        print(f"[bold red]Error disconnecting from Dash: {str(e)}[/bold red]")
        return f"Error disconnecting from Dash: {str(e)}"

@mcp.tool()
def test(text: str) -> str:
    return "OMG OMG OMG OMG"

@mcp.tool()
def plusTwoNums(first: int, second: int) -> int:
    return first + second + 5

@mcp.tool()
def test_rich_print() -> str:
    """
    A simple test function using the rich library for colored output
    """
    # Demonstrate rich's formatting capabilities
    print("[bold red]This is a test function[/bold red]")
    return "Test function executed successfully"

@mcp.tool()
def test_http_request() -> str:
    """
    A test function that makes a simple HTTP request
    """
    try:
        response = requests.get('https://httpbin.org/get')
        return f"Request successful. Status code: {response.status_code}"
    except Exception as e:
        return f"Request failed: {str(e)}"

# @mcp.tool()
# def take_webcam_screenshot() -> Optional[str]:
#     """
#     Take a screenshot from the webcam and return it as a base64 encoded string.
   
#     Args:
#         device_id: The camera device ID (default is 0 for the primary webcam)
   
#     Returns:
#         Base64 encoded string of the image or None if capture fails
#     """
#     try:
#         # Initialize the webcam
#         cap = cv2.VideoCapture(0)
       
#         if not cap.isOpened():
#             return None
           
#         # Capture a single frame
#         ret, frame = cap.read()
       
#         # Release the webcam
#         cap.release()
       
#         if not ret:
#             return None
           
#         # Convert the image to JPEG format
#         _, buffer = cv2.imencode('.jpg', frame)
       
#         # Convert to base64 string
#         image_base64 = base64.b64encode(buffer).decode('utf-8')
       
#         return image_base64
       
    # except Exception as e:
    #     print(f"Error capturing image: {str(e)}", file=sys.stderr)
    #     return None

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