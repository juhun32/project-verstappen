import time
import pandas as pd
from pynput.keyboard import Listener

# Replace with telemetry data extraction


def get_game_state():
    return {
        "speed": 120,  # Example values
        "steering_angle": 0,
        "throttle": 1.0,
        "brake": 0.0
    }


# Log the control inputs
controls = []


def on_press(key):
    if key == "w":  # Accelerate
        controls.append({"throttle": 1.0, "brake": 0.0})
    elif key == "s":  # Brake
        controls.append({"throttle": 0.0, "brake": 1.0})
    # Add more controls for steering, etc.


# Save game state and controls
data = []


def record_data():
    while True:
        game_state = get_game_state()
        game_state.update(
            controls[-1] if controls else {"throttle": 0.0, "brake": 0.0})
        data.append(game_state)
        time.sleep(0.1)  # Record every 0.1 seconds


with Listener(on_press=on_press):
    record_data()

# Save the data to a CSV file
pd.DataFrame(data).to_csv("driving_data.csv")
