import math


def calculate_u_inlet(wind_direction: float, wind_speed: float) -> str:
    # Convert wind_direction to radians (assuming degrees as input)
    wind_direction_rad = (90 - wind_direction) * (math.pi / 180.0)

    # Calculate the velocity components Ux and Uy
    u_x = wind_speed * math.cos(wind_direction_rad)
    u_y = wind_speed * math.sin(wind_direction_rad)

    # Create the U file entry string
    u_inlet_str = f"Uinlet ({u_x} {u_y} 0);"

    return u_inlet_str