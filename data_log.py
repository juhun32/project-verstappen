import os
import json
import ac
import acsys

# Define your custom log file
log_file = os.path.join(os.getcwd(), "data.json")


# Create or append to the log file
def log_data(data):
    with open(log_file, "a") as file:
        file.write(json.dumps(data) + "\n")


def acUpdate(deltaT):
    # Collect game data
    lap_get = ac.getCarState(0, acsys.CS.LapCount)
    speed_get = ac.getCarState(0, acsys.CS.SpeedKMH)
    rpm_get = ac.getCarState(0, acsys.CS.RPM)
    throttle_get = ac.getCarState(0, acsys.CS.Gas)
    brake_get = ac.getCarState(0, acsys.CS.Brake)
    gear_get = ac.getCarState(0, acsys.CS.Gear)
    steer_get = ac.getCarState(0, acsys.CS.Steer)

    # Log the data
    log_entry = {
        "Laps": lap_get,
        "Speed": speed_get,
        "RPM": rpm_get,
        "Throttle": throttle_get,
        "Brake": brake_get,
        "Gear": gear_get,
        "Steer": steer_get,
    }
    log_data(log_entry)
