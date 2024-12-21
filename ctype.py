# read ac telemetry data

import ctypes


class SPageFilePhysics(ctypes.Structure):
    _fields_ = [
        ("speedKmh", ctypes.c_float),  # Speed in km/h
        ("gas", ctypes.c_float),      # Gas pedal position (0-1)
        ("brake", ctypes.c_float),    # Brake pedal position (0-1)
        ("steerAngle", ctypes.c_float),  # Steering angle in radians
        # Add other fields as needed
    ]


def read_shared_memory():
    shm_file = "Local\\acpmf_physics"
    size = ctypes.sizeof(SPageFilePhysics)
    shared_memory = ctypes.windll.kernel32.OpenFileMappingA(
        0x4, False, shm_file.encode('ascii'))

    if not shared_memory:
        raise FileNotFoundError(
            "Shared memory not found. Is Assetto Corsa running?")

    mapped_view = ctypes.windll.kernel32.MapViewOfFile(
        shared_memory, 0x4, 0, 0, size)
    if not mapped_view:
        raise MemoryError("Could not map view of shared memory.")

    data = SPageFilePhysics.from_address(mapped_view)
    return data


try:
    shm_file = "Local\\acpmf_physics"
    shared_memory = ctypes.windll.kernel32.OpenFileMappingA(
        0x4, False, shm_file.encode('ascii'))
    if not shared_memory:
        raise FileNotFoundError(
            "Shared memory not found. Is Assetto Corsa running?")

    size = ctypes.sizeof(SPageFilePhysics)
    mapped_view = ctypes.windll.kernel32.MapViewOfFile(
        shared_memory, 0x4, 0, 0, size)
    if not mapped_view:
        raise MemoryError("Could not map view of shared memory.")

    data = SPageFilePhysics.from_address(mapped_view)

    # Access and print specific fields
    print(f"Speed: {data.speedKmh} km/h")
    print(f"Gas: {data.gas * 100:.2f}%")  # Convert to percentage
    print(f"Brake: {data.brake * 100:.2f}%")
    print(f"Steering Angle: {data.steerAngle:.2f} radians")

except Exception as e:
    print(f"Error: {e}")
