import math


def calculate_u_inlet(wind_direction: float, wind_speed: float) -> str:
    wind_direction_rad = math.radians(wind_direction)

    # Calculate the velocity components Ux and Uy
    u_x = -wind_speed * math.sin(wind_direction_rad)
    u_y = -wind_speed * math.cos(wind_direction_rad)

    return u_x, u_y