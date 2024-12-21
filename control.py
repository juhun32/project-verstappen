# car control

import pyautogui


def send_controls(throttle, brake, steer):
    """Send inputs to the game using keyboard or joystick emulation."""
    pyautogui.keyDown('w') if throttle > 0.5 else pyautogui.keyUp('w')
    pyautogui.keyDown('s') if brake > 0.5 else pyautogui.keyUp('s')
    # Implement steering control using left/right keys or joystick API


# Example usage
send_controls(throttle, brake, steer=0.0)
