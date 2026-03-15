import json
import os

FEEDBACK_FILE = "feedback_log.json"
DATASET_FILE = "app/memory/fine_tune_dataset.jsonl"

def generate_dataset():
    if not os.path.exists(FEEDBACK_FILE):
        print("No feedback found.")
        return

    with open(FEEDBACK_FILE, "r") as f:
        data = json.load(f)

    # Filter for approved feedback only
    approved_data = [entry for entry in data if entry.get("approved")]

    if not approved_data:
        print("No approved feedback to generate dataset.")
        return

    with open(DATASET_FILE, "w") as f:
        for entry in approved_data:
            json_line = {
                "instruction": entry["query"],
                "input": "",
                "output": entry["response"]
            }
            f.write(json.dumps(json_line) + "\n")
    
    print(f"Generated dataset with {len(approved_data)} entries at {DATASET_FILE}")

if __name__ == "__main__":
    generate_dataset()
