import ac
import acsys

# App initialization


# def acMain(ac_version):
#     global app_window, speed_label, rpm_label, throttle_label, brake_label, gear_label

#     # Create the app
#     app_window = ac.newApp("project-verstappen")
#     ac.setTitle(app_window, "project-verstappen")
#     ac.setSize(app_window, 300, 200)

#     # Add labels to display car data
#     speed_label = ac.addLabel(app_window, "Speed: 0 km/h")
#     ac.setPosition(speed_label, 10, 30)

#     rpm_label = ac.addLabel(app_window, "RPM: 0")
#     ac.setPosition(rpm_label, 10, 60)

#     throttle_label = ac.addLabel(app_window, "Throttle: 0%")
#     ac.setPosition(throttle_label, 10, 90)

#     brake_label = ac.addLabel(app_window, "Brake: 0%")
#     ac.setPosition(brake_label, 10, 120)

#     gear_label = ac.addLabel(app_window, "Gear: N")
#     ac.setPosition(gear_label, 10, 150)

#     # Set a callback function to refresh the data
#     ac.addRenderCallback(app_window, on_render)

#     return "project-verstappen"


# # Function to refresh car data


# def on_render(deltaT):
#     try:
#         car_id = 0  # Player's car ID

#         # Fetch car data using ac.getCarState
#         speed = ac.getCarState(car_id, "SpeedKMH")
#         rpm = ac.getCarState(car_id, "RPM")
#         throttle = ac.getCarState(car_id, "Gas") * 100
#         brake = ac.getCarState(car_id, "Brake") * 100
#         gear = ac.getCarState(car_id, "Gear")

#         # Display gear as 'N' for 0, 'R' for -1, or the gear number
#         gear_display = "N" if gear == 0 else "R" if gear == -1 else str(gear)

#         # Update labels
#         ac.setText(speed_label, f"Speed: {speed:.1f} km/h")
#         ac.setText(rpm_label, f"RPM: {int(rpm)}")
#         ac.setText(throttle_label, f"Throttle: {throttle:.1f}%")
#         ac.setText(brake_label, f"Brake: {brake:.1f}%")
#         ac.setText(gear_label, f"Gear: {gear_display}")
#     except Exception as e:
#         ac.log(f"Error in on_render: {e}")


lapcount_label = 0
lapcount = 0
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


def acMain(ac_version):
    global lapcount_label, speed_label, rpm_label, throttle_label, brake_label, gear_label

    appWindow = ac.newApp("appName")
    ac.setSize(appWindow, 200, 200)

    ac.log("Hello, Assetto Corsa application world!")
    ac.console("Hello, Assetto Corsa console!")

    lapcount_label = ac.addLabel(appWindow, "Laps: 0")
    ac.setPosition(lapcount_label, 3, 30)

    speed_label = ac.addLabel(appWindow, "Speed: 0 km/h")
    ac.setPosition(speed_label, 10, 50)

    rpm_label = ac.addLabel(appWindow, "RPM: 0")
    ac.setPosition(rpm_label, 10, 70)

    throttle_label = ac.addLabel(appWindow, "Throttle: 0%")
    ac.setPosition(throttle_label, 10, 90)

    brake_label = ac.addLabel(appWindow, "Brake: 0%")
    ac.setPosition(brake_label, 10, 120)

    gear_label = ac.addLabel(appWindow, "Gear: N")
    ac.setPosition(gear_label, 10, 150)

    # Set a callback function to refresh the data
    # ac.addRenderCallback(appWindow, on_render)
    return "appName"


def acUpdate(deltaT):
    global lapcount_label, lapcount
    global speed, speed_label
    global rpm, rpm_label
    global throttle, throttle_label
    global brake, brake_label
    global gear, gear_label

    lap_get = ac.getCarState(0, acsys.CS.LapCount)
    speed_get = ac.getCarState(0, acsys.CS.SpeedKMH)
    rpm_get = ac.getCarState(0, acsys.CS.RPM)
    throttle_get = ac.getCarState(0, acsys.CS.Gas)
    brake_get = ac.getCarState(0, acsys.CS.Brake)
    gear_get = ac.getCarState(0, acsys.CS.Gear)

    ac.log("Laps: {}, Speed: {}, RPM: {}, Throttle: {}, Brake: {}, Gear: {}".format(
        lap_get, speed_get, rpm_get, throttle_get, brake_get, gear_get))

    if lap_get > lapcount:
        lapcount = lap_get
        ac.setText(lapcount_label, "Laps: {}".format(lapcount))

    if speed_get != speed:
        speed = speed_get
        ac.setText(speed_label, "KM/H: {}".format(speed))

    if rpm_get != rpm:
        rpm = rpm_get
        ac.setText(rpm_label, "RPM: {}".format(rpm))

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
