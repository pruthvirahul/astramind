import math

def calculate_mach(velocity: float, temperature: float):
    gamma = 1.4          # Air
    R = 287              # J/kgK
    speed_of_sound = math.sqrt(gamma * R * temperature)
    mach = velocity / speed_of_sound
    return round(mach, 3)