from app.memory.vectorstore import add_documents

# A "Mastered" Aerospace Dataset
# Focusing on Graduate-level concepts
MEGA_DATASET = [
    {
        "text": "The Navier-Stokes equations describe the motion of viscous fluid substances. They are the cornerstone of modern aerodynamics and CFD (Computational Fluid Dynamics).",
        "metadata": {"topic": "Fluid Dynamics", "level": "Advanced"}
    },
    {
        "text": "The Kutta-Joukowski theorem states that the lift per unit span acting on a cylinder of any cross section is equal to the density of the fluid times the velocity of the fluid times the circulation.",
        "metadata": {"topic": "Aerodynamics", "level": "Mastery"}
    },
    {
        "text": "Hohmann Transfer Orbit: An elliptical orbit used to transfer between two circular orbits of different radii in the same plane. It is the most fuel-efficient method for such transfers.",
        "metadata": {"topic": "Orbital Mechanics", "level": "Intermediate"}
    },
    {
        "text": "Specific Impulse (Isp) is a measure of the efficiency of a rocket or jet engine. It represents the impulse (change in momentum) per unit of propellant consumed.",
        "metadata": {"topic": "Propulsion", "level": "Core"}
    },
    {
        "text": "The Boundary Layer is the layer of fluid in the immediate vicinity of a bounding surface where the effects of viscosity are significant. Transition from laminar to turbulent flow occurs here.",
        "metadata": {"topic": "Aerodynamics", "level": "Advanced"}
    },
    {
        "text": "Supersonic flow occurs when the speed of an object exceeds the local speed of sound (Mach > 1). This leads to the formation of shock waves and significant changes in air pressure and density.",
        "metadata": {"topic": "Gas Dynamics", "level": "Mastery"}
    },
    {
        "text": "Orbital Perturbations: Deviations from a perfect Keplerian orbit caused by factors like atmospheric drag, solar radiation pressure, and the non-spherical shape of the Earth (J2 effect).",
        "metadata": {"topic": "Astrodynamics", "level": "Mastery"}
    },
    {
        "text": "Heat Transfer in Re-entry: During atmospheric entry, vehicles experience intense aerodynamic heating. Thermal Protection Systems (TPS) like carbon-phenolic ablators or ceramic tiles are used to protect the structure.",
        "metadata": {"topic": "Thermodynamics", "level": "Advanced"}
    }
]

def run_mega_ingest():
    print("🚀 Injecting Graduate-Level Aerospace Knowledge...")
    add_documents(MEGA_DATASET)
    print("✅ Mastery Layer integrated into Vector Store.")

if __name__ == "__main__":
    run_mega_ingest()
