# ai control

def ai_control(current_speed, target_speed):
    """Simple control logic to adjust speed."""
    throttle = 0.0
    brake = 0.0

    if current_speed < target_speed - 5:
        throttle = min(1.0, (target_speed - current_speed) /
                       10.0)  # Gradual throttle
    elif current_speed > target_speed + 5:
        brake = min(1.0, (current_speed - target_speed) /
                    10.0)  # Gradual brake

    return throttle, brake


# Example usage
current_speed = telemetry.speedKmh
target_speed = 100  # Target speed in km/h

throttle, brake = ai_control(current_speed, target_speed)
print(f"Throttle: {throttle}, Brake: {brake}")
