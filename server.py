import subprocess
import base64
import cv2
# import sys
# from typing import Optional
from rich import print
import requests
from mcp.server.fastmcp import FastMCP, Image
import asyncio
from dash.robot import DashRobot, discover_and_connect
import time
from PIL import Image as PILImage
mcp = FastMCP("My App")

# Global robot instance for persistent connection
dash_robot = None

@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"

@mcp.tool()
def get_image() -> list[Image]:
    # these works
    img1 = Image(path="/Users/jakesimonds/Documents/mcp-python-demo/photo/latest_photo.jpg")

    # buffer = io.BytesIO()
    # PILImage.open("photo/test.jpg").save(buffer, format="PNG")
    # img4 = Image(data=buffer.getvalue(), format="png")

    # success
    return img1


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
            
            await dash_robot.move(100)
            await dash_robot.say("hi")

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
        
        await dash_robot.move(distance)
        await asyncio.sleep(2)  # Wait for movement to complete
        return f"Dash moved forward at speed {distance}"
    except Exception as e:
        print(f"[bold red]Error moving Dash: {str(e)}[/bold red]")
        return f"Error moving Dash: {str(e)}"

@mcp.tool()
async def dash_stop() -> str:
    """Stop Dash robot from moving"""
    global dash_robot
    
    try:
        if not dash_robot:
            return "Dash robot is not connected. Use connect_to_dash() first."
        
        await dash_robot.stop()
        return "Dash stopped"
    except Exception as e:
        print(f"[bold red]Error stopping Dash: {str(e)}[/bold red]")
        return f"Error stopping Dash: {str(e)}"

@mcp.tool()
async def dash_spin(speed: int = 200) -> str:
    """
    Make Dash robot spin left or right
    
    Args:
        speed: Speed value (-2048 to 2048), positive for clockwise, negative for counter-clockwise
    """
    global dash_robot
    
    try:
        if not dash_robot:
            return "Dash robot is not connected. Use connect_to_dash() first."
        
        await dash_robot.spin(speed)
        return f"Dash spinning at speed {speed}"
    except Exception as e:
        print(f"[bold red]Error spinning Dash: {str(e)}[/bold red]")
        return f"Error spinning Dash: {str(e)}"




@mcp.tool()
#async def dash_turn(degrees, speed_dps=360/2.094):
async def dash_turn(degrees, speed_dps=360/5.0):
    """
    Turns the robot a specific number of degrees at a certain speed.
    This method simplifies the operation to a 'spin' command for a calculated duration.
    Adjust this method based on your robot's capabilities.
    """
    global dash_robot

    # Convert string parameters to numeric values
    degrees = float(degrees)
    speed_dps = float(speed_dps)

    if not dash_robot:
        return "Dash robot is not connected. Use connect_to_dash() first."

    if abs(degrees) > 360:
        print("Cannot turn more than one rotation per move")
        return
    
    # Assuming positive degrees for clockwise, negative for counter-clockwise
    speed = 200 if degrees > 0 else -200
    # Calculate duration based on speed and degrees to turn
    duration = abs(degrees / speed_dps)
    await dash_robot.spin(speed)
    await asyncio.sleep(duration)
    await dash_robot.stop()
    
    return f"Dash turned {degrees} degrees"



@mcp.tool()
async def dash_say(sound_name: str) -> str:
    """
    Make Dash robot play a sound
    
    Args:
        sound_name: Name of the sound to play (from NOISES dictionary)
    """
    global dash_robot
    
    try:
        if not dash_robot:
            return "Dash robot is not connected. Use connect_to_dash() first."
        
        await dash_robot.say(sound_name)
        return f"Dash played sound: {sound_name}"
    except Exception as e:
        print(f"[bold red]Error making Dash play sound: {str(e)}[/bold red]")
        return f"Error making Dash play sound: {str(e)}"



@mcp.tool()
async def dash_head_movement(yaw: int = 0, pitch: int = 0) -> str:
    """
    Move Dash robot's head
    
    Args:
        yaw: Horizontal angle (-53 to 53)
        pitch: Vertical angle (-5 to 10)
    """
    global dash_robot
    
    try:
        if not dash_robot:
            return "Dash robot is not connected. Use connect_to_dash() first."
        
        await dash_robot.head_yaw(yaw)
        await dash_robot.head_pitch(pitch)
        return f"Dash moved head to yaw:{yaw}, pitch:{pitch}"
    except Exception as e:
        print(f"[bold red]Error moving Dash's head: {str(e)}[/bold red]")
        return f"Error moving Dash's head: {str(e)}"

