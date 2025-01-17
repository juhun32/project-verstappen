from beamngpy import BeamNGpy, Scenario, Vehicle
import time

# Instantiate BeamNGpy instance running the simulator from the given path,
# communicating over localhost:25252
bng = BeamNGpy('localhost', 25252, home='C:\Program Files (x86)\Steam\steamapps\common\BeamNG.drive',
               user='/path/to/bng/tech/userfolder')

# Launch BeamNG.tech
bng.open()

# Create a scenario in automation_test_track called 'example'
scenario = Scenario('automation_test_track', 'example')

# Create an ETK800 with the licence plate 'PYTHON'
vehicle = Vehicle('ego_vehicle', model='etk800', license='PYTHON')

# # Add it to our scenario at this position and rotation
# scenario.add_vehicle(vehicle, pos=(-717, 101, 118),
#                      rot_quat=(0, 0, 0.3826834, 0.9238795))

# # Place files defining our scenario for the simulator to read
# scenario.make(bng)

# # Load and start our scenario
# bng.scenario.load(scenario)
# bng.scenario.start()

# # Make the vehicle's AI span the map
# vehicle.ai.set_mode('traffic')
# input('Hit Enter when done...')

# # Disconnect BeamNG
# bng.disconnect()

# # Or close the simulator
# # bng.close()

scenario.add_vehicle(vehicle, pos=(
    493.4843837138369, 178.14530187901983, 131.96188901015057), rot=(0, 90, 0))

# Start BeamNG and load the scenario
scenario.make(bng)
bng.scenario.load(scenario)
bng.scenario.start()

# Poll vehicle position
try:
    while True:
        # Retrieve vehicle state
        state = vehicle.state

        scenario.update()

        # Access the position
        position = state['pos']
        print(f"Vehicle Position: {position}")
        time.sleep(1)
finally:
    bng.close()
