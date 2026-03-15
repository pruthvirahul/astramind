def calculate_lift(rho: float, velocity: float, area: float, cl: float):
    lift = 0.5 * rho * velocity**2 * area * cl
    return round(lift, 2)