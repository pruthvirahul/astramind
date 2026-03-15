import re
from app.tools.lift import calculate_lift
from app.tools.rocket import calculate_delta_v
from app.tools.mach import calculate_mach
from app.tools.orbit import calculate_orbital_velocity
from app.ai_model import generate_response
from app.memory.vectorstore import search
def extract_numbers(text):
    return list(map(float, re.findall(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", text)))

def handle_query(query: str):

    query_lower = query.lower()
    numbers = extract_numbers(query)

    if "lift" in query_lower:
        if len(numbers) >= 4:
            rho, velocity, area, cl = numbers[:4]
            lift = calculate_lift(rho, velocity, area, cl)
            return f"Calculated Lift: {lift} N"
        else:
            return "Please provide rho, velocity, area, and cl."
        
    elif "rocket" in query_lower or "delta" in query_lower:
        if len(numbers) >= 3:
            ve, m0, mf = numbers[:3]
            delta_v = calculate_delta_v(ve, m0, mf)
            return f"Delta-V: {round(delta_v,2)} m/s"
        else:
            return "Please provide exhaust_velocity, initial_mass, final_mass."

    elif "mach" in query_lower:
        if len(numbers) >= 2:
            velocity, temperature = numbers[:2]
            mach = calculate_mach(velocity, temperature)
            return f"Mach Number: {mach}"
        else:
            return "Please provide velocity and temperature (K)."

    elif "orbit" in query_lower:
        if len(numbers) >= 2:
            mass, radius = numbers[:2]
            velocity = calculate_orbital_velocity(mass, radius)
            return f"Orbital Velocity: {velocity} m/s"
        else:
            return "Please provide mass (kg) and orbital radius (m)."

    else:
        # RAG Implementation
        context_docs = search(query, top_k=2)
        context_text = "\n".join([d["document"]["text"] for d in context_docs])
        
        prompt = f"Knowledge Context: {context_text}\n\nQuestion: {query}\n\nAnswer like an aerospace expert:"
        return generate_response(prompt)