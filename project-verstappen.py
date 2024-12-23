import ac
import acsys

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


def acMain(ac_version):
    global lapcount_label, speed_label, rpm_label, throttle_label, brake_label, gear_label, steer_label

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

    return "data console"


def acUpdate(deltaT):
    global lapcount_label, lapcount
    global speed, speed_label
    global rpm, rpm_label
    global throttle, throttle_label
    global brake, brake_label
    global gear, gear_label
    global steer, steer_label

    lap_get = ac.getCarState(0, acsys.CS.LapCount)
    speed_get = ac.getCarState(0, acsys.CS.SpeedKMH)
    rpm_get = ac.getCarState(0, acsys.CS.RPM)
    throttle_get = ac.getCarState(0, acsys.CS.Gas)
    brake_get = ac.getCarState(0, acsys.CS.Brake)
    gear_get = ac.getCarState(0, acsys.CS.Gear)
    steer_get = ac.getCarState(0, acsys.CS.Steer)

    ac.log("Laps: {}, Speed: {}, RPM: {}, Throttle: {}, Brake: {}, Gear: {}, Steer: {}".format(
        lap_get, speed_get, rpm_get, throttle_get, brake_get, gear_get, steer_get))

    if lap_get > lapcount:
        lapcount = lap_get
        ac.setText(lapcount_label, "Laps: {}".format(lapcount))

    if speed_get != speed:
        speed = speed_get
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
