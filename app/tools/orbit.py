import math

def calculate_orbital_velocity(mass: float, radius: float):
    """
    Calculates the circular orbital velocity.
    :param mass: Mass of the central body in kg.
    :param radius: Orbital radius in meters.
    :return: Orbital velocity in m/s.
    """
    G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
    velocity = math.sqrt((G * mass) / radius)
    return round(velocity, 2)
