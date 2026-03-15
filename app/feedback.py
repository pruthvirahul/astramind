import json
import os
from datetime import datetime

FEEDBACK_FILE = "feedback_log.json"

def store_feedback(query, response, approved=False):
    entry = {
        "timestamp": str(datetime.utcnow()),
        "query": query,
        "response": response,
        "approved": approved
    }

    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w") as f:
            json.dump([], f)

    with open(FEEDBACK_FILE, "r") as f:
        data = json.load(f)

    data.append(entry)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)