@mcp.tool()
async def dash_change_lights(eye_value: int = None, neck_color: str = None, 
                           left_ear_color: str = None, right_ear_color: str = None) -> str:
    """
    Change Dash robot's lights
    
    Args:
        eye_value: Eye brightness (0-255)
        neck_color: Color name (e.g., 'red', 'blue', 'green')
        left_ear_color: Color name for left ear
        right_ear_color: Color name for right ear
    """
    global dash_robot
    
    try:
        if not dash_robot:
            return "Dash robot is not connected. Use connect_to_dash() first."
        
        actions = []
        if eye_value is not None:
            await dash_robot.eye_brightness(eye_value)
            actions.append(f"eye brightness to {eye_value}")
            
        if neck_color is not None:
            await dash_robot.neck_color(neck_color)
            actions.append(f"neck color to {neck_color}")
            
        if left_ear_color is not None:
            await dash_robot.left_ear_color(left_ear_color)
            actions.append(f"left ear color to {left_ear_color}")
            
        if right_ear_color is not None:
            await dash_robot.right_ear_color(right_ear_color)
            actions.append(f"right ear color to {right_ear_color}")
        
        if not actions:
            return "No light changes specified"
            
        return f"Changed Dash lights: {', '.join(actions)}"
    except Exception as e:
        print(f"[bold red]Error changing Dash lights: {str(e)}[/bold red]")
        return f"Error changing Dash lights: {str(e)}"

@mcp.tool()
def get_available_sounds() -> list[str]:
    """Returns a list of all available sound names that can be used with dash_say()"""
    from dash.constants import NOISES
    return list(NOISES.keys())

@mcp.tool()
def get_sound_descriptions() -> dict:
    """Returns a dictionary mapping sound names to descriptions of what they sound like"""
    return {
        "elephant": "Elephant trumpet sound",
        "tiresqueal": "Car tires screeching",
        "hi": "Dash saying hello",
        "bragging": "Boastful robot sounds",
        "ohno": "Concerned 'oh no' sound",
        "ayayay": "Confused 'ayayay' sound",
        "confused2": "Second confused sound variation",
        "confused3": "Third confused sound variation",
        "confused5": "Fifth confused sound variation",
        "confused8": "Eighth confused sound variation",
        "brrp": "Short robotic 'brrp' sound",
        "charge": "Energetic charge forward sound",
        "huh": "Questioning 'huh?' sound",
        "okay": "Robot saying 'okay'",
        "yawn": "Sleepy yawning sound",
        "tada": "Triumphant 'ta-da' sound",
        "wee": "Excited 'wee!' sound",
        "bye": "Goodbye sound",
        "horse": "Horse whinnying",
        "cat": "Cat meowing",
        "dog": "Dog barking",
        "dino": "Dinosaur roaring",
        "lion": "Lion roaring",
        "goat": "Goat bleating",
        "croc": "Crocodile noise",
        "siren": "Emergency siren",
        "horn": "Vehicle horn",
        "engine": "Engine revving",
        "tires": "Tires screeching",
        "helicopter": "Helicopter blades whirring",
        "jet": "Jet engine sound",
        "boat": "Boat horn/engine",
        "train": "Train whistle",
        "beep": "Cute robot beep",
        "laser": "Laser beam sound",
        "gobble": "Gobbling sound",
        "buzz": "Buzzing sound",
        "squeek": "Squeaking sound",
        "my1": "Custom recorded sound 1",
        "my2": "Custom recorded sound 2",
        "my3": "Custom recorded sound 3",
        "my4": "Custom recorded sound 4",
        "my5": "Custom recorded sound 5",
        "my6": "Custom recorded sound 6",
        "my7": "Custom recorded sound 7",
        "my8": "Custom recorded sound 8",
        "my9": "Custom recorded sound 9",
        "my10": "Custom recorded sound 10"
    }

@mcp.tool()
def get_available_commands() -> dict:
    """Returns a mapping of all available robot commands and their command codes"""
    from dash.constants import COMMANDS
    return COMMANDS

@mcp.tool()
def get_movement_limits() -> dict:
    """Returns the limits for various movement parameters"""
    return {
        "speed": {
            "min": -2048,
            "max": 2048,
            "description": "Speed value for driving and spinning. Positive for forward/clockwise, negative for backward/counter-clockwise."
        },
        "head_yaw": {
            "min": -53,
            "max": 53,
            "description": "Horizontal head angle in degrees. Positive turns right, negative turns left."
        },
        "head_pitch": {
            "min": -5,
            "max": 10,
            "description": "Vertical head angle in degrees. Positive tilts up, negative tilts down."
        },
        "turn_degrees": {
            "min": -360,
            "max": 360,
            "description": "Degrees to turn. Positive for clockwise, negative for counter-clockwise."
        },
        "brightness": {
            "min": 0,
            "max": 255,
            "description": "Brightness value for lights (eyes, tail, etc)."
        }
    }

@mcp.tool()
def get_color_examples() -> dict:
    """Returns example color names that can be used with Dash's light commands"""
    return {
        "basic_colors": ["red", "green", "blue", "yellow", "purple", "cyan", "magenta", "orange", "pink", "white"],
        "additional_colors": ["navy", "teal", "olive", "lime", "maroon", "brown", "coral", "gold", "silver", "lavender"],
        "note": "Any CSS color name or hex code (#RRGGBB) can be used for the robot's lights"
    }


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

if __name__ == "__main__":
    mcp.run()