import time
import ac
import acsys
import json
import os
from datetime import datetime


lapcount_label = 1
lapcount = 1
speed = 0
speed_label = 0
rpm = 0
rpm_label = 0
throttle = 0
throttle_label = 0
brake = 0
brake_label = 0
gear = 0
gear_label = 0
steer = 0
steer_label = 0
lapTime = 0
lapTime_label = 0

lastTime = ac.getCarState(0, acsys.CS.LapTime)


def recordData(lapCount_get, lapTime_get, speedKPH_get, rpm_get, gear_get, throttle_get, brake_get, steer_get):
    data = {
        "lap": lapCount_get,
        "lapTime": lapTime_get,
        "speed": "{:.7f}".format(speedKPH_get),
        "rpm": "{:.7f}".format(rpm_get),
        "gear": gear_get,
        "throttle": throttle_get,
        "brake": brake_get,
        "steer": "{:.7f}".format(steer_get),
    }

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Define the path to the JSON file
    file_path = os.path.join(os.path.dirname(__file__), 'car_data.json')
    json_data = {}
    json_data[timestamp] = data

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Load the existing JSON data and append the new record
        with open(file_path, 'r+') as json_file:
            try:
                json_data = json.load(json_file)  # Read existing data
            except json.JSONDecodeError:
                json_data = {}  # Initialize a new dictionary if the file is invalid

            json_data[timestamp] = data  # Add the new record
            json_file.seek(0)  # Move to the start of the file
            json.dump(json_data, json_file, indent=4)  # Write the updated JSON
            json_file.truncate()  # Remove any leftover data
    else:
        # If file doesn't exist or is empty, create a new JSON object
        with open(file_path, 'w') as json_file:
            json.dump({timestamp: data}, json_file, indent=4)


def acMain(ac_version):
    global lapcount_label, speed_label, rpm_label, throttle_label, brake_label, gear_label, steer_label, lapTime_label, time_test

    appWindow = ac.newApp("data console")
    ac.setSize(appWindow, 200, 200)

    ac.log("Hello, Assetto Corsa application world!")
    ac.console("Hello, Assetto Corsa console!")

    lapcount_label = ac.addLabel(appWindow, "Laps: 0")
    ac.setPosition(lapcount_label, 10, 30)

    speed_label = ac.addLabel(appWindow, "Speed: 0 km/h")
    ac.setPosition(speed_label, 10, 50)

    rpm_label = ac.addLabel(appWindow, "RPM: 0")
    ac.setPosition(rpm_label, 10, 70)

    throttle_label = ac.addLabel(appWindow, "Throttle: 0%")
    ac.setPosition(throttle_label, 10, 90)

    brake_label = ac.addLabel(appWindow, "Brake: 0%")
    ac.setPosition(brake_label, 10, 110)

    gear_label = ac.addLabel(appWindow, "Gear: N")
    ac.setPosition(gear_label, 10, 130)

    steer_label = ac.addLabel(appWindow, "Steer: 0")
    ac.setPosition(steer_label, 10, 150)

    lapTime_label = ac.addLabel(appWindow, "Lap Time: 0")
    ac.setPosition(lapTime_label, 10, 170)

    time_test = ac.addLabel(appWindow, "Time: 0")
    ac.setPosition(time_test, 10, 190)

    return "data console"


def acUpdate(deltaT):
    global lapcount_label, lapcount
    global speed, speed_label
    global rpm, rpm_label
    global throttle, throttle_label
    global brake, brake_label
    global gear, gear_label
    global steer, steer_label
    global lapTime, lapTime_label
    global time_test, lastTime

    lapCount_get = ac.getCarState(0, acsys.CS.LapCount) + 1
    speedKPH_get = ac.getCarState(0, acsys.CS.SpeedKMH)
    rpm_get = ac.getCarState(0, acsys.CS.RPM)
    throttle_get = ac.getCarState(0, acsys.CS.Gas)
    brake_get = ac.getCarState(0, acsys.CS.Brake)
    gear_get = ac.getCarState(0, acsys.CS.Gear)
    steer_get = ac.getCarState(0, acsys.CS.Steer)
    lapTime_get = ac.getCarState(0, acsys.CS.LapTime)

    ac.log("Laps: {}, Speed: {}, RPM: {}, Throttle: {}, Brake: {}, Gear: {}, Steer: {}".format(
        lapCount_get, speedKPH_get, rpm_get, throttle_get, brake_get, gear_get, steer_get))

    if lapCount_get > lapcount:
        lapcount = lapCount_get
        lastTime = 0
        ac.setText(lapcount_label, "Laps: {}".format(lapcount))

    if speedKPH_get != speed:
        speed = speedKPH_get
        ac.setText(speed_label, "KM/H: {:.3f}".format(speed))

    if rpm_get != rpm:
        rpm = rpm_get
        ac.setText(rpm_label, "RPM: {:.3f}".format(rpm))

    if throttle != throttle_label:
        throttle = throttle_get
        ac.setText(throttle_label, "Throttle: {:.1f}%".format(throttle * 100))

    if brake_get != brake:
        brake = brake_get
        ac.setText(brake_label, "Brake: {:.1f}%".format(brake * 100))

    if gear != gear_get:
        gear = gear_get - 1
        if gear == -1:
            ac.setText(gear_label, "Gear: R")
        elif gear == 0:
            ac.setText(gear_label, "Gear: N")
        else:
            ac.setText(gear_label, "Gear: {}".format(gear))

    if steer != steer_get:
        steer = steer_get
        ac.setText(steer_label, "Steer: {:.1f}".format(steer))

    if lapTime_get != lapTime:
        lapTime = lapTime_get
        ac.setText(lapTime_label, "Lap Time: {:.3f}".format(lapTime))

    currentTime = ac.getCarState(0, acsys.CS.LapTime)
    time_difference = abs(currentTime - lastTime)

    if time_difference > 1000:
        recordData(lapCount_get, lapTime_get, speedKPH_get, rpm_get,
                   gear_get, throttle_get, brake_get, steer_get)
        lastTime = currentTime
        ac.setText(time_test, "Time: {}".format(time_difference))
