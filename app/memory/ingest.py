from app.memory.vectorstore import add_documents

def ingest_sample_data():
    docs = [
        {"id": "1", "text": "Lift is generated due to pressure difference between upper and lower wing surfaces."},
        {"id": "2", "text": "The Tsiolkovsky rocket equation determines delta-v using exhaust velocity and mass ratio."},
        {"id": "3", "text": "Mach number is the ratio of velocity to local speed of sound."},
        {"id": "4", "text": "Boundary layer behavior affects drag and flow separation."}
    ]
    add_documents(docs)

if __name__ == "__main__":
    ingest_sample_data()