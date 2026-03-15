import math

def calculate_delta_v(exhaust_velocity, initial_mass, final_mass):
    return exhaust_velocity * math.log(initial_mass / final_mass)